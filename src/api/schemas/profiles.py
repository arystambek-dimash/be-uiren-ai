from typing import Optional

from pydantic import BaseModel

from src.app.constants import SystemLanguage, EnglishLevel


class ProfileRead(BaseModel):
    id: Optional[int] = None
    age: Optional[int] = None
    system_language: Optional[SystemLanguage] = None
    learning_goal: Optional[str] = None
    current_english_level: Optional[EnglishLevel] = None
    interests: Optional[list] = None
    daily_training_spend: Optional[int] = None

    class Config:
        from_attributes = True


class ProfileCreate(BaseModel):
    age: int
    system_language: SystemLanguage
    learning_goal: str
    current_english_level: EnglishLevel
    interests: list
    daily_training_spend: int

    class Config:
        from_attributes = True


class ProfileUpdate(ProfileCreate):
    age: Optional[int] = None
    system_language: Optional[SystemLanguage] = None
    learning_goal: Optional[str] = None
    current_english_level: Optional[EnglishLevel] = None
    interests: Optional[list] = None
    daily_training_spend: Optional[int] = None
