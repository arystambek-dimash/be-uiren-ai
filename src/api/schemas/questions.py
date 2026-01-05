from typing import Any

from pydantic import BaseModel

from src.app.constants import QuestionType


class QuestionRead(BaseModel):
    id: int
    type: QuestionType
    content: dict[str, Any]
    difficulty: int

    class Config:
        from_attributes = True
