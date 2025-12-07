from pydantic import BaseModel, Field
from typing import Optional, List

class UserProfile(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user.")
    learning_style: Optional[str] = Field(None, description="User's preferred learning style (e.g., visual, auditory, kinesthetic).")
    reading_history: List[str] = Field(default_factory=list, description="Log of chapters/sections read.")
    quiz_performance: Optional[dict] = Field(None, description="Records of quiz scores, strengths, and weaknesses.")
    preferences: Optional[dict] = Field(None, description="Other user-defined preferences.")
