import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

from qdrant_client import QdrantClient
from qdrant_client.http import models
from cohere import Client as CohereClient
import uuid

# Use the same connection logic as agent.py
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_host = os.getenv("QDRANT_HOST", "localhost")
qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_embedding")

# Try different connection methods in order of preference
qdrant_client = None

if qdrant_url:
    try:
        qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            prefer_grpc=False,
            timeout=5,  # Shorter timeout to fail faster
            https=True
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

# Check collection info
try:
    collection_info = qdrant_client.get_collection(COLLECTION_NAME)
    print(f"Collection '{COLLECTION_NAME}' exists with {collection_info.points_count} points")
except Exception as e:
    print(f"Collection '{COLLECTION_NAME}' does not exist: {e}")
    exit()

# Count the actual points in the collection
count_result = qdrant_client.count(
    collection_name=COLLECTION_NAME
)
print(f"Actual count of points in collection: {count_result.count}")

# Sample a few points to see what's stored
try:
    records, _ = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        limit=3,  # Get first 3 records
    )

    print("\nSample records from the collection:")
    for i, record in enumerate(records):  # Updated for newer Qdrant client
        print(f"Record {i+1}:")
        print(f"  ID: {record.id}")
        print(f"  Payload keys: {list(record.payload.keys()) if isinstance(record.payload, dict) else 'N/A'}")
        if isinstance(record.payload, dict):
            content_preview = record.payload.get('content', '')[:100] + "..." if len(record.payload.get('content', '')) > 100 else record.payload.get('content', '')
            print(f"  Content preview: {content_preview}")
        print()

except Exception as e:
    print(f"Error sampling records: {e}")

# Test embedding and search with a simple query
try:
    cohere_client = CohereClient(api_key=os.getenv("COHERE_API_KEY"))

    # Test embedding
    test_query = "Physical AI concepts"
    embedding_response = cohere_client.embed(
        texts=[test_query],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    query_embedding = embedding_response.embeddings[0]

    print(f"Generated embedding for query: '{test_query}'")

    # Test search - use query_points if search is not available, or handle differently
    try:
        # Try the newer search method first
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=5,
            with_payload=True
        )
    except AttributeError:
        # Fall back to older method if needed
        search_results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=5,
            with_payload=True
        ).points

    print(f"Search returned {len(search_results)} results")

    for i, result in enumerate(search_results):
        print(f"Result {i+1}:")
        print(f"  Score: {result.score}")
        print(f"  ID: {result.id}")
        if isinstance(result.payload, dict):
            content_preview = result.payload.get('content', '')[:100] + "..." if len(result.payload.get('content', '')) > 100 else result.payload.get('content', '')
            print(f"  Content preview: {content_preview}")
        print()

except Exception as e:
    print(f"Error testing search: {e}")