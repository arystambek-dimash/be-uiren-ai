from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.profiles import Profile
from src.repositories.base import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Profile)

    async def get_by_user_id(self, user_id: int) -> Profile | None:
        stmt = select(Profile).where(Profile.user_id == user_id)
        result = await self._session.execute(stmt)
        profile = result.scalar_one_or_none()
        return profile
