from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_answers import UserAnswer
from src.repositories.base import BaseRepository


class UserAnswerRepository(BaseRepository[UserAnswer]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserAnswer)

    async def get_user_answer_for_edge(
            self, user_id: int, edge_id: int
    ) -> UserAnswer | None:
        stmt = (
            select(UserAnswer)
            .where(
                UserAnswer.user_id == user_id,
                UserAnswer.roadmap_edge_id == edge_id
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
