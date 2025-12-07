import os
from qdrant_client import QdrantClient, models
from psycopg2 import connect
from dotenv import load_dotenv
from .embedding_service import EmbeddingService

load_dotenv()

class IngestionService:
    def __init__(self):
        self.qdrant_client = QdrantClient(host=os.getenv("QDRANT_HOST", "localhost"), port=int(os.getenv("QDRANT_PORT", 6333)))
        self.embedding_service = EmbeddingService()
        self.neon_conn_str = os.getenv("NEON_CONN_STR")

        # Ensure Qdrant collection exists
        self.collection_name = "textbook_content"
        try:
            self.qdrant_client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )
        except Exception as e:
            print(f"Could not recreate collection, it might already exist: {e}")

        # Initialize Neon DB schema (placeholder for actual schema)
        self._init_neon_db()

    def _init_neon_db(self):
        """Initializes the Neon database schema for storing content metadata."""
        with connect(self.neon_conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS chapters (
                        id VARCHAR(255) PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        content_path VARCHAR(255) NOT NULL,
                        chapter_order INTEGER NOT NULL
                    );
                """)
                conn.commit()

    def ingest_chapter(self, chapter_id: str, title: str, content_path: str, chapter_text: str, chapter_order: int):
        """Ingests a chapter's content into Qdrant and metadata into Neon."""
        # Generate embeddings
        embeddings = self.embedding_service.get_embeddings([chapter_text])[0] # Assuming one embedding per chapter for now

        # Store in Qdrant
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=chapter_id,
                    vector=embeddings,
                    payload={
                        "title": title,
                        "content_path": content_path,
                        "chapter_order": chapter_order
                    }
                )
            ]
        ).wait()

        # Store metadata in Neon
        with connect(self.neon_conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO chapters (id, title, content_path, chapter_order) VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, content_path = EXCLUDED.content_path, chapter_order = EXCLUDED.chapter_order;",
                    (chapter_id, title, content_path, chapter_order)
                )
                conn.commit()
        print(f"Ingested chapter: {title}")
