from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_qdrant_connection():
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        timeout=30
    )

    print(f"Attempting to connect to: {os.getenv('QDRANT_URL')}")

    collection_name = "test_collection"

    # Create collection
    try:
        client.delete_collection(collection_name)
        print(f"Deleted existing collection '{collection_name}'")
    except:
        pass  # Collection doesn't exist, which is fine

    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)  # Cohere default
    )
    print(f"Created collection '{collection_name}'")

    # Upload dummy points
    points = [
        models.PointStruct(
            id=1,
            vector=[float(i) for i in range(1536)],  # Dummy 1536-dim vector
            payload={"text": "Test document 1", "source": "test"}
        ),
        models.PointStruct(
            id=2,
            vector=[float(i * 0.5) for i in range(1536)],  # Different dummy vector
            payload={"text": "Test document 2", "source": "test"}
        ),
        models.PointStruct(
            id=uuid.uuid4().int & (1<<63)-1,  # Large random ID
            vector=[1.0] * 1536,  # All 1s vector
            payload={"text": "Test document 3", "source": "test"}
        )
    ]

    # Upsert with wait=True for immediate consistency
    result = client.upsert(
        collection_name=collection_name,
        points=points,
        wait=True
    )
    print(f"Upserted {len(points)} points with wait=True")

    # Verify points were added
    collection_info = client.get_collection(collection_name)
    print(f"Collection points count: {collection_info.points_count}")

    # Retrieve points to verify
    retrieved_points, _ = client.scroll(
        collection_name=collection_name,
        limit=10,
        with_payload=True,
        with_vectors=False
    )

    print(f"Retrieved {len(retrieved_points)} points:")
    for point in retrieved_points:
        print(f"  ID: {point.id}, Payload: {point.payload}")

    print(f"\n✅ Test completed! Check Qdrant Cloud dashboard for collection '{collection_name}'")

if __name__ == "__main__":
    test_qdrant_connection()