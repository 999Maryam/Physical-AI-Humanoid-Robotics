"""Vector service for RAG Ingestion Pipeline using Qdrant."""

import uuid
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from exceptions import VectorStorageError


class VectorService:
    """Service class for handling vector storage with Qdrant."""

    def __init__(self):
        """Initialize the vector service with Qdrant client."""
        url = Config.QDRANT_URL
        api_key = Config.QDRANT_API_KEY

        if not url:
            raise ValueError("QDRANT_URL environment variable is required")
        if not api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")

        self.client = QdrantClient(
            url=url,
            api_key=api_key,
            prefer_grpc=True
        )
        self.collection_name = Config.COLLECTION_NAME

    def create_collection(self, vector_size: int = 1024) -> bool:
        """
        Create a collection in Qdrant for storing embeddings.

        Args:
            vector_size (int): Size of the embedding vectors

        Returns:
            bool: True if collection was created or already exists
        """
        import logging
        logger = logging.getLogger(__name__)

        try:
            logger.info(f"Attempting to create or verify collection: {self.collection_name}")
            logger.info(f"Qdrant URL: {Config.QDRANT_URL}")

            # Check if collection already exists
            collections = self.client.get_collections()
            existing_collection = None
            for collection in collections.collections:
                if collection.name == self.collection_name:
                    existing_collection = collection
                    break

            if existing_collection:
                logger.info(f"Collection '{self.collection_name}' already exists")
                print(f"Collection '{self.collection_name}' already exists")
                return True

            # Create new collection
            logger.info(f"Creating new collection '{self.collection_name}' with vector size {vector_size}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")
            print(f"Collection '{self.collection_name}' created successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise VectorStorageError(f"Failed to create collection: {e}")

    def save_chunk_to_qdrant(self, embedding: List[float], metadata: Dict[str, Any], chunk_id: Optional[str] = None) -> str:
        """
        Save a chunk with its embedding to Qdrant.

        Args:
            embedding (List[float]): The embedding vector
            metadata (Dict[str, Any]): Metadata associated with the chunk
            chunk_id (Optional[str]): Optional chunk ID, will be generated if not provided

        Returns:
            str: The ID of the saved point
        """
        import logging
        logger = logging.getLogger(__name__)

        try:
            logger.debug(f"Attempting to save chunk to Qdrant with embedding length: {len(embedding) if embedding else 0}")

            if chunk_id is None:
                chunk_id = str(uuid.uuid4())
                logger.debug(f"Generated new chunk ID: {chunk_id}")

            # Prepare the point to be inserted
            point = models.PointStruct(
                id=chunk_id,
                vector=embedding,
                payload=metadata
            )

            logger.debug(f"Prepared point for insertion: ID={chunk_id}, vector length={len(embedding) if embedding else 0}")

            # Insert the point into the collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            logger.info(f"Successfully saved chunk to Qdrant: ID={chunk_id}")
            return chunk_id

        except Exception as e:
            logger.error(f"Failed to save chunk to Qdrant: {e}")
            raise VectorStorageError(f"Failed to save chunk to Qdrant: {e}")

    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in Qdrant.

        Args:
            query_embedding (List[float]): The query embedding vector
            top_k (int): Number of similar results to return

        Returns:
            List[Dict[str, Any]]: List of similar results with metadata
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )

            # Format results to include content and metadata
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "content": result.payload.get("content", ""),
                    "source_url": result.payload.get("source_url", ""),
                    "document_title": result.payload.get("document_title", "")
                })

            return formatted_results

        except Exception as e:
            raise VectorStorageError(f"Failed to search similar vectors: {e}")

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.

        Returns:
            Dict[str, Any]: Collection information
        """
        try:
            collection_info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vector_size": collection_info.config.params.vectors.size,
                "points_count": collection_info.points_count,
                "indexed_vectors_count": collection_info.points_count  # Fixed typo: was collection.points_count
            }
        except Exception as e:
            raise VectorStorageError(f"Failed to get collection info: {e}")