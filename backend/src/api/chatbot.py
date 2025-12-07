from fastapi import APIRouter
from backend.src.models.user_query import UserQuery
from backend.src.models.chatbot_response import ChatbotResponse
from backend.src.services.rag_service import RAGService
import uuid

router = APIRouter()
rag_service = RAGService()

@router.post("/query", response_model=ChatbotResponse)
async def query_chatbot(user_query: UserQuery):
    response_data = rag_service.query_chatbot(user_query.query)
    chatbot_response = ChatbotResponse(
        id=str(uuid.uuid4()),
        query_id=str(uuid.uuid4()), # Generate a new ID for the query response
        text=response_data["response_text"],
        source_references=response_data["source_references"],
        relevance_score=None # RAGService does not return this yet
    )
    return chatbot_response
