from typing import List

from pydantic import BaseModel, Field

from src.api.schemas.questions import QuestionRead
from src.app.constants import EnglishLevel


class RoadmapRead(BaseModel):
    id: int
    x: int = Field(..., title="X", description="it s required to be 1 0 -1 nothgin else")
    title: str
    description_of_edge: str
    is_looked: bool = False

    class Config:
        from_attributes = True
        extra = "ignore"


class ListOfRoadmapRead(BaseModel):
    level: EnglishLevel
    edges: List[RoadmapRead]


class StudyWordRead(BaseModel):
    id: int
    word_ru: str
    word_kk: str
    word_en: str

    usage_context_kk: str
    usage_context_en: str
    usage_context_ru: str

    class Config:
        from_attributes = True

class RoadmapDetailRead(BaseModel):
    id: int
    title: str
    description_of_edge: str
    questions: List[QuestionRead]
    study_words: List[StudyWordRead]

    class Config:
        from_attributes = True