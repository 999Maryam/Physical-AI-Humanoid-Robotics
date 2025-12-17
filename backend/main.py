import logging
import sys
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Handle imports for both direct execution and module execution
try:
    # When running as part of the backend package
    from backend import config
    from backend.models import Document, QueryResult, RetrievalRequest, RetrievalResponse, ValidationResult, DocumentChunk
    from backend.retrieve import QdrantRetriever, list_qdrant_collections, validate_qdrant_storage, search_qdrant
except ImportError:
    # When running directly from backend directory
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import config
    from models import Document, QueryResult, RetrievalRequest, RetrievalResponse, ValidationResult, DocumentChunk
    from retrieve import QdrantRetriever, list_qdrant_collections, validate_qdrant_storage, search_qdrant
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time
from typing import List, Set
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import argparse
import uuid


# =========================
# URL NORMALIZATION (FIX)
# =========================
def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    return urlunparse(parsed._replace(fragment=""))


def create_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("rag_ingestion.log"),
        ],
    )


# =========================
# CRAWLER (FIXED)
# =========================
def get_all_urls(base_url: str) -> List[str]:
    logger = logging.getLogger(__name__)
    logger.info(f"Starting to crawl: {base_url}")

    visited_urls: Set[str] = set()
    urls_to_visit: List[str] = [normalize_url(base_url)]
    all_urls: List[str] = []

    base_domain = urlparse(base_url).netloc
    session = create_session_with_retries()

    while urls_to_visit:
        current_url = normalize_url(urls_to_visit.pop(0))

        if "/en/" in current_url:
            continue

        if current_url.endswith("/docs/intro") or current_url.endswith("/ur/docs/intro"):
            continue


        if current_url in visited_urls:
            continue

        if urlparse(current_url).netloc != base_domain:
            continue

        try:
            time.sleep(60.0 / config.Config.REQUESTS_PER_MINUTE)

            response = session.get(current_url, timeout=10)
            response.raise_for_status()

            visited_urls.add(current_url)
            all_urls.append(current_url)
            logger.info(f"Successfully crawled: {current_url}")

            soup = BeautifulSoup(response.content, "html.parser")

            for link in soup.find_all("a", href=True):
                href = link["href"]
                absolute_url = normalize_url(urljoin(current_url, href))

                if (
                    urlparse(absolute_url).netloc == base_domain
                    and absolute_url not in visited_urls
                    and absolute_url not in urls_to_visit
                ):
                    urls_to_visit.append(absolute_url)

        except requests.RequestException as e:
            logger.error(f"Failed to crawl {current_url}: {e}")

    logger.info(f"Crawling completed. Found {len(all_urls)} URLs.")
    return all_urls


# =========================
# EXTRACTION
# =========================
def extract_text_from_url(url: str) -> dict:
    logger = logging.getLogger(__name__)
    session = create_session_with_retries()

    time.sleep(60.0 / config.Config.REQUESTS_PER_MINUTE)
    response = session.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    title = soup.title.get_text(strip=True) if soup.title else ""

    main_content = soup.find("main") or soup.find("article") or soup.find("body")
    text = main_content.get_text(separator=" ", strip=True)

    cleaned_text = utils.clean_text(text)

    return {
        "url": url,
        "title": title,
        "content": cleaned_text,
        "word_count": len(cleaned_text.split()),
    }


def chunk_text(text: str, chunk_size: int, overlap: int):
    return utils.chunk_text(text, chunk_size, overlap)


def embed(texts: List[str]):
    from services.embedding_service import EmbeddingService
    return EmbeddingService().embed_texts(texts)


def create_collection():
    from services.vector_service import VectorService
    return VectorService().create_collection()


def save_chunk_to_qdrant(chunk: DocumentChunk):
    from services.vector_service import VectorService
    return VectorService().save_chunk_to_qdrant(
        embedding=chunk.embedding,
        metadata={
            "content": chunk.content,
            "source_url": chunk.source_url,
            "document_title": chunk.document_title,
            "chunk_index": chunk.chunk_index,
            "token_count": chunk.token_count,
        },
        chunk_id=chunk.id,
    )


# =========================
# FASTAPI APPLICATION
# =========================
app = FastAPI(
    title="RAG Data Retrieval API",
    description="API for testing RAG pipeline data retrieval from Qdrant",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "RAG Data Retrieval API is running"}


@app.get("/api/list-collections", response_model=List[str])
async def api_list_collections():
    """
    List all available Qdrant collections.
    """
    try:
        collections = list_qdrant_collections()
        return collections
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing collections: {str(e)}")


@app.get("/api/validate-storage", response_model=ValidationResult)
async def api_validate_storage():
    """
    Validate that documents are properly stored in Qdrant with embeddings.
    """
    try:
        result = validate_qdrant_storage()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage validation failed: {str(e)}")


@app.post("/api/retrieve", response_model=RetrievalResponse)
async def api_retrieve(request: RetrievalRequest):
    """
    Perform similarity search in Qdrant to retrieve relevant documents.
    """
    try:
        start_time = __import__('time').time()
        results = search_qdrant(
            query_text=request.query_text,
            top_k=request.top_k,
            collection_name=request.collection_name,
            min_score=request.min_score
        )
        end_time = __import__('time').time()

        response = RetrievalResponse(
            query=request.query_text,
            results=results,
            total_count=len(results),
            execution_time=end_time - start_time
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")


# =========================
# MAIN
# =========================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=config.Config.TARGET_URL)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--chunk-size", type=int, default=config.Config.CHUNK_SIZE)
    parser.add_argument("--chunk-overlap", type=int, default=config.Config.CHUNK_OVERLAP)
    parser.add_argument("--store", action="store_true")
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("RAG Ingestion Pipeline started")

    urls = get_all_urls(args.url)
    urls = urls[: args.limit]

    all_chunks = []

    for url in urls:
        data = extract_text_from_url(url)

        if data["word_count"] < 100:
            continue

        chunks = chunk_text(
            data["content"], args.chunk_size, args.chunk_overlap
        )

        for idx, text in enumerate(chunks):
            all_chunks.append(
                DocumentChunk(
                    id=str(uuid.uuid4()),
                    content=text,
                    source_url=data["url"],
                    chunk_index=idx,
                    document_title=data["title"],
                    token_count=utils.count_tokens(text),
                )
            )

    if not all_chunks:
        return

    embeddings = embed([c.content for c in all_chunks])

    # Log embedding information for debugging
    logger.info(f"Generated {len(embeddings)} embeddings")
    if embeddings and len(embeddings) > 0:
        logger.info(f"First embedding length: {len(embeddings[0]) if embeddings[0] else 0}")
        logger.info(f"First embedding sample: {embeddings[0][:5] if embeddings[0] else []}")

    for c, e in zip(all_chunks, embeddings):
        c.embedding = e

    if args.store:
        logger.info("Store flag detected, creating collection and saving to Qdrant")
        create_collection()
        for idx, c in enumerate(all_chunks):
            try:
                logger.info(f"Saving chunk {idx+1}/{len(all_chunks)} to Qdrant with embedding length: {len(c.embedding) if c.embedding else 0}")
                save_chunk_to_qdrant(c)
                logger.info(f"Successfully saved chunk {idx+1} to Qdrant")
            except Exception as e:
                logger.error(f"Failed to save chunk {idx+1} to Qdrant: {e}")
                raise
    else:
        logger.info("Store flag not set, skipping Qdrant insertion")

    print(f"✅ Done. Clean chunks stored: {len(all_chunks)}")


if __name__ == "__main__":
    main()
