import os
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

class EmbeddingService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    def get_embeddings(self, texts: list[str]):
        return self.embeddings.embed_documents(texts)

    def get_query_embedding(self, query: str):
        return self.embeddings.embed_query(query)
