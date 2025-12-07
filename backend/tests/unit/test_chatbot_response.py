import pytest
from datetime import datetime, timedelta
from backend.src.models.chatbot_response import ChatbotResponse

def test_chatbot_response_creation():
    response_data = {
        "id": "resp1",
        "query_id": "query123",
        "text": "Physical AI is the integration of AI with physical systems.",
        "source_references": ["intro-to-physical-ai:10"]
    }
    response = ChatbotResponse(**response_data)

    assert response.id == "resp1"
    assert response.query_id == "query123"
    assert response.text == "Physical AI is the integration of AI with physical systems."
    assert response.source_references == ["intro-to-physical-ai:10"]
    assert isinstance(response.timestamp, datetime)
    assert response.relevance_score is None

def test_chatbot_response_with_all_fields():
    current_time = datetime.now()
    response_data = {
        "id": "resp2",
        "query_id": "query456",
        "text": "Humanoid robots use bipedal locomotion.",
        "source_references": ["basics-of-humanoid-robotics:12"],
        "timestamp": current_time.isoformat(),
        "relevance_score": 0.85
    }
    response = ChatbotResponse(**response_data)

    assert response.id == "resp2"
    assert response.query_id == "query456"
    assert response.text == "Humanoid robots use bipedal locomotion."
    assert response.source_references == ["basics-of-humanoid-robotics:12"]
    assert response.timestamp.replace(microsecond=0) == current_time.replace(microsecond=0)
    assert response.relevance_score == 0.85

def test_chatbot_response_default_timestamp_and_empty_sources():
    response_data = {
        "id": "resp3",
        "query_id": "query789",
        "text": "ROS 2 uses nodes and topics.",
        "source_references": []
    }
    response = ChatbotResponse(**response_data)

    assert isinstance(response.timestamp, datetime)
    assert datetime.now() - response.timestamp < timedelta(seconds=1)
    assert response.source_references == []

def test_chatbot_response_missing_required_fields():
    with pytest.raises(ValueError):
        ChatbotResponse(id="r4", query_id="q1") # Missing text
    with pytest.raises(ValueError):
        ChatbotResponse(id="r4", text="test", source_references=[]) # Missing query_id
    with pytest.raises(ValueError):
        ChatbotResponse(query_id="q1", text="test", source_references=[]) # Missing id
