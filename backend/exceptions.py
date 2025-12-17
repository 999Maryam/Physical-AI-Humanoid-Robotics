"""Custom exceptions for RAG Ingestion Pipeline."""


class RAGIngestionError(Exception):
    """Base exception for RAG ingestion pipeline errors."""
    pass


class ContentExtractionError(RAGIngestionError):
    """Raised when content extraction fails."""
    pass


class EmbeddingGenerationError(RAGIngestionError):
    """Raised when embedding generation fails."""
    pass


class VectorStorageError(RAGIngestionError):
    """Raised when vector storage operations fail."""
    pass


class ConfigurationError(RAGIngestionError):
    """Raised when configuration is invalid or missing."""
    pass


class RateLimitError(RAGIngestionError):
    """Raised when API rate limits are exceeded."""
    pass


class NetworkError(RAGIngestionError):
    """Raised when network requests fail."""
    pass