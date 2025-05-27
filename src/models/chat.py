from pydantic import BaseModel, Field
from datetime import datetime, timezone

class ChatMessage(BaseModel):
    conversation_id: str
    user_id: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MessageResponse(BaseModel):
    message_id: str
    conversation_id: str
    user_id: str
    content: str
    timestamp: datetime