from typing import Optional

from pydantic import BaseModel

from src.api.schemas.profiles import ProfileRead


class TokenSchema(BaseModel):
    token: str


class UserRead(BaseModel):
    id: int
    email: str
    fullname: str
    profile: Optional[ProfileRead] = None

    class Config:
        from_attributes = True
