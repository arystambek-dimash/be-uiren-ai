from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.questions import Question
from src.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Question)

    async def get_by_edge_id(
            self, edge_id: int, limit: int = 100
    ) -> Sequence[Question]:
        stmt = (
            select(Question)
            .where(Question.edge_id == edge_id)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()
