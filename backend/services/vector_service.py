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
        # Use the same connection logic as in agent.py
        qdrant_url = Config.QDRANT_URL
        qdrant_api_key = Config.QDRANT_API_KEY
        qdrant_host = Config.QDRANT_HOST
        qdrant_port = Config.QDRANT_PORT

        # Try different connection methods in order of preference
        qdrant_client = None

        if qdrant_url:
            try:
                qdrant_client = QdrantClient(
                    url=qdrant_url,
                    api_key=qdrant_api_key,
                    prefer_grpc=False,
                    timeout=5,  # Shorter timeout to fail faster
                    https=True  # Explicitly set https for cloud
                )
                # Test connection
                qdrant_client.get_collections()
                print("Connected to Qdrant Cloud")
            except Exception as e:
                print(f"Could not connect to Qdrant Cloud: {e}")
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
                print("Connected to local Qdrant")
            except Exception as e:
                print(f"Could not connect to local Qdrant: {e}")
                qdrant_client = None  # Explicitly set to None to trigger fallback

        if qdrant_client is None:
            # Fallback to in-memory Qdrant for development
            print("Using in-memory Qdrant for development")
            qdrant_client = QdrantClient(":memory:")

        self.client = qdrant_client
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

            # Generate a valid UUID if chunk_id is not provided or is invalid
            if chunk_id is None:
                point_id = str(uuid.uuid4())
            else:
                # If chunk_id is provided, try to use it, but generate a UUID if it's invalid
                try:
                    # Try to validate if it's a UUID
                    uuid.UUID(chunk_id)
                    point_id = chunk_id
                except ValueError:
                    # If it's not a valid UUID, generate a new one but keep the original as metadata
                    point_id = str(uuid.uuid4())
                    # Add the original chunk_id to metadata for reference
                    metadata['original_chunk_id'] = chunk_id

            logger.debug(f"Using point ID: {point_id}")

            # Prepare the point to be inserted
            point = models.PointStruct(
                id=point_id,
                vector=embedding,
                payload=metadata
            )

            logger.debug(f"Prepared point for insertion: ID={point_id}, vector length={len(embedding) if embedding else 0}")

            # Insert the point into the collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )

            logger.info(f"Successfully saved chunk to Qdrant: ID={point_id}")
            return point_id

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