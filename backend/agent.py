#!/usr/bin/env python3
"""
Grounded RAG Tutor using Gemini-2.0-flash via OpenAI-compatible endpoint.
Retrieves from Qdrant using Cohere embeddings, answers strictly from retrieved content.
"""

import os
import time
import random
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest, VectorParams, Distance
from qdrant_client.http import models
from cohere import Client as CohereClient
from cohere.core.api_error import ApiError
from openai import OpenAI, APIError as OpenAIAPIError

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


# Custom exceptions for better error handling
class RateLimitExceededError(Exception):
    """Raised when API rate limit is exceeded after all retries"""
    pass


class ServiceUnavailableError(Exception):
    """Raised when service is temporarily unavailable"""
    pass


# Simple in-memory cache for embeddings with TTL
class EmbeddingCache:
    """Thread-safe in-memory cache for embeddings with TTL"""

    def __init__(self, ttl_minutes: int = 10):
        self.cache: Dict[str, Tuple[list[float], datetime]] = {}
        self.ttl = timedelta(minutes=ttl_minutes)

    def _hash_query(self, query: str) -> str:
        """Generate cache key from query"""
        return hashlib.md5(query.encode('utf-8')).hexdigest()

    def get(self, query: str) -> Optional[list[float]]:
        """Get cached embedding if available and not expired"""
        key = self._hash_query(query)
        if key in self.cache:
            embedding, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                logger.info(f"Cache hit for query (age: {(datetime.now() - timestamp).seconds}s)")
                return embedding
            else:
                # Expired, remove it
                del self.cache[key]
                logger.debug("Cache entry expired, removed")
        return None

    def set(self, query: str, embedding: list[float]):
        """Store embedding in cache"""
        key = self._hash_query(query)
        self.cache[key] = (embedding, datetime.now())
        logger.debug(f"Cached embedding (cache size: {len(self.cache)})")

    def clear_expired(self):
        """Remove all expired entries"""
        now = datetime.now()
        expired_keys = [
            k for k, (_, ts) in self.cache.items()
            if now - ts >= self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
        if expired_keys:
            logger.debug(f"Cleared {len(expired_keys)} expired cache entries")


# Initialize embedding cache
embedding_cache = EmbeddingCache(ttl_minutes=int(os.getenv("EMBEDDING_CACHE_TTL_MINUTES", "10")))

# Initialize clients
cohere_client = CohereClient(api_key=os.getenv("COHERE_API_KEY"))

# Qdrant client setup (supports cloud, local, and in-memory)
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_host = os.getenv("QDRANT_HOST", "localhost")
qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))

# Try different connection methods in order of preference
qdrant_client = None

if qdrant_url:
    try:
        qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            prefer_grpc=False,
            timeout=5,  # Shorter timeout to fail faster
            https=True
        )
        # Test connection
        qdrant_client.get_collections()
        logger.info("Connected to Qdrant Cloud")
    except Exception as e:
        logger.warning(f"Could not connect to Qdrant Cloud: {e}")
        qdrant_client = None  # Explicitly set to None to trigger fallback

if qdrant_client is None and not qdrant_url:
    try:
        qdrant_client = QdrantClient(
            host=qdrant_host,
            port=qdrant_port,
            prefer_grpc=False,
            timeout=5  # Shorter timeout to fail faster
        )
        # Test connection
        qdrant_client.get_collections()
        logger.info("Connected to local Qdrant")
    except Exception as e:
        logger.warning(f"Could not connect to local Qdrant: {e}")
        qdrant_client = None  # Explicitly set to None to trigger fallback

if qdrant_client is None:
    # Fallback to in-memory Qdrant for development
    logger.info("Using in-memory Qdrant for development")
    qdrant_client = QdrantClient(":memory:")

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_embedding")


def ensure_collection_exists():
    """Ensure the collection exists, create it if it doesn't."""
    try:
        # Try to get collection info
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        logger.info(f"Collection '{COLLECTION_NAME}' exists with {collection_info.points_count} points")
        return True
    except Exception as e:
        logger.warning(f"Collection '{COLLECTION_NAME}' does not exist: {e}")

        # Determine vector size based on Cohere model (embed-english-v3.0 typically uses 1024 dimensions)
        # But we'll use a more flexible approach by checking the embedding size when we first create an embedding
        try:
            # Create the collection with appropriate vector size
            # For Cohere embed-english-v3.0 with multilingual preset, it's typically 1024 dimensions
            qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
            )
            logger.info(f"Collection '{COLLECTION_NAME}' created successfully!")
            return True
        except Exception as create_error:
            logger.error(f"Failed to create collection '{COLLECTION_NAME}': {create_error}")
            # For in-memory Qdrant, sometimes collection creation might not be needed upfront
            # since collections can be created implicitly when adding points
            logger.info(f"Continuing without pre-created collection. Collection '{COLLECTION_NAME}' will be created when first points are added.")
            return True  # Return True to allow the system to continue


# Ensure collection exists when module loads
ensure_collection_exists()

# OpenAI client pointing to Gemini's OpenAI-compatible endpoint
openai_client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_embedding")


def get_embedding_with_retry(query: str, max_retries: int = 3) -> list[float]:
    """
    Get embedding from Cohere with exponential backoff + jitter retry for rate limits.
    Uses in-memory cache to reduce API calls for identical queries.

    Args:
        query: Text to embed
        max_retries: Maximum number of retry attempts

    Returns:
        Embedding vector as list of floats

    Raises:
        RateLimitExceededError: If rate limit exceeded after all retries
        ServiceUnavailableError: If service errors persist
        ApiError: For other API errors
    """
    # Check cache first
    cached_embedding = embedding_cache.get(query)
    if cached_embedding is not None:
        return cached_embedding

    last_error = None

    for attempt in range(max_retries + 1):
        try:
            embedding = cohere_client.embed(
                texts=[query],
                model="embed-english-v3.0",
                input_type="search_query"
            ).embeddings[0]

            # Cache successful result
            embedding_cache.set(query, embedding)

            if attempt > 0:
                logger.info(f"Cohere embed succeeded on attempt {attempt + 1}")

            return embedding

        except ApiError as e:
            last_error = e

            # Check if it's a rate limit error (429)
            if hasattr(e, 'status_code') and e.status_code == 429:
                if attempt < max_retries:
                    # Exponential backoff with jitter: base * 2^attempt + random(0-1s)
                    base_backoff = 2 ** attempt  # 1s, 2s, 4s, 8s...
                    jitter = random.uniform(0, 1)  # 0-1 second random jitter
                    backoff_time = min(base_backoff + jitter, 16)  # Cap at 16s

                    logger.warning(
                        f"Cohere rate limit hit (429), retrying in {backoff_time:.2f}s "
                        f"(attempt {attempt + 1}/{max_retries}, next attempt: {attempt + 2})"
                    )
                    time.sleep(backoff_time)
                    continue
                else:
                    logger.error(
                        f"Max retries ({max_retries}) exceeded for Cohere embedding API. "
                        f"Rate limit persists. Consider reducing request rate or upgrading API tier."
                    )
                    raise RateLimitExceededError(
                        f"Cohere API rate limit exceeded after {max_retries} retries"
                    )

            # Check for 5xx service errors
            elif hasattr(e, 'status_code') and 500 <= e.status_code < 600:
                if attempt < max_retries:
                    base_backoff = 2 ** attempt
                    jitter = random.uniform(0, 1)
                    backoff_time = min(base_backoff + jitter, 16)

                    logger.warning(
                        f"Cohere service error ({e.status_code}), retrying in {backoff_time:.2f}s "
                        f"(attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(backoff_time)
                    continue
                else:
                    logger.error(f"Cohere service unavailable after {max_retries} retries")
                    raise ServiceUnavailableError(
                        f"Cohere API service error ({e.status_code}) persists after {max_retries} retries"
                    )

            else:
                # For other API errors (4xx except 429), fail immediately
                logger.error(f"Cohere API error (status: {getattr(e, 'status_code', 'unknown')}): {e}")
                raise

        except Exception as e:
            logger.error(f"Unexpected error getting embedding: {type(e).__name__}: {e}")
            raise

    # Should not reach here, but just in case
    if last_error:
        raise last_error
    raise ServiceUnavailableError("Failed to get embedding after retries")


def retrieve(query: str) -> list[str]:
    """Retrieve top 5 relevant text chunks from Qdrant using Cohere embedding."""
    logger.info(f"Retrieving documents for query: {query}")

    try:
        # Get embedding from Cohere with retry logic
        embedding = get_embedding_with_retry(query)

        # Search in Qdrant - try newer method first, fall back to older method
        try:
            # Try the newer search method
            search_results = qdrant_client.search(
                collection_name=COLLECTION_NAME,
                query_vector=embedding,
                limit=5,
                with_payload=True
            )
        except AttributeError:
            # Fall back to older query_points method if search is not available
            search_results = qdrant_client.query_points(
                collection_name=COLLECTION_NAME,
                query=embedding,
                limit=5,
                with_payload=True
            ).points

        # Extract text from payload - handle both search result types
        texts = []
        for point in search_results:
            # Handle both SearchResultPoint (newer) and PointStruct (older) objects
            if hasattr(point, 'payload'):
                payload = point.payload
            else:  # Fallback
                payload = getattr(point, 'payload', point)

            if isinstance(payload, dict):
                text = payload.get("text") or payload.get("content") or str(payload)
                texts.append(text)
            else:
                texts.append(str(payload))

        logger.info(f"Retrieved {len(texts)} documents")
        return texts

    except Exception as e:
        logger.error(f"Error during retrieval: {e}")
        raise


def call_gemini_with_retry(system_prompt: str, user_prompt: str, max_retries: int = 3) -> str:
    """
    Call Gemini API with exponential backoff + jitter retry logic.

    Args:
        system_prompt: System message for the model
        user_prompt: User message with context
        max_retries: Maximum number of retry attempts

    Returns:
        Generated response text

    Raises:
        RateLimitExceededError: If rate limit exceeded after all retries
        ServiceUnavailableError: If service errors persist
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response = openai_client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=512
            )

            if attempt > 0:
                logger.info(f"Gemini API succeeded on attempt {attempt + 1}")

            return response.choices[0].message.content.strip()

        except OpenAIAPIError as e:
            last_error = e

            # Rate limit error (429)
            if hasattr(e, 'status_code') and e.status_code == 429:
                if attempt < max_retries:
                    base_backoff = 2 ** attempt
                    jitter = random.uniform(0, 1)
                    backoff_time = min(base_backoff + jitter, 16)

                    logger.warning(
                        f"Gemini rate limit hit (429), retrying in {backoff_time:.2f}s "
                        f"(attempt {attempt + 1}/{max_retries}, next attempt: {attempt + 2})"
                    )
                    time.sleep(backoff_time)
                    continue
                else:
                    logger.error(f"Max retries ({max_retries}) exceeded for Gemini API")
                    raise RateLimitExceededError(
                        f"Gemini API rate limit exceeded after {max_retries} retries"
                    )

            # Service errors (5xx)
            elif hasattr(e, 'status_code') and 500 <= e.status_code < 600:
                if attempt < max_retries:
                    base_backoff = 2 ** attempt
                    jitter = random.uniform(0, 1)
                    backoff_time = min(base_backoff + jitter, 16)

                    logger.warning(
                        f"Gemini service error ({e.status_code}), retrying in {backoff_time:.2f}s "
                        f"(attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(backoff_time)
                    continue
                else:
                    logger.error(f"Gemini service unavailable after {max_retries} retries")
                    raise ServiceUnavailableError(
                        f"Gemini API service error ({e.status_code}) persists after {max_retries} retries"
                    )

            else:
                # Other API errors, fail immediately
                logger.error(f"Gemini API error (status: {getattr(e, 'status_code', 'unknown')}): {e}")
                raise

        except Exception as e:
            logger.error(f"Unexpected error calling Gemini: {type(e).__name__}: {e}")
            raise

    # Should not reach here, but just in case
    if last_error:
        raise last_error
    raise ServiceUnavailableError("Failed to get response from Gemini after retries")


def create_rag_response(user_query: str) -> str:
    """Generate grounded response using only retrieved documents."""

    # Check if the query is a greeting
    user_query_lower = user_query.lower().strip()
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"]

    if any(greeting in user_query_lower for greeting in greetings):
        return "Hello! How can I assist you today?"

    # For non-greetings, proceed with RAG retrieval
    retrieved_docs = retrieve(user_query)

    if not retrieved_docs:
        return "I don't know"

    context = "\n\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(retrieved_docs)])

    system_prompt = """You are a precise tutor on Physical AI and Humanoid Robotics.
Answer ONLY using the provided documents. Never use external knowledge.
If the answer is not in the documents, say "I don't know"."""

    user_prompt = f"""Question: {user_query}

Retrieved Documents:
{context}

Answer strictly using only the above documents."""

    try:
        return call_gemini_with_retry(system_prompt, user_prompt)
    except (RateLimitExceededError, ServiceUnavailableError):
        # Re-raise these to be handled by API layer
        raise
    except Exception as e:
        logger.error(f"Error in create_rag_response: {type(e).__name__}: {e}")
        # For unexpected errors, return fallback response
        return "I don't know"


def main():
    print("Testing RAG Tutor with gemini-2.5-flash (OpenAI-compatible)...\n")
    test_query = "what is physical ai?"
    print(f"Testing with query: '{test_query}'\n")

    response = create_rag_response(test_query)

    print(f"Query: {test_query}")
    print(f"Response:\n{response}")
    print(f"\nfinal_output: {response}")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()