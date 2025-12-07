import pytest
from backend.src.services.personalization_service import PersonalizationService
from backend.src.models.user_profile import UserProfile

@pytest.fixture
def personalization_service():
    return PersonalizationService()

def test_get_personalized_content_visual_learner(personalization_service):
    user_profile = UserProfile(
        user_id="visual_user",
        learning_style="visual"
    )
    original_content = "This is a chapter about AI."
    personalized_content = personalization_service.get_personalized_content(user_profile, original_content)
    assert "[Personalized for Visual Learner]" in personalized_content
    assert "diagrams and charts" in personalized_content

def test_get_personalized_content_auditory_learner(personalization_service):
    user_profile = UserProfile(
        user_id="auditory_user",
        learning_style="auditory"
    )
    original_content = "This is a chapter about Machine Learning."
    personalized_content = personalization_service.get_personalized_content(user_profile, original_content)
    assert "[Personalized for Auditory Learner]" in personalized_content
    assert "listening to explanations" in personalized_content

def test_get_personalized_content_reading_history_suggestion(personalization_service):
    user_profile = UserProfile(
        user_id="new_user",
        reading_history=["basics-of-humanoid-robotics"]
    )
    original_content = "This is a chapter about advanced robotics."
    personalized_content = personalization_service.get_personalized_content(user_profile, original_content)
    assert "[Suggestion: Read Introduction to Physical AI]" in personalized_content
    assert "introduction helpful" in personalized_content

def test_get_personalized_content_no_personalization(personalization_service):
    user_profile = UserProfile(
        user_id="standard_user",
        learning_style="kinesthetic"
    )
    original_content = "A regular chapter."
    personalized_content = personalization_service.get_personalized_content(user_profile, original_content)
    assert "[Standard Content]" in personalized_content
    assert "A regular chapter." in personalized_content

