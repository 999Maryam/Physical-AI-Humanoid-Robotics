"""Configuration module for RAG Ingestion Pipeline."""

import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class to store all configuration values."""

    # Cohere API Configuration
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    # Qdrant Configuration
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

    # Default values for processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_embedding")
    TARGET_URL = os.getenv("TARGET_URL", "https://physical-ai-humanoid-robotics-eight-snowy.vercel.app/")

    # Rate limiting
    REQUESTS_PER_MINUTE = int(os.getenv("REQUESTS_PER_MINUTE", "30"))
    EMBEDDING_REQUESTS_PER_MINUTE = int(os.getenv("EMBEDDING_REQUESTS_PER_MINUTE", "100"))

    # Processing limits
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "10000"))  # characters
    MAX_TOKENS_PER_CHUNK = int(os.getenv("MAX_TOKENS_PER_CHUNK", "256"))

    # RAG Testing Configuration
    DEFAULT_RETRIEVAL_TOP_K = int(os.getenv("DEFAULT_RETRIEVAL_TOP_K", "5"))
    DEFAULT_MIN_SCORE = float(os.getenv("DEFAULT_MIN_SCORE", "0.0"))


def get_config():
    """Get configuration instance."""
    return Config()