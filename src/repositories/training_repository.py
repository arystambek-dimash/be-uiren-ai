from typing import Tuple

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.trainings import Training
from src.repositories import BaseRepository


class TrainingRepository(BaseRepository[Training]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Training)

    async def get_statistics(self, user_id: int, training_type: str) -> Tuple[int, float]:
        stmt = (
            select(
                func.count(Training.id).label("cnt"),
                func.avg(Training.accuracy).label("avg_accuracy"),
            )
            .where(Training.user_id == user_id, Training.type == training_type)
        )

        result = await self._session.execute(stmt)
        cnt, avg_accuracy = result.one()
        return int(cnt or 0), float(avg_accuracy) if avg_accuracy is not None else 0.0
