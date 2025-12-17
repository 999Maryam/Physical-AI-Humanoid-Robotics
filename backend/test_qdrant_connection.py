#!/usr/bin/env python3
"""
Test script to verify Qdrant connection and vector insertion
"""

import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import uuid

# Your configuration
QDRANT_URL = "https://07f4497d-1e9d-4314-8c2e-9a8531849b2e.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.XWV3j9oNNhhAnewQbg5AbZhHV_2tRm-zJ5uqC0aWySQ"
COLLECTION_NAME = "rag_embedding"

def test_qdrant_connection():
    """Test Qdrant connection and perform basic operations"""
    print("Testing Qdrant Connection...")
    print(f"URL: {QDRANT_URL}")
    print(f"Collection: {COLLECTION_NAME}")

    try:
        # Initialize client
        client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            prefer_grpc=True
        )

        print("[SUCCESS] Successfully connected to Qdrant")

        # Test 1: Get list of collections
        print("\n1. Checking existing collections...")
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]
        print(f"Existing collections: {collection_names}")

        # Check if our collection exists
        collection_exists = COLLECTION_NAME in collection_names
        print(f"Target collection '{COLLECTION_NAME}' exists: {collection_exists}")

        if not collection_exists:
            print(f"\n2. Creating collection '{COLLECTION_NAME}'...")
            # Create collection with appropriate vector size for Cohere embeddings (1024 dimensions)
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )
            print(f"[SUCCESS] Collection '{COLLECTION_NAME}' created successfully")
        else:
            print(f"\n2. Collection '{COLLECTION_NAME}' already exists, checking its configuration...")
            collection_info = client.get_collection(COLLECTION_NAME)
            vector_size = collection_info.config.params.vectors.size
            print(f"Collection vector size: {vector_size}")

            # If vector size is not 1024 (expected for Cohere), we might have a mismatch
            if vector_size != 1024:
                print(f"⚠️  WARNING: Vector size is {vector_size}, expected 1024 for Cohere embeddings")

        # Test 3: Insert a test vector
        print(f"\n3. Testing vector insertion...")

        # Create a test embedding (1024-dimensional vector for Cohere compatibility)
        test_embedding = [0.1] * 1024  # Simple test vector

        # Create a test point
        test_point = models.PointStruct(
            id=str(uuid.uuid4()),  # Generate unique ID
            vector=test_embedding,
            payload={
                "content": "This is a test document for Qdrant verification",
                "source_url": "test://verification",
                "document_title": "Test Document",
                "chunk_index": 0,
                "token_count": 10
            }
        )

        # Insert the point
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[test_point]
        )

        print(f"[SUCCESS] Successfully inserted test vector with ID: {test_point.id}")

        # Test 4: Verify the insertion by counting points
        collection_info = client.get_collection(COLLECTION_NAME)
        points_count = collection_info.points_count
        print(f"[SUCCESS] Collection now has {points_count} points")

        # Test 5: Perform a simple search to verify the vector is queryable
        print(f"\n4. Testing vector search...")
        search_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=test_embedding,
            limit=1
        )

        if search_results:
            result = search_results[0]
            print(f"[SUCCESS] Successfully found vector in search: ID={result.id}, Score={result.score}")
            print(f"  Payload content: {result.payload.get('content', 'N/A')[:50]}...")
        else:
            print("[WARNING] No results found in search - vector might not be properly indexed")

        print(f"\n[SUCCESS] All tests completed successfully! Your Qdrant configuration is working.")
        return True

    except Exception as e:
        print(f"[ERROR] Error during Qdrant testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_different_dimensions():
    """Test with different common embedding dimensions"""
    print(f"\n--- Testing with different vector dimensions ---")

    common_dimensions = [384, 512, 768, 1024, 1536]  # Common embedding sizes

    for dim in common_dimensions:
        print(f"\nTesting with dimension {dim}...")
        try:
            client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY,
                prefer_grpc=True
            )

            # Create a temporary test collection
            temp_collection = f"test_collection_{dim}"

            # Check if it exists and create if needed
            collections = client.get_collections()
            if temp_collection not in [col.name for col in collections.collections]:
                client.create_collection(
                    collection_name=temp_collection,
                    vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
                )
                print(f"[SUCCESS] Created temporary collection with {dim} dimensions")

            # Test insertion
            test_embedding = [0.1] * dim
            test_point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=test_embedding,
                payload={"test": f"dimension_test_{dim}"}
            )

            client.upsert(
                collection_name=temp_collection,
                points=[test_point]
            )

            print(f"[SUCCESS] Successfully inserted vector with {dim} dimensions")

            # Clean up - delete the temporary collection
            client.delete_collection(temp_collection)

        except Exception as e:
            print(f"[ERROR] Failed with dimension {dim}: {e}")

if __name__ == "__main__":
    print("Qdrant Connection and Insertion Test")
    print("=" * 50)

    success = test_qdrant_connection()

    if not success:
        print(f"\n--- Retrying with different dimensions ---")
        test_with_different_dimensions()

    print("\n" + "=" * 50)
    print("Test completed. Check the results above for any issues.")