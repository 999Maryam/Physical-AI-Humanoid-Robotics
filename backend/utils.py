"""Utility functions for RAG Ingestion Pipeline."""

import re
import tiktoken
from typing import List


def count_tokens(text: str, model_name: str = "gpt-3.5-turbo") -> int:
    """
    Count the number of tokens in a text using tiktoken.

    Args:
        text (str): The text to count tokens for
        model_name (str): The model name to use for tokenization

    Returns:
        int: Number of tokens in the text
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
        tokens = encoding.encode(text)
        return len(tokens)
    except Exception:
        # Fallback: rough estimation (4 chars per token on average)
        return len(text) // 4


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing formatting.

    Args:
        text (str): The text to clean

    Returns:
        str: Cleaned text
    """
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    # Normalize newlines
    text = re.sub(r'\n+', '\n', text)

    return text


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into chunks with specified size and overlap.

    Args:
        text (str): The text to chunk
        chunk_size (int): Maximum size of each chunk (in tokens)
        overlap (int): Number of tokens to overlap between chunks

    Returns:
        List[str]: List of text chunks
    """
    if not text:
        return []

    # Use tiktoken to encode the text
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)

    chunks = []
    start_idx = 0

    while start_idx < len(tokens):
        # Calculate end index for the current chunk
        end_idx = start_idx + chunk_size

        # Extract the token slice for this chunk
        chunk_tokens = tokens[start_idx:end_idx]

        # Decode back to text
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)

        # Move start index forward by chunk_size - overlap
        start_idx = end_idx - overlap

        # Ensure we don't get stuck in an infinite loop
        if start_idx >= len(tokens):
            break
        if end_idx - start_idx <= 0:
            # If overlap is too large, advance by 1 token
            start_idx = start_idx + 1

    # Clean up each chunk
    cleaned_chunks = [clean_text(chunk) for chunk in chunks if chunk.strip()]

    return cleaned_chunks


def validate_vector(vector: List[float], expected_dim: int = None) -> bool:
    """
    Validate that a vector is properly formatted.

    Args:
        vector: List of floats representing the vector
        expected_dim: Expected dimension of the vector (optional)

    Returns:
        bool: True if vector is valid, False otherwise
    """
    if not isinstance(vector, list):
        return False

    if not vector:  # Empty vector
        return False

    # Check that all elements are floats/numbers
    if not all(isinstance(val, (int, float, complex)) for val in vector):
        return False

    # Check dimension if specified
    if expected_dim is not None and len(vector) != expected_dim:
        return False

    # Check that all values are finite (not NaN or infinity)
    import math
    if any(not math.isfinite(val) for val in vector):
        return False

    return True


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        float: Cosine similarity score between -1 and 1
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same dimension")

    # Calculate dot product
    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    # Calculate magnitudes
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5

    # Avoid division by zero
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    return dot_product / (magnitude1 * magnitude2)


def normalize_vector(vector: List[float]) -> List[float]:
    """
    Normalize a vector to unit length.

    Args:
        vector: Input vector to normalize

    Returns:
        List[float]: Normalized vector
    """
    magnitude = sum(x * x for x in vector) ** 0.5

    if magnitude == 0:
        return vector  # Return original if zero vector

    return [x / magnitude for x in vector]


def calculate_vector_stats(vectors: List[List[float]]) -> dict:
    """
    Calculate statistics for a list of vectors.

    Args:
        vectors: List of vectors to analyze

    Returns:
        dict: Statistics including count, avg dimension, min/max values
    """
    if not vectors:
        return {
            "count": 0,
            "avg_dimension": 0,
            "min_value": None,
            "max_value": None,
            "avg_magnitude": 0
        }

    dimensions = [len(vec) for vec in vectors]
    all_values = [val for vec in vectors for val in vec]
    magnitudes = [sum(x * x for x in vec) ** 0.5 for vec in vectors]

    return {
        "count": len(vectors),
        "avg_dimension": sum(dimensions) / len(dimensions),
        "min_dimension": min(dimensions),
        "max_dimension": max(dimensions),
        "min_value": min(all_values),
        "max_value": max(all_values),
        "avg_magnitude": sum(magnitudes) / len(magnitudes),
        "zero_vectors": sum(1 for vec in vectors if sum(x * x for x in vec) == 0)
    }


def setup_logging():
    """Set up logging configuration for the application."""
    import logging
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("rag_ingestion.log"),
        ],
    )