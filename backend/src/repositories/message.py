from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from .base import BaseRepository
from ..models.base import Message

class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: Session):
        super().__init__(Message, db)

    def get_session_messages(self, session_id: int, skip: int = 0, limit: int = 50) -> List[Message]:
        stmt = (
            select(self.model)
            .filter_by(session_id=session_id)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_user_messages(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Message]:
        stmt = (
            select(self.model)
            .filter_by(user_id=user_id)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def create_message(self, session_id: int, user_id: int, role: str, content: str, 
                      tokens: Optional[int] = None, client_info: Optional[str] = None,
                      ip_address: Optional[str] = None) -> Message:
        message_data = {
            "session_id": session_id,
            "user_id": user_id,
            "role": role,
            "content": content,
            "tokens": tokens,
            "client_info": client_info,
            "ip_address": ip_address
        }
        return self.create(message_data)