from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class ChatbotResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the response")
    query_id: str = Field(..., description="Reference to the UserQuery this response is answering")
    text: str = Field(..., description="The AI-generated answer")
    source_references: List[str] = Field(default_factory=list, description="List of specific sections/paragraphs in the textbook that support the answer.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Time when the response was generated")
    relevance_score: Optional[float] = Field(None, description="An internal score indicating how relevant the response is to the query")
