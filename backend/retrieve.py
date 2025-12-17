"""
RAG Data Retrieval Testing Module

This module provides functionality for AI engineers to validate that the RAG
ingestion and retrieval pipeline works correctly by connecting to Qdrant and
testing data storage and retrieval.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import logging
try:
    # When running as part of the backend package
    from backend.models import Document, QueryResult, RetrievalRequest, RetrievalResponse, ValidationResult
except ImportError:
    # When running directly from backend directory
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from models import Document, QueryResult, RetrievalRequest, RetrievalResponse, ValidationResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QdrantRetriever:
    """
    Main class for retrieving data from Qdrant for testing purposes.
    Provides methods to validate storage, perform similarity searches,
    and inspect stored content.
    """

    def __init__(self):
        """Initialize the QdrantRetriever with configuration"""
        # We'll implement the actual Qdrant client initialization here
        # For now, we'll create a placeholder that will be updated later
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the Qdrant client with configuration"""
        try:
            from qdrant_client import QdrantClient
            try:
                # When running as part of the backend package
                from backend.config import Config
            except ImportError:
                # When running directly from backend directory
                import sys
                import os
                sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                from config import Config

            # Get Qdrant configuration from config
            qdrant_url = Config.QDRANT_URL
            qdrant_api_key = Config.QDRANT_API_KEY
            qdrant_host = Config.QDRANT_HOST
            qdrant_port = Config.QDRANT_PORT

            # Initialize client based on configuration
            if qdrant_url:
                self.client = QdrantClient(
                    url=qdrant_url,
                    api_key=qdrant_api_key,
                    prefer_grpc=True
                )
            else:
                self.client = QdrantClient(
                    host=qdrant_host,
                    port=qdrant_port,
                    api_key=qdrant_api_key
                )

            logger.info(f"Qdrant client initialized successfully with host: {qdrant_host}")

        except ImportError:
            logger.error("qdrant-client library not found. Please install it using 'pip install qdrant-client'")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {str(e)}")
            raise

    def list_collections(self) -> List[str]:
        """
        List all available Qdrant collections.

        Returns:
            List of collection names
        """
        try:
            collections = self.client.get_collections()
            collection_names = [collection.name for collection in collections.collections]
            logger.info(f"Found {len(collection_names)} collections: {collection_names}")
            return collection_names
        except Exception as e:
            logger.error(f"Error listing collections: {str(e)}")
            raise

    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        Get statistics for a specific collection.

        Args:
            collection_name: Name of the collection to get stats for

        Returns:
            Dictionary with collection statistics
        """
        try:
            collection_info = self.client.get_collection(collection_name)
            # Check if the collection has vector configuration
            vector_config = collection_info.config.params.vectors
            vector_dim = None
            if vector_config:
                # Handle both single vector and multiple named vectors configurations
                if hasattr(vector_config, 'size'):  # Single vector configuration
                    vector_dim = vector_config.size
                elif hasattr(vector_config, 'get'):  # Multiple named vectors configuration
                    # Get the first vector configuration's size
                    if hasattr(vector_config, '__iter__') or hasattr(vector_config, 'keys'):
                        # If it's a dict-like object, get first vector's size
                        if hasattr(vector_config, 'keys'):
                            first_key = next(iter(vector_config.keys()))
                            vector_dim = vector_config[first_key].size if hasattr(vector_config[first_key], 'size') else None
                        else:
                            # If it's not dict-like, try to access the first vector config
                            try:
                                first_config = list(vector_config.values())[0] if hasattr(vector_config, 'values') else None
                                vector_dim = first_config.size if hasattr(first_config, 'size') else None
                            except:
                                vector_dim = None
                    else:
                        vector_dim = None

            stats = {
                "total_points": collection_info.points_count,
                "vector_dim": vector_dim,
                "collection_name": collection_name
            }
            logger.info(f"Retrieved stats for collection '{collection_name}': {stats}")
            return stats
        except Exception as e:
            logger.error(f"Error getting collection stats for '{collection_name}': {str(e)}")
            raise

    def validate_storage(self) -> ValidationResult:
        """
        Validate that documents are properly stored in Qdrant with embeddings.

        Returns:
            ValidationResult indicating whether storage is valid
        """
        try:
            collections = self.list_collections()
            if not collections:
                return ValidationResult(
                    is_valid=False,
                    message="No collections found in Qdrant - ingestion may have failed"
                )

            total_points = 0
            for collection_name in collections:
                stats = self.get_collection_stats(collection_name)
                total_points += stats["total_points"]

            if total_points == 0:
                return ValidationResult(
                    is_valid=False,
                    message="Collections exist but contain no points - ingestion may have failed"
                )

            return ValidationResult(
                is_valid=True,
                message=f"Storage validation passed: {len(collections)} collections with {total_points} total points",
                details={
                    "collection_count": len(collections),
                    "total_points": total_points,
                    "collections": collections
                }
            )
        except Exception as e:
            logger.error(f"Error during storage validation: {str(e)}")
            return ValidationResult(
                is_valid=False,
                message=f"Storage validation failed: {str(e)}"
            )

    def search(self, query_text: str, top_k: int = None, collection_name: str = None,
               min_score: Optional[float] = None) -> List[QueryResult]:
        """
        Perform similarity search in Qdrant.

        Args:
            query_text: Text to search for similar documents
            top_k: Number of results to return (uses config default if None)
            collection_name: Name of Qdrant collection to search in (uses default if None)
            min_score: Minimum relevance score threshold (uses config default if None)

        Returns:
            List of QueryResult objects
        """
        try:
            from sentence_transformers import SentenceTransformer
            try:
                # When running as part of the backend package
                from backend.config import Config
            except ImportError:
                # When running directly from backend directory
                import sys
                import os
                sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                from config import Config

            # Use defaults from config if not provided
            if top_k is None:
                top_k = Config.DEFAULT_RETRIEVAL_TOP_K
            if collection_name is None:
                collection_name = Config.COLLECTION_NAME
            if min_score is None and min_score != 0.0:  # Allow 0.0 as a valid value
                min_score = Config.DEFAULT_MIN_SCORE

            # Initialize embedding model for query
            # In a real implementation, you'd want to use the same model used for ingestion
            model = SentenceTransformer('all-MiniLM-L6-v2')
            query_embedding = model.encode([query_text])[0].tolist()

            # Perform search
            search_results = self.client.search(
                collection_name=collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True,
                with_vectors=False
            )

            # Convert results to QueryResult objects
            results = []
            for i, hit in enumerate(search_results):
                # Extract content and metadata from payload
                payload = hit.payload or {}
                content = payload.get("content", "")
                metadata = {k: v for k, v in payload.items() if k != "content"}  # Exclude content from metadata

                # Apply minimum score filter if specified
                if min_score is not None and hit.score < min_score:
                    continue

                result = QueryResult(
                    id=hit.id,
                    content=content,
                    score=hit.score,
                    metadata=metadata,
                    position=i
                )
                results.append(result)

            logger.info(f"Search completed for query '{query_text[:50]}...', found {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            raise

    def get_document_by_id(self, doc_id: str, collection_name: str = "documents") -> Optional[Document]:
        """
        Retrieve a specific document by its ID.

        Args:
            doc_id: ID of the document to retrieve
            collection_name: Name of the collection to search in

        Returns:
            Document object or None if not found
        """
        try:
            records = self.client.retrieve(
                collection_name=collection_name,
                ids=[doc_id],
                with_payload=True,
                with_vectors=True
            )

            if not records:
                logger.info(f"No document found with ID: {doc_id}")
                return None

            record = records[0]
            payload = record.payload or {}
            content = payload.get("content", "")
            metadata = {k: v for k, v in payload.items() if k != "content"}

            document = Document(
                id=record.id,
                content=content,
                metadata=metadata,
                embedding=record.vector if record.vector else [],
                collection_name=collection_name
            )

            logger.info(f"Retrieved document with ID: {doc_id}")
            return document

        except Exception as e:
            logger.error(f"Error retrieving document with ID {doc_id}: {str(e)}")
            raise

    def get_random_sample(self, collection_name: str = "documents", sample_size: int = 5) -> List[Document]:
        """
        Get a random sample of documents from a collection for inspection.

        Args:
            collection_name: Name of the collection to sample from
            sample_size: Number of documents to sample

        Returns:
            List of Document objects
        """
        try:
            # Use scroll to get random samples without knowing the IDs
            scroll_result, _ = self.client.scroll(
                collection_name=collection_name,
                limit=sample_size,
                with_payload=True,
                with_vectors=False
            )

            documents = []
            for record in scroll_result:
                payload = record.payload or {}
                content = payload.get("content", "")
                metadata = {k: v for k, v in payload.items() if k != "content"}

                document = Document(
                    id=str(record.id),  # Ensure ID is a string
                    content=content,
                    metadata=metadata,
                    embedding=[],
                    collection_name=collection_name
                )
                documents.append(document)

            logger.info(f"Retrieved sample of {len(documents)} documents from collection '{collection_name}'")
            return documents

        except Exception as e:
            logger.error(f"Error getting sample from collection '{collection_name}': {str(e)}")
            # Fallback to using scroll with offset if direct scroll fails
            try:
                # Get all IDs using scroll
                all_records, _ = self.client.scroll(
                    collection_name=collection_name,
                    with_payload=False,
                    with_vectors=False
                )

                if not all_records:
                    return []

                # Sample from the available IDs
                import random
                sample_records = random.sample(all_records, min(sample_size, len(all_records)))
                sample_ids = [str(record.id) for record in sample_records]

                # Retrieve the full records
                records = self.client.retrieve(
                    collection_name=collection_name,
                    ids=sample_ids,
                    with_payload=True,
                    with_vectors=False
                )

                documents = []
                for record in records:
                    payload = record.payload or {}
                    content = payload.get("content", "")
                    metadata = {k: v for k, v in payload.items() if k != "content"}

                    document = Document(
                        id=str(record.id),
                        content=content,
                        metadata=metadata,
                        embedding=[],
                        collection_name=collection_name
                    )
                    documents.append(document)

                logger.info(f"Retrieved sample of {len(documents)} documents from collection '{collection_name}' using fallback method")
                return documents
            except Exception as fallback_e:
                logger.error(f"Fallback method also failed: {str(fallback_e)}")
                raise

    def end_to_end_validation(self, test_queries: List[Dict[str, str]],
                              expected_sources: List[str] = None) -> ValidationResult:
        """
        Perform end-to-end validation of the RAG pipeline.

        Args:
            test_queries: List of dictionaries with 'query' and 'expected_content' keys
            expected_sources: Optional list of expected source documents

        Returns:
            ValidationResult indicating the success of the end-to-end test
        """
        try:
            import time
            validation_results = []

            for i, test_query in enumerate(test_queries):
                query_text = test_query.get("query", "")
                expected_content = test_query.get("expected_content", "")

                if not query_text:
                    continue

                # Perform search
                start_time = time.time()
                results = self.search(query_text)
                end_time = time.time()

                # Check if expected content appears in results
                found_expected = False
                if expected_content:
                    for result in results:
                        if expected_content.lower() in result.content.lower():
                            found_expected = True
                            break

                validation_results.append({
                    "query_index": i,
                    "query": query_text,
                    "result_count": len(results),
                    "found_expected": found_expected,
                    "response_time": end_time - start_time,
                    "top_score": results[0].score if results else 0.0
                })

            # Calculate overall validation result
            successful_queries = sum(1 for r in validation_results if r["found_expected"])
            total_queries = len(validation_results)
            success_rate = successful_queries / total_queries if total_queries > 0 else 0

            is_valid = success_rate >= 0.8  # Require 80% success rate

            message = f"End-to-end validation: {successful_queries}/{total_queries} queries successful ({success_rate*100:.1f}% success rate)"

            details = {
                "total_queries": total_queries,
                "successful_queries": successful_queries,
                "success_rate": success_rate,
                "validation_results": validation_results,
                "performance_metrics": {
                    "avg_response_time": sum(r["response_time"] for r in validation_results) / total_queries if total_queries > 0 else 0,
                    "min_response_time": min((r["response_time"] for r in validation_results), default=0),
                    "max_response_time": max((r["response_time"] for r in validation_results), default=0)
                }
            }

            logger.info(f"End-to-end validation completed: {message}")

            return ValidationResult(
                is_valid=is_valid,
                message=message,
                details=details
            )

        except Exception as e:
            logger.error(f"Error during end-to-end validation: {str(e)}")
            return ValidationResult(
                is_valid=False,
                message=f"End-to-end validation failed: {str(e)}"
            )

    def debug_inspect_content(self, collection_name: str = "documents",
                             content_filter: str = None) -> List[Dict[str, Any]]:
        """
        Debug utility to inspect stored content in Qdrant collections.

        Args:
            collection_name: Name of the collection to inspect
            content_filter: Optional substring to filter content by

        Returns:
            List of dictionaries with document information for debugging
        """
        try:
            # Get collection info
            collection_info = self.client.get_collection(collection_name)
            total_points = collection_info.points_count

            # Limit the number of points to inspect for performance
            inspect_limit = min(total_points, 100)

            # Sample points to inspect
            import random
            if total_points <= inspect_limit:
                # If less than limit, inspect all
                ids_to_inspect = [str(i) for i in range(total_points)]
            else:
                # Otherwise, sample randomly
                sampled_indices = random.sample(range(total_points), inspect_limit)
                ids_to_inspect = [str(i) for i in sampled_indices]

            # Retrieve the sampled documents
            records = self.client.retrieve(
                collection_name=collection_name,
                ids=ids_to_inspect,
                with_payload=True,
                with_vectors=False
            )

            inspected_docs = []
            for record in records:
                payload = record.payload or {}
                content = payload.get("content", "")

                # Apply content filter if specified
                if content_filter and content_filter.lower() not in content.lower():
                    continue

                doc_info = {
                    "id": record.id,
                    "content_preview": content[:200] + "..." if len(content) > 200 else content,
                    "content_length": len(content),
                    "metadata": payload,
                    "has_embedding": bool(payload.get("has_embedding", True))  # Assuming all have embeddings
                }
                inspected_docs.append(doc_info)

            logger.info(f"Debug inspection completed for collection '{collection_name}': {len(inspected_docs)} documents inspected")
            return inspected_docs

        except Exception as e:
            logger.error(f"Error during debug inspection: {str(e)}")
            raise

    def measure_performance(self, test_queries: List[str], iterations: int = 5) -> Dict[str, Any]:
        """
        Measure performance of retrieval operations.

        Args:
            test_queries: List of queries to test
            iterations: Number of iterations to run for averaging

        Returns:
            Dictionary with performance metrics
        """
        try:
            import time
            import statistics

            all_times = []
            all_result_counts = []

            for _ in range(iterations):
                for query in test_queries:
                    start_time = time.time()
                    results = self.search(query, top_k=5)
                    end_time = time.time()

                    all_times.append(end_time - start_time)
                    all_result_counts.append(len(results))

            performance_metrics = {
                "avg_response_time": statistics.mean(all_times),
                "median_response_time": statistics.median(all_times),
                "min_response_time": min(all_times),
                "max_response_time": max(all_times),
                "std_dev_response_time": statistics.stdev(all_times) if len(all_times) > 1 else 0,
                "avg_results_count": statistics.mean(all_result_counts),
                "total_queries_processed": len(test_queries) * iterations,
                "throughput_queries_per_second": len(test_queries) * iterations / sum(all_times) if sum(all_times) > 0 else 0
            }

            logger.info(f"Performance measurement completed: avg response time {performance_metrics['avg_response_time']:.3f}s")
            return performance_metrics

        except Exception as e:
            logger.error(f"Error during performance measurement: {str(e)}")
            raise


    def run_command_line_interface(self):
        """
        Run a command-line interface for testing RAG functionality.
        """
        import argparse
        import json

        parser = argparse.ArgumentParser(description="RAG Data Retrieval Testing CLI")
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # List collections command
        list_parser = subparsers.add_parser("list-collections", help="List all Qdrant collections")

        # Validate storage command
        validate_parser = subparsers.add_parser("validate-storage", help="Validate storage integrity")

        # Search command
        search_parser = subparsers.add_parser("search", help="Perform similarity search")
        search_parser.add_argument("--query", required=True, help="Search query text")
        search_parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")
        search_parser.add_argument("--collection", default="documents", help="Collection to search in")
        search_parser.add_argument("--min-score", type=float, help="Minimum relevance score")

        # Get document command
        get_doc_parser = subparsers.add_parser("get-document", help="Get document by ID")
        get_doc_parser.add_argument("--id", required=True, help="Document ID")
        get_doc_parser.add_argument("--collection", default="documents", help="Collection to search in")

        # Debug inspect command
        debug_parser = subparsers.add_parser("debug-inspect", help="Debug content inspection")
        debug_parser.add_argument("--collection", default="documents", help="Collection to inspect")
        debug_parser.add_argument("--filter", help="Content filter string")

        # Performance test command
        perf_parser = subparsers.add_parser("perf-test", help="Performance testing")
        perf_parser.add_argument("--queries", nargs="+", required=True, help="Test queries")

        args = parser.parse_args()

        try:
            if args.command == "list-collections":
                collections = self.list_collections()
                print(json.dumps(collections, indent=2))

            elif args.command == "validate-storage":
                result = self.validate_storage()
                # Convert datetime objects to ISO format strings for JSON serialization
                result_dict = result.model_dump()
                if result_dict.get('timestamp') and hasattr(result_dict['timestamp'], 'isoformat'):
                    result_dict['timestamp'] = result_dict['timestamp'].isoformat()
                if result_dict.get('details') and isinstance(result_dict['details'], dict):
                    # Handle any datetime objects in the details
                    details = result_dict['details']
                    for key, value in details.items():
                        if hasattr(value, 'isoformat'):
                            details[key] = value.isoformat()
                print(json.dumps(result_dict, indent=2, default=str))

            elif args.command == "search":
                results = self.search(
                    query_text=args.query,
                    top_k=args.top_k,
                    collection_name=args.collection,
                    min_score=args.min_score
                )
                # Handle datetime serialization for search results
                results_data = []
                for result in results:
                    result_dict = result.model_dump()
                    results_data.append(result_dict)
                print(json.dumps(results_data, indent=2, default=str))

            elif args.command == "get-document":
                document = self.get_document_by_id(args.id, args.collection)
                if document:
                    # Handle datetime serialization for document
                    document_dict = document.model_dump()
                    print(json.dumps(document_dict, indent=2, default=str))
                else:
                    print(f"Document with ID {args.id} not found")

            elif args.command == "debug-inspect":
                docs = self.debug_inspect_content(args.collection, args.filter)
                print(json.dumps(docs, indent=2, default=str))

            elif args.command == "perf-test":
                metrics = self.measure_performance(args.queries)
                print(json.dumps(metrics, indent=2, default=str))

            else:
                parser.print_help()

        except Exception as e:
            print(f"Error executing command: {str(e)}")
            return 1

        return 0


# Standalone functions for direct usage
def list_qdrant_collections() -> List[str]:
    """Convenience function to list all collections"""
    retriever = QdrantRetriever()
    return retriever.list_collections()


def validate_qdrant_storage() -> ValidationResult:
    """Convenience function to validate storage"""
    retriever = QdrantRetriever()
    return retriever.validate_storage()


def search_qdrant(query_text: str, top_k: int = 5, collection_name: str = "documents",
                 min_score: Optional[float] = None) -> List[QueryResult]:
    """Convenience function to perform search"""
    retriever = QdrantRetriever()
    return retriever.search(query_text, top_k, collection_name, min_score)


def get_qdrant_document_by_id(doc_id: str, collection_name: str = "documents") -> Optional[Document]:
    """Convenience function to get document by ID"""
    retriever = QdrantRetriever()
    return retriever.get_document_by_id(doc_id, collection_name)


def run_cli():
    """
    Run the command-line interface for RAG testing.
    """
    try:
        retriever = QdrantRetriever()
        return retriever.run_command_line_interface()
    except Exception as e:
        print(f"Error initializing RAG tester: {str(e)}")
        return 1


if __name__ == "__main__":
    import sys
    # Check if running in CLI mode
    if len(sys.argv) > 1:
        # Run CLI mode
        exit_code = run_cli()
        sys.exit(exit_code)
    else:
        # Example usage
        print("RAG Data Retrieval Testing Module")
        print("==================================")

        try:
            retriever = QdrantRetriever()

            print("\n1. Listing collections:")
            collections = retriever.list_collections()
            print(f"   Found collections: {collections}")

            print("\n2. Validating storage:")
            validation_result = retriever.validate_storage()
            print(f"   Valid: {validation_result.is_valid}")
            print(f"   Message: {validation_result.message}")

            if validation_result.is_valid and collections:
                print(f"\n3. Getting stats for first collection '{collections[0]}':")
                stats = retriever.get_collection_stats(collections[0])
                print(f"   Stats: {stats}")

                print(f"\n4. Getting a sample of documents from '{collections[0]}':")
                sample_docs = retriever.get_random_sample(collections[0], 2)
                for i, doc in enumerate(sample_docs):
                    print(f"   Doc {i+1}: ID={doc.id}, Content preview: {doc.content[:100]}...")

        except Exception as e:
            print(f"Error during example execution: {str(e)}")