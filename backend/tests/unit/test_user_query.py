import pytest
from backend.src.models.user_query import UserQuery

def test_user_query_creation():
    query_data = {
        "query": "What is Physical AI?",
        "user_id": "testuser123",
        "context": "introduction-to-physical-ai"
    }
    user_query = UserQuery(**query_data)

    assert user_query.query == "What is Physical AI?"
    assert user_query.user_id == "testuser123"
    assert user_query.context == "introduction-to-physical-ai"

def test_user_query_model_missing_query():
    with pytest.raises(ValueError):
        UserQuery(user_id="testuser123")
