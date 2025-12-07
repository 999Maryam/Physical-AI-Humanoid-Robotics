from pydantic import BaseModel, Field
from typing import Optional

class UserQuery(BaseModel):
    query: str = Field(..., description="The user's question or prompt.")
    user_id: Optional[str] = Field(None, description="Optional user ID for personalization/logging.")
    context: Optional[str] = Field(None, description="Optional current chapter or section ID for contextual queries.")
