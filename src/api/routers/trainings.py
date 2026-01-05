import json

from fastapi import APIRouter, Depends

from src.api.depends import get_current_user, get_openai_service, get_uow, get_training_repo
from src.api.schemas.trainings import WritingPost, TrainingStatics, Statistic, SpeakingPost, \
    TrainingAIResponse
from src.api.schemas.users import UserRead
from src.app.constants import TrainingType
from src.app.uow import UoW
from src.repositories.training_repository import TrainingRepository
from src.services.openai_service import OpenAIService

router = APIRouter(prefix="/trainings", tags=["trainings"])


@router.post("/writing", response_model=TrainingAIResponse)
async def post_writing(
        writing: WritingPost,
        current_user: UserRead = Depends(get_current_user),
        openai_service: OpenAIService = Depends(get_openai_service),
        uow: UoW = Depends(get_uow),
        training_repo: TrainingRepository = Depends(get_training_repo),
):
    prompt = """
You are an expert writing tutor and examiner.

Task:
- Evaluate the student's writing for: task achievement, coherence, grammar, vocabulary, and style.
- Provide specific, actionable feedback and a corrected/improved version of the text.

Rules:
- Return ONLY valid JSON that matches the provided response schema.
- Do not include markdown, extra keys, or any text outside JSON.
"""

    payload = writing.model_dump() if hasattr(writing, "model_dump") else writing.dict()

    response: TrainingAIResponse = await openai_service.request(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        response_format=TrainingAIResponse,
    )
    async with uow:
        await training_repo.create(**{
            "accuracy": response.accuracy,
            "type": TrainingType.WRITING.value,
            "user_id": current_user.id,
        })
    return response


@router.post("/speaking", response_model=TrainingAIResponse)
async def post_speaking(
        speaking: SpeakingPost,
        current_user: UserRead = Depends(get_current_user),
        openai_service: OpenAIService = Depends(get_openai_service),
        uow: UoW = Depends(get_uow),
        training_repo: TrainingRepository = Depends(get_training_repo),
):
    prompt = """
You are an expert speaking tutor and examiner.

Task:
- Evaluate the student's speaking (based on the provided transcript/messages) for: task achievement, coherence, grammar, vocabulary, and style.
- Provide specific, actionable feedback and an improved version of the student's answer.

Rules:
- Return ONLY valid JSON that matches the provided response schema.
- Do not include markdown, extra keys, or any text outside JSON.
"""

    payload = speaking.model_dump() if hasattr(speaking, "model_dump") else speaking.dict()

    response: TrainingAIResponse = await openai_service.request(
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        response_format=TrainingAIResponse,
    )

    async with uow:
        await training_repo.create(
            **{
                "accuracy": response.accuracy,
                "type": TrainingType.SPEAKING.value,
                "user_id": current_user.id,
            }
        )

    return response


@router.get("/statistics", response_model=TrainingStatics)
async def get_training_statistics(
        current_user: UserRead = Depends(get_current_user),
        training_repo: TrainingRepository = Depends(get_training_repo),
):
    writing = await training_repo.get_statistics(current_user.id, TrainingType.WRITING)
    speaking = await training_repo.get_statistics(current_user.id, TrainingType.SPEAKING)

    return TrainingStatics(writing=Statistic(accuracy=writing[1], count=writing[0]), speaking=Statistic(accuracy=speaking[1], count=speaking[0]))
