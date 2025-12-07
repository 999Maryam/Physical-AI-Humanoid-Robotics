import pytest
from backend.src.models.user_profile import UserProfile

def test_user_profile_creation():
    profile_data = {
        "user_id": "user123",
        "learning_style": "visual",
        "reading_history": ["intro-to-physical-ai", "basics-of-humanoid-robotics"],
        "quiz_performance": {"chapter1": {"score": 85, "attempts": 2}}
    }
    user_profile = UserProfile(**profile_data)

    assert user_profile.user_id == "user123"
    assert user_profile.learning_style == "visual"
    assert "intro-to-physical-ai" in user_profile.reading_history
    assert user_profile.quiz_performance["chapter1"]["score"] == 85

def test_user_profile_optional_fields():
    user_profile = UserProfile(user_id="user456")

    assert user_profile.user_id == "user456"
    assert user_profile.learning_style is None
    assert user_profile.reading_history == []
    assert user_profile.quiz_performance is None

def test_user_profile_missing_user_id():
    with pytest.raises(ValueError):
        UserProfile(learning_style="auditory")
