import pytest
from fastapi.testclient import TestClient
from backend.src.main import app # Assuming your main FastAPI app is in main.py
from backend.src.services.rag_service import RAGService

client = TestClient(app)

# Mock the RAGService to control its behavior during testing
class MockRAGService(RAGService):
    def query_chatbot(self, query: str) -> dict:
        if "Physical AI" in query:
            return {"response_text": "Physical AI integrates AI with physical systems.", "source_references": ["intro-to-physical-ai:10"]}
        elif "Humanoid" in query:
            return {"response_text": "Humanoid robots use bipedal locomotion.", "source_references": ["basics-of-humanoid-robotics:12"]}
        else:
            return {"response_text": "I'm sorry, I don't have information on that topic.", "source_references": []}

# Override the RAGService dependency for testing
app.dependency_overrides[RAGService] = MockRAGService

def test_chat_query_physical_ai():
    response = client.post(
        "/chat/query",
        json={
            "query": "What is Physical AI?",
            "user_id": "testuser1",
            "context": "introduction-to-physical-ai"
        }
    )
    assert response.status_code == 200
    assert "Physical AI integrates AI with physical systems." in response.json()["text"]
    assert "intro-to-physical-ai:10" in response.json()["source_references"]

def test_chat_query_humanoid_robotics():
    response = client.post(
        "/chat/query",
        json={
            "query": "How do Humanoid robots move?",
            "user_id": "testuser2",
            "context": "basics-of-humanoid-robotics"
        }
    )
    assert response.status_code == 200
    assert "Humanoid robots use bipedal locomotion." in response.json()["text"]
    assert "basics-of-humanoid-robotics:12" in response.json()["source_references"]

def test_chat_query_unknown_topic():
    response = client.post(
        "/chat/query",
        json={
            "query": "Tell me about quantum physics."
        }
    )
    assert response.status_code == 200
    assert "I'm sorry, I don't have information on that topic." in response.json()["text"]
    assert response.json()["source_references"] == []

def test_chat_query_invalid_input():
    response = client.post(
        "/chat/query",
        json={
            "user_id": "testuser3"
        } # Missing 'query' field
    )
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation error
