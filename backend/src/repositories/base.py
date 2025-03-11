from typing import Generic, TypeVar, Type, Optional, List, Union, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from ..models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        return self.db.get(self.model, id)

    def get_by(self, **kwargs) -> Optional[ModelType]:
        stmt = select(self.model).filter_by(**kwargs)
        return self.db.execute(stmt).scalar_one_or_none()

    def list(self, skip: int = 0, limit: int = 100, **filters) -> List[ModelType]:
        stmt = select(self.model).filter_by(**filters).offset(skip).limit(limit)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, obj_in: Union[Dict[str, Any], ModelType]) -> ModelType:
        if isinstance(obj_in, dict):
            obj = self.model(**obj_in)
        else:
            obj = obj_in
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: int, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        stmt = update(self.model).where(self.model.id == id).values(**obj_in)
        self.db.execute(stmt)
        self.db.commit()
        return self.get(id)

    def delete(self, id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == id)
        self.db.execute(stmt)
        self.db.commit()
        return True

    def count(self, **filters) -> int:
        stmt = select(self.model).filter_by(**filters)
        return len(list(self.db.execute(stmt).scalars().all()))