from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.users import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email).options(
            joinedload(User.profile)
        )
        result = await self._session.execute(stmt)
        user = result.scalars().first()
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id).options(
            joinedload(User.profile)
        )
        result = await self._session.execute(stmt)
        user = result.scalars().first()
        return user
