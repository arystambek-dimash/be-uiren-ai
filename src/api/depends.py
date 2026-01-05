from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import exceptions as jwt
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.requests import Request

from src.app.uow import UoW
from src.repositories import UserRepository, ProfileRepository, RoadmapEdgesRepository, StudyWordRepository, \
    QuestionRepository, UserAnswerRepository
from src.repositories.training_repository import TrainingRepository
from src.services.jwt_service import decode_jwt
from src.services.openai_service import OpenAIService

http_bearer = HTTPBearer(auto_error=False)


def get_sessionmaker(request: Request) -> async_sessionmaker[AsyncSession]:
    return request.app.state.sessionmaker


async def get_session(
        sessionmaker: async_sessionmaker[AsyncSession] = Depends(get_sessionmaker),
) -> AsyncSession:
    async with sessionmaker() as session:
        yield session


async def get_uow(session: AsyncSession = Depends(get_session)) -> UoW:
    return UoW(session=session)


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)


def get_profile_repository(session: AsyncSession = Depends(get_session)) -> ProfileRepository:
    return ProfileRepository(session=session)


def get_roadmap_edge_repository(session: AsyncSession = Depends(get_session)) -> RoadmapEdgesRepository:
    return RoadmapEdgesRepository(session=session)


def get_user_answer_repository(session: AsyncSession = Depends(get_session)) -> UserAnswerRepository:
    return UserAnswerRepository(session=session)


def get_study_word_repo(session: AsyncSession = Depends(get_session)) -> StudyWordRepository:
    return StudyWordRepository(session=session)


def get_training_repo(session: AsyncSession = Depends(get_session)) -> TrainingRepository:
    return TrainingRepository(session=session)


def get_question_repo(session: AsyncSession = Depends(get_session)) -> QuestionRepository:
    return QuestionRepository(session=session)


def get_openai_service(request: Request) -> OpenAIService:
    return OpenAIService(
        api_key=request.app.state.settings.OPENAI_API_KEY,
    )


async def get_current_user(
        request: Request,
        credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
        user_repo: UserRepository = Depends(get_user_repository),
):
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Authorization token is required")

    token = credentials.credentials
    print(token)
    try:
        decoded: dict = await decode_jwt(
            token,
            key=request.app.state.settings.JWT_ACCESS_TOKEN_SECRET_KEY,
        )

        user_id = decoded.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token is expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
