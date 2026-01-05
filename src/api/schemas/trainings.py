from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class WritingPost(BaseModel):
    topic: str
    writing: str


class ChatMsg(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class SpeakingPost(BaseModel):
    topic: str
    messages: List[ChatMsg]


class TrainingIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["grammar", "spelling", "punctuation", "vocabulary", "style", "coherence", "task"]
    snippet: str = Field(..., description="Short excerpt where the issue appears")
    explanation: str
    suggestion: str


class TrainingAIResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    accuracy: int = Field(..., ge=0, le=100)
    band: Optional[str] = Field(None, description="Optional CEFR/IELTS-style band label if you use it")
    strengths: List[str]
    issues: List[TrainingIssue]
    improved_version: str = Field(..., description="A corrected/improved version of the text")
    next_steps: List[str] = Field(..., description="Concrete practice tasks for the student")


class Statistic(BaseModel):
    count: int
    accuracy: float

    class Config:
        from_attributes = True


class TrainingStatics(BaseModel):
    writing: Statistic
    speaking: Statistic
