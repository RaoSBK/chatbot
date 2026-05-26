from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str = Field(..., min_length=1, description="The user's query or message explaining investment topics")
    session_id: Optional[str] = Field(None, description="Optional conversation session ID to maintain history")

class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    topic: str = Field(..., description="The personal finance topic identified from the conversation")
    response: str = Field(..., description="The structured, educational response from the assistant")
