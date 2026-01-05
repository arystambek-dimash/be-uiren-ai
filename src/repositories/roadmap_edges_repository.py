from typing import Sequence, Mapping, Any

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.app.constants import EnglishLevel
from src.models.roadmap_edges import RoadmapEdges
from src.repositories.base import BaseRepository


class RoadmapEdgesRepository(BaseRepository[RoadmapEdges]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, RoadmapEdges)

    async def get_by_user_id(
            self, user_id: int
    ) -> Sequence[RoadmapEdges]:
        stmt = (
            select(RoadmapEdges)
            .where(RoadmapEdges.user_id == user_id)
            .options(selectinload(RoadmapEdges.user_answers))
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_with_user_id_and_level(
            self,
            user_id: int,
            level: EnglishLevel,
    ) -> Sequence[RoadmapEdges]:
        stmt = (
            select(RoadmapEdges)
            .where(RoadmapEdges.user_id == user_id)
            .where(RoadmapEdges.level == level)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_with_all_relations(
            self, edge_id: int
    ) -> RoadmapEdges | None:
        stmt = (
            select(RoadmapEdges)
            .where(RoadmapEdges.id == edge_id)
            .options(
                selectinload(RoadmapEdges.study_words),
                selectinload(RoadmapEdges.questions)
            )
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def bulk_insert(self, edges: Sequence[Mapping[str, Any]]):
        stmt = insert(RoadmapEdges).values(list(edges)).returning(RoadmapEdges)
        res = await self._session.execute(stmt)
        instances = res.scalars().all()
        return instances
