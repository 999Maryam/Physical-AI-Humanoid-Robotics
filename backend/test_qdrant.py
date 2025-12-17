#!/usr/bin/env python3
"""Test script to check Qdrant client method availability"""

import os
from qdrant_client import QdrantClient

# Test the exact same initialization as in agent.py
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_host = os.getenv("QDRANT_HOST", "localhost")
qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))

print(f"QDRANT_URL: {qdrant_url}")
print(f"QDRANT_HOST: {qdrant_host}")
print(f"QDRANT_PORT: {qdrant_port}")

# Initialize client based on configuration
if qdrant_url:
    print("Using URL-based initialization")
    qdrant_client = QdrantClient(
        url=qdrant_url,
        api_key=qdrant_api_key,
        prefer_grpc=True
    )
else:
    print("Using host/port-based initialization")
    qdrant_client = QdrantClient(
        host=qdrant_host,
        port=qdrant_port,
        api_key=qdrant_api_key
    )

print(f"Client type: {type(qdrant_client)}")
print(f"query_points method exists: {hasattr(qdrant_client, 'query_points')}")
print(f"search method exists: {hasattr(qdrant_client, 'search')}")

# List some available methods
methods = [method for method in dir(qdrant_client) if not method.startswith('_') and 'query' in method.lower()]
print(f"Query-related methods: {methods}")