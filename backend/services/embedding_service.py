"""Embedding service for RAG Ingestion Pipeline using Cohere."""

import cohere
import time
from typing import List, Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from exceptions import EmbeddingGenerationError, RateLimitError


class EmbeddingService:
    """Service class for handling embedding generation with Cohere."""

    def __init__(self):
        """Initialize the embedding service with Cohere client."""
        api_key = Config.COHERE_API_KEY
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(api_key)
        self.model = "embed-english-v3.0"  # Default model

    def embed_texts(self, texts: List[str], request_type: str = "search_document") -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts (List[str]): List of texts to embed
            request_type (str): Type of request (search_document, search_query, etc.)

        Returns:
            List[List[float]]: List of embeddings for each text
        """
        if not texts:
            return []

        try:
            # Rate limiting - pause if needed
            time.sleep(1.0 / Config.EMBEDDING_REQUESTS_PER_MINUTE * 60)  # Convert to seconds per request

            response = self.client.embed(
                texts=texts,
                model=self.model,
                input_type=request_type
            )

            return response.embeddings

        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg or "429" in error_msg:
                raise RateLimitError(f"Rate limit exceeded: {e}")
            elif "401" in error_msg or "unauthorized" in error_msg or "invalid api token" in error_msg:
                raise EmbeddingGenerationError(f"Invalid API token: {e}")
            else:
                raise EmbeddingGenerationError(f"Failed to generate embeddings: {e}")

    def embed_single_text(self, text: str, request_type: str = "search_document") -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text (str): Text to embed
            request_type (str): Type of request

        Returns:
            List[float]: Embedding vector for the text
        """
        embeddings = self.embed_texts([text], request_type)
        if embeddings:
            return embeddings[0]
        else:
            raise EmbeddingGenerationError("Failed to generate embedding for single text")