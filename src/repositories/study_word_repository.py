from sqlalchemy.ext.asyncio import AsyncSession

from src.models.study_words import StudyWord
from src.repositories.base import BaseRepository


class StudyWordRepository(BaseRepository[StudyWord]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, StudyWord)
