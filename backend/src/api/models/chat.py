from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class SessionBase(BaseModel):
    title: str
    system_prompt: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int
    user_id: int
    status: str
    message_count: int
    last_message_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str
    role: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    session_id: int
    user_id: int
    tokens: Optional[int]
    status: str
    created_at: datetime
    response_time: Optional[int]
    client_info: Optional[str]
    ip_address: Optional[str]

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None
    system_prompt: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class ChatResponse(BaseModel):
    session_id: int
    message: Message
    total_tokens: Optional[int]