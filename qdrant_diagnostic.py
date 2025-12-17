from qdrant_client import QdrantClient
from qdrant_client.http import models
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize client
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=30  # Increased timeout
)

print(f"Attempting to connect to: {os.getenv('QDRANT_URL')}")

# 1. Check collection info
collection_name = "rag_embedding"
try:
    collection_info = client.get_collection(collection_name)
    print(f"Collection '{collection_name}' exists")
    print(f"Points count: {collection_info.points_count}")
    print(f"Config: {collection_info.config}")
    print(f"Vectors count: {collection_info.vectors_count}")
except Exception as e:
    print(f"Collection '{collection_name}' not found or connection issue: {e}")

# 2. List all collections
try:
    collections = client.get_collections()
    print("\nAll collections:")
    for collection in collections.collections:
        print(f"- {collection.name}: {collection.point_count} points")
except Exception as e:
    print(f"Cannot list collections - connection failed: {e}")

print("\nConnection test completed.")