from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from .base import BaseRepository
from ..models.base import Session as ChatSession

class SessionRepository(BaseRepository[ChatSession]):
    def __init__(self, db: Session):
        super().__init__(ChatSession, db)

    def get_user_sessions(self, user_id: int, skip: int = 0, limit: int = 20) -> List[ChatSession]:
        stmt = (
            select(self.model)
            .filter_by(user_id=user_id)
            .order_by(desc(self.model.last_message_time))
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def get_active_sessions(self, user_id: int) -> List[ChatSession]:
        return self.list(user_id=user_id, status='active')

    def archive_session(self, session_id: int) -> Optional[ChatSession]:
        return self.update(session_id, {"status": "archived"})