from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Field

from src.app.constants import EnglishLevel, QuestionType


class XPosEnum(int, Enum):
    NEGATIVE = -1
    POSITIVE = 1
    NEUTRAL = 0


class SuccessResponse(BaseModel):
    success: bool
    message: str


class EdgeResponse(BaseModel):
    title: str
    description_of_edge: str
    x: XPosEnum


class EdgeListResponse(BaseModel):
    roadmap_edges: List[EdgeResponse]
    level: EnglishLevel

    class Config:
        extra = "ignore"


class RoadmapResponse(BaseModel):
    edges: List[EdgeListResponse]


###################### QUESTION RESPONSE #######################

class FillGapContent(BaseModel):
    sentence_parts: list[str] = Field(..., description="Части предложения [до, после]")
    hidden_word: str = Field(..., description="Слово, которое нужно вставить (правильный ответ)")
    options: list[str] = Field(..., description="Массив вариантов ответа (строки)")
    translation: str = Field(..., description="Перевод всего предложения на казахский")


# --- 2. TRANSLATE MODELS ---
class TranslateOption(BaseModel):
    id: str
    text: str


class TranslateContent(BaseModel):
    source_sentence: str = Field(..., description="Предложение на английском")
    correct_option_id: str = Field(..., description="ID правильного ответа")
    options: list[TranslateOption] = Field(..., description="Варианты перевода")


# --- 3. MATCH PAIRS MODELS ---
class MatchPairItem(BaseModel):
    id: str
    left: str = Field(..., description="Английское слово")
    right: str = Field(..., description="Перевод")


class MatchPairsContent(BaseModel):
    pairs: list[MatchPairItem] = Field(..., description="Список пар для соединения")


QuestionContent = Union[FillGapContent, TranslateContent, MatchPairsContent]


class QuestionResponse(BaseModel):
    type: QuestionType
    content: QuestionContent
    difficulty: int


class StudWordResponse(BaseModel):
    word_ru: str
    word_kk: str
    word_en: str

    usage_context_kk: str
    usage_context_en: str
    usage_context_ru: str


class ListEdgeRelationsResponse(BaseModel):
    questions: List[QuestionResponse]
    study_words: List[StudWordResponse]
