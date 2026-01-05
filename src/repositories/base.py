from typing import TypeVar, Generic, Sequence

from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self._session = session
        self._model = model

    async def create(self, **kwargs) -> ModelType:
        stmt = insert(self._model).values(**kwargs).returning(self._model)
        result = await self._session.execute(stmt)
        instance = result.scalar()
        return instance

    async def get_by_id(self, entity_id: int) -> ModelType | None:
        return await self._session.get(self._model, entity_id)

    async def get_all(self, limit: int = 100, offset: int = 0) -> Sequence[ModelType]:
        stmt = select(self._model).limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update(self, entity_id: int, **kwargs) -> ModelType | None:
        stmt = (
            update(self._model)
            .where(self._model.id == entity_id)
            .values(**kwargs)
            .returning(self._model)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, entity_id: int) -> bool:
        stmt = delete(self._model).where(self._model.id == entity_id)
        result = await self._session.execute(stmt)
        return result.rowcount > 0

    async def count(self) -> int:
        from sqlalchemy import func
        stmt = select(func.count()).select_from(self._model)
        result = await self._session.execute(stmt)
        return result.scalar_one()
