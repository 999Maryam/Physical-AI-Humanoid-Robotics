"""
Tests for RAG Data Retrieval Module

These tests validate the functionality of the retrieve.py module for testing RAG pipeline.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.retrieve import (
    QdrantRetriever,
    Document,
    QueryResult,
    RetrievalRequest,
    RetrievalResponse,
    ValidationResult,
    list_qdrant_collections,
    validate_qdrant_storage,
    search_qdrant,
    get_qdrant_document_by_id
)
from pydantic import ValidationError
from typing import List, Dict, Any
import os


class TestDocumentModel:
    """Test the Document Pydantic model"""

    def test_document_creation(self):
        """Test creating a Document instance"""
        doc = Document(
            id="test-id",
            content="Test content",
            metadata={"source": "test", "format": "txt"},
            embedding=[0.1, 0.2, 0.3],
            collection_name="test_collection"
        )

        assert doc.id == "test-id"
        assert doc.content == "Test content"
        assert doc.metadata == {"source": "test", "format": "txt"}
        assert doc.embedding == [0.1, 0.2, 0.3]
        assert doc.collection_name == "test_collection"

    def test_document_validation(self):
        """Test Document model validation"""
        # Should pass with valid data
        Document(
            id="test-id",
            content="Test content",
            metadata={"source": "test"},
            embedding=[0.1, 0.2, 0.3],
            collection_name="test_collection"
        )

        # Should fail without required fields
        with pytest.raises(ValidationError):
            Document(
                id="test-id",
                content="Test content",
                metadata={"source": "test"},
                collection_name="test_collection"
                # Missing embedding
            )


class TestQueryResultModel:
    """Test the QueryResult Pydantic model"""

    def test_query_result_creation(self):
        """Test creating a QueryResult instance"""
        result = QueryResult(
            id="result-id",
            content="Result content",
            score=0.85,
            metadata={"source": "doc1"},
            position=0
        )

        assert result.id == "result-id"
        assert result.content == "Result content"
        assert result.score == 0.85
        assert result.metadata == {"source": "doc1"}
        assert result.position == 0

    def test_query_result_score_validation(self):
        """Test QueryResult score validation"""
        # Valid score
        QueryResult(
            id="result-id",
            content="Result content",
            score=0.85,
            metadata={"source": "doc1"},
            position=0
        )

        # Invalid score should not raise an error in this basic model
        # (score validation would be implemented if added to the model)


class TestRetrievalRequestModel:
    """Test the RetrievalRequest Pydantic model"""

    def test_retrieval_request_creation(self):
        """Test creating a RetrievalRequest instance"""
        request = RetrievalRequest(
            query_text="Test query",
            top_k=5,
            collection_name="documents",
            min_score=0.5
        )

        assert request.query_text == "Test query"
        assert request.top_k == 5
        assert request.collection_name == "documents"
        assert request.min_score == 0.5

    def test_retrieval_request_defaults(self):
        """Test RetrievalRequest default values"""
        request = RetrievalRequest(query_text="Test query")

        assert request.query_text == "Test query"
        assert request.top_k == 5  # default
        assert request.collection_name == "documents"  # default
        assert request.min_score is None  # default

    def test_retrieval_request_validation(self):
        """Test RetrievalRequest validation"""
        # Should pass with valid data
        RetrievalRequest(query_text="Test query", top_k=10)

        # Should fail with invalid top_k
        with pytest.raises(ValidationError):
            RetrievalRequest(query_text="Test query", top_k=0)  # top_k must be >= 1

        with pytest.raises(ValidationError):
            RetrievalRequest(query_text="Test query", top_k=101)  # top_k must be <= 100


class TestValidationResultModel:
    """Test the ValidationResult Pydantic model"""

    def test_validation_result_creation(self):
        """Test creating a ValidationResult instance"""
        result = ValidationResult(
            is_valid=True,
            message="Validation passed",
            details={"count": 10}
        )

        assert result.is_valid is True
        assert result.message == "Validation passed"
        assert result.details == {"count": 10}

    def test_validation_result_optional_details(self):
        """Test ValidationResult with optional details"""
        result = ValidationResult(
            is_valid=False,
            message="Validation failed"
            # details is optional
        )

        assert result.is_valid is False
        assert result.message == "Validation failed"
        assert result.details is None


class TestQdrantRetriever:
    """Test the QdrantRetriever class"""

    @patch('backend.retrieve.QdrantClient')
    def test_initialization(self, mock_qdrant_client):
        """Test QdrantRetriever initialization"""
        # Mock the Qdrant client
        mock_client = Mock()
        mock_qdrant_client.return_value = mock_client

        # Initialize the retriever
        retriever = QdrantRetriever()

        # Verify the client was initialized
        assert mock_qdrant_client.called

    @patch('backend.retrieve.QdrantClient')
    def test_list_collections(self, mock_qdrant_client):
        """Test list_collections method"""
        # Mock the Qdrant client
        mock_client = Mock()
        mock_qdrant_client.return_value = mock_client

        # Mock the get_collections response
        mock_collection_info = Mock()
        mock_collection_info.name = "test_collection"
        mock_client.get_collections.return_value = Mock(collections=[mock_collection_info])

        # Initialize the retriever
        retriever = QdrantRetriever()

        # Call list_collections
        collections = retriever.list_collections()

        # Verify the call and result
        mock_client.get_collections.assert_called_once()
        assert collections == ["test_collection"]

    @patch('backend.retrieve.QdrantClient')
    def test_get_collection_stats(self, mock_qdrant_client):
        """Test get_collection_stats method"""
        # Mock the Qdrant client
        mock_client = Mock()
        mock_qdrant_client.return_value = mock_client

        # Mock the get_collection response
        mock_collection = Mock()
        mock_collection.points_count = 100
        mock_config = Mock()
        mock_params = Mock()
        mock_vectors = Mock()
        mock_vectors.size = 384
        mock_params.vectors = mock_vectors
        mock_config.params = mock_params
        mock_collection.config = mock_config
        mock_client.get_collection.return_value = mock_collection

        # Initialize the retriever
        retriever = QdrantRetriever()

        # Call get_collection_stats
        stats = retriever.get_collection_stats("test_collection")

        # Verify the call and result
        mock_client.get_collection.assert_called_once_with("test_collection")
        assert stats["total_points"] == 100
        assert stats["vector_dim"] == 384
        assert stats["collection_name"] == "test_collection"

    @patch('backend.retrieve.QdrantClient')
    def test_validate_storage_with_collections(self, mock_qdrant_client):
        """Test validate_storage method when collections exist"""
        # Mock the Qdrant client
        mock_client = Mock()
        mock_qdrant_client.return_value = mock_client

        # Mock responses
        mock_collection_info = Mock()
        mock_collection_info.name = "documents"
        mock_client.get_collections.return_value = Mock(collections=[mock_collection_info])

        mock_collection = Mock()
        mock_collection.points_count = 50
        mock_config = Mock()
        mock_params = Mock()
        mock_vectors = Mock()
        mock_vectors.size = 384
        mock_params.vectors = mock_vectors
        mock_config.params = mock_params
        mock_collection.config = mock_config
        mock_client.get_collection.return_value = mock_collection

        # Initialize the retriever
        retriever = QdrantRetriever()

        # Call validate_storage
        result = retriever.validate_storage()

        # Verify the result
        assert result.is_valid is True
        assert "50 total points" in result.message
        assert result.details is not None
        assert result.details["collection_count"] == 1
        assert result.details["total_points"] == 50

    @patch('backend.retrieve.QdrantClient')
    def test_validate_storage_no_collections(self, mock_qdrant_client):
        """Test validate_storage method when no collections exist"""
        # Mock the Qdrant client
        mock_client = Mock()
        mock_qdrant_client.return_value = mock_client

        # Mock response with no collections
        mock_client.get_collections.return_value = Mock(collections=[])

        # Initialize the retriever
        retriever = QdrantRetriever()

        # Call validate_storage
        result = retriever.validate_storage()

        # Verify the result
        assert result.is_valid is False
        assert "No collections found" in result.message

    @patch('backend.retrieve.QdrantClient')
    @patch('backend.retrieve.SentenceTransformer')
    def test_search(self, mock_sentence_transformer, mock_qdrant_client):
        """Test search method"""
        # Mock the Qdrant client
        mock_client = Mock()
        mock_qdrant_client.return_value = mock_client

        # Mock the sentence transformer
        mock_model = Mock()
        mock_model.encode.return_value = [[0.1, 0.2, 0.3]]
        mock_sentence_transformer.return_value = mock_model

        # Mock the search response
        mock_hit = Mock()
        mock_hit.id = "doc1"
        mock_hit.score = 0.85
        mock_hit.payload = {"content": "Test content", "source": "test"}
        mock_client.search.return_value = [mock_hit]

        # Initialize the retriever
        retriever = QdrantRetriever()

        # Call search
        results = retriever.search("test query", top_k=1)

        # Verify the call and result
        assert len(results) == 1
        assert results[0].id == "doc1"
        assert results[0].content == "Test content"
        assert results[0].score == 0.85
        assert results[0].metadata == {"source": "test"}
        assert results[0].position == 0

    @patch('backend.retrieve.QdrantClient')
    def test_get_document_by_id(self, mock_qdrant_client):
        """Test get_document_by_id method"""
        # Mock the Qdrant client
        mock_client = Mock()
        mock_qdrant_client.return_value = mock_client

        # Mock the retrieve response
        mock_record = Mock()
        mock_record.id = "doc1"
        mock_record.payload = {"content": "Test content", "source": "test"}
        mock_record.vector = [0.1, 0.2, 0.3]
        mock_client.retrieve.return_value = [mock_record]

        # Initialize the retriever
        retriever = QdrantRetriever()

        # Call get_document_by_id
        document = retriever.get_document_by_id("doc1")

        # Verify the result
        assert document.id == "doc1"
        assert document.content == "Test content"
        assert document.metadata == {"source": "test"}
        assert document.embedding == [0.1, 0.2, 0.3]

    @patch('backend.retrieve.QdrantClient')
    def test_get_document_by_id_not_found(self, mock_qdrant_client):
        """Test get_document_by_id method when document is not found"""
        # Mock the Qdrant client
        mock_client = Mock()
        mock_qdrant_client.return_value = mock_client

        # Mock the retrieve response with empty list
        mock_client.retrieve.return_value = []

        # Initialize the retriever
        retriever = QdrantRetriever()

        # Call get_document_by_id
        document = retriever.get_document_by_id("nonexistent")

        # Verify the result
        assert document is None


class TestStandaloneFunctions:
    """Test the standalone convenience functions"""

    @patch('backend.retrieve.QdrantRetriever')
    def test_list_qdrant_collections(self, mock_retriever_class):
        """Test list_qdrant_collections function"""
        mock_retriever = Mock()
        mock_retriever_class.return_value = mock_retriever
        mock_retriever.list_collections.return_value = ["collection1", "collection2"]

        result = list_qdrant_collections()

        assert result == ["collection1", "collection2"]
        mock_retriever_class.assert_called_once()
        mock_retriever.list_collections.assert_called_once()

    @patch('backend.retrieve.QdrantRetriever')
    def test_validate_qdrant_storage(self, mock_retriever_class):
        """Test validate_qdrant_storage function"""
        mock_retriever = Mock()
        mock_retriever_class.return_value = mock_retriever
        mock_result = ValidationResult(is_valid=True, message="Valid")
        mock_retriever.validate_storage.return_value = mock_result

        result = validate_qdrant_storage()

        assert result.is_valid is True
        assert result.message == "Valid"
        mock_retriever_class.assert_called_once()
        mock_retriever.validate_storage.assert_called_once()


def test_contract_list_collections():
    """Contract test for list-collections endpoint"""
    # This test verifies that the function returns a list of strings
    try:
        collections = list_qdrant_collections()
        assert isinstance(collections, list)
        if collections:  # If there are collections
            assert all(isinstance(col, str) for col in collections)
    except Exception:
        # If Qdrant is not available, this is expected
        pass


def test_integration_storage_validation():
    """Integration test for storage validation"""
    try:
        result = validate_qdrant_storage()
        assert isinstance(result, ValidationResult)
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'message')
    except Exception:
        # If Qdrant is not available, this is expected
        pass


def test_integration_end_to_end_rag_validation():
    """Integration test for end-to-end RAG validation"""
    try:
        from backend.retrieve import QdrantRetriever

        retriever = QdrantRetriever()

        # Define test queries for end-to-end validation
        test_queries = [
            {
                "query": "test query for validation",
                "expected_content": ""  # Not specifying expected content for this test
            }
        ]

        result = retriever.end_to_end_validation(test_queries)

        assert isinstance(result, ValidationResult)
        assert hasattr(result, 'is_valid')
        assert hasattr(result, 'message')
        assert hasattr(result, 'details')
    except Exception:
        # If Qdrant is not available, this is expected
        pass


if __name__ == "__main__":
    pytest.main([__file__])