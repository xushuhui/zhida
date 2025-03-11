from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from .base import BaseRepository
from ..models.base import Statistics

class StatisticsRepository(BaseRepository[Statistics]):
    def __init__(self, db: Session):
        super().__init__(Statistics, db)

    def get_user_daily_stats(self, user_id: int, start_date: date, end_date: date) -> List[Statistics]:
        stmt = (
            select(self.model)
            .filter(
                self.model.user_id == user_id,
                self.model.date >= start_date,
                self.model.date <= end_date
            )
            .order_by(self.model.date)
        )
        return list(self.db.execute(stmt).scalars().all())

    def update_daily_stats(self, user_id: int, stats_date: date, 
                          chat_count: int = 0, message_count: int = 0,
                          avg_response_time: float = 0.0, token_usage: int = 0,
                          error_count: int = 0) -> Statistics:
        stats = self.get_by(user_id=user_id, date=stats_date)
        if not stats:
            stats_data = {
                "user_id": user_id,
                "date": stats_date,
                "chat_count": chat_count,
                "message_count": message_count,
                "avg_response_time": avg_response_time,
                "token_usage": token_usage,
                "error_count": error_count
            }
            return self.create(stats_data)
        else:
            stats_data = {
                "chat_count": stats.chat_count + chat_count,
                "message_count": stats.message_count + message_count,
                "avg_response_time": (stats.avg_response_time + avg_response_time) / 2 if stats.avg_response_time else avg_response_time,
                "token_usage": stats.token_usage + token_usage,
                "error_count": stats.error_count + error_count
            }
            return self.update(stats.id, stats_data)

    def get_total_stats(self, user_id: int) -> dict:
        stmt = (
            select(
                func.sum(self.model.chat_count).label("total_chats"),
                func.sum(self.model.message_count).label("total_messages"),
                func.avg(self.model.avg_response_time).label("avg_response_time"),
                func.sum(self.model.token_usage).label("total_tokens"),
                func.sum(self.model.error_count).label("total_errors")
            )
            .filter(self.model.user_id == user_id)
        )
        result = self.db.execute(stmt).first()
        return {
            "total_chats": result.total_chats or 0,
            "total_messages": result.total_messages or 0,
            "avg_response_time": float(result.avg_response_time or 0),
            "total_tokens": result.total_tokens or 0,
            "total_errors": result.total_errors or 0
        }