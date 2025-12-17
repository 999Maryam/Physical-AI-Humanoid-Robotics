#!/usr/bin/env python3
"""
Grounded RAG Tutor using Gemini-2.0-flash via OpenAI-compatible endpoint.
Retrieves from Qdrant using Cohere embeddings, answers strictly from retrieved content.
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest
from cohere import Client as CohereClient
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize clients
cohere_client = CohereClient(api_key=os.getenv("COHERE_API_KEY"))

# Qdrant client setup (supports both local and cloud)
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_host = os.getenv("QDRANT_HOST", "localhost")
qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))

if qdrant_url:
    qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key, prefer_grpc=True)
else:
    qdrant_client = QdrantClient(host=qdrant_host, port=qdrant_port)

# OpenAI client pointing to Gemini's OpenAI-compatible endpoint
openai_client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_embedding")


def retrieve(query: str) -> list[str]:
    """Retrieve top 5 relevant text chunks from Qdrant using Cohere embedding."""
    print(f"Retrieving documents for query: {query}")

    # Get embedding from Cohere
    embedding = cohere_client.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings[0]

    # Search in Qdrant using the new .search() method (latest client)
    search_results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=5,
        with_payload=True
    )

    # Extract text from payload
    texts = []
    for point in search_results:
        payload = point.payload
        if isinstance(payload, dict):
            text = payload.get("text") or payload.get("content") or str(payload)
            texts.append(text)
        else:
            texts.append(str(payload))

    print(f"Retrieved {len(texts)} documents")
    return texts


def create_rag_response(user_query: str) -> str:
    """Generate grounded response using only retrieved documents."""
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
        response = openai_client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=512
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling Gemini: {e}")
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