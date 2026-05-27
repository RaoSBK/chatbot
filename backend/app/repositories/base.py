from uuid import UUID
from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: UUID, user_id: UUID) -> Optional[ModelType]:
        from sqlalchemy import inspect
        pk = inspect(self.model).primary_key[0]
        result = await self.db.execute(
            select(self.model).where(
                pk == id,
                self.model.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self, user_id: UUID, skip: int = 0, limit: int = 20) -> List[ModelType]:
        result = await self.db.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, obj_in_data: dict, user_id: UUID) -> ModelType:
        db_obj = self.model(**obj_in_data, user_id=user_id)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelType, obj_in_data: dict) -> ModelType:
        for field, value in obj_in_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: ModelType) -> ModelType:
        await self.db.delete(db_obj)
        await self.db.commit()
        return db_obj
