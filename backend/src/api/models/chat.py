from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    role: str = "user"

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    session_id: int
    user_id: int
    tokens: Optional[int] = None
    status: str
    created_at: datetime
    response_time: Optional[float] = None
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True

class SessionBase(BaseModel):
    title: Optional[str] = None

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int
    user_id: int
    status: str
    message_count: int
    last_message_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    context: Optional[dict] = None
    messages: List[Message] = []

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    response: str
    session_id: int
    messages: List[Message]