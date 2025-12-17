"""Data models for RAG Ingestion Pipeline."""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


@dataclass
class DocumentChunk:
    """Represents a segment of extracted content with associated metadata."""

    id: str
    content: str
    source_url: str
    chunk_index: int
    document_title: str = ""
    created_at: datetime = None
    token_count: int = 0
    embedding: Optional[List[float]] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class EmbeddingVector:
    """High-dimensional numerical representation of document chunk semantics."""

    vector_id: str
    embedding: List[float]
    document_chunk_id: str
    model_version: str = "embed-english-v3.0"
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class ContentCollection:
    """Organized group of documents from a specific Docusaurus website."""

    collection_name: str
    source_website: str
    document_count: int = 0
    chunk_count: int = 0
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


# Pydantic models for RAG testing functionality
class Document(BaseModel):
    """Represents an ingested document with text content and metadata"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: List[float]
    collection_name: str


class QueryResult(BaseModel):
    """Contains retrieved documents with relevance scores"""
    id: str
    content: str
    score: float
    metadata: Dict[str, Any]
    position: int


class RetrievalRequest(BaseModel):
    """Input for retrieval operations"""
    query_text: str
    top_k: int = Field(default=5, ge=1, le=100)
    collection_name: str = "documents"
    min_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class RetrievalResponse(BaseModel):
    """Output from retrieval operations"""
    query: str
    results: List[QueryResult]
    total_count: int
    execution_time: float


class ValidationResult(BaseModel):
    """Result of validation operations"""
    is_valid: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)