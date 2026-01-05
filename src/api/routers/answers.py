from fastapi import APIRouter, Depends, Form, HTTPException

from src.api.depends import get_current_user, get_roadmap_edge_repository, \
    get_user_answer_repository, get_uow
from src.api.schemas.users import UserRead
from src.app.uow import UoW
from src.repositories import UserAnswerRepository, RoadmapEdgesRepository

router = APIRouter(prefix="/user-answers", tags=["User Answers"])


@router.post("", status_code=201)
async def user_answer(
        edge_id: int = Form(),
        accuracy: float = Form(),
        edge_repository: RoadmapEdgesRepository = Depends(get_roadmap_edge_repository),
        user_answer_repository: UserAnswerRepository = Depends(get_user_answer_repository),
        current_user: UserRead = Depends(get_current_user),
        uow: UoW = Depends(get_uow)
):
    db_edge = await edge_repository.get_by_id(edge_id)
    if not db_edge:
        raise HTTPException(status_code=404, detail="Question not found")
    db_user_answer = await user_answer_repository.get_user_answer_for_edge(user_id=current_user.id,
                                                                           edge_id=edge_id)
    if db_user_answer:
        await user_answer_repository.delete(db_user_answer.id)
    async with uow:
        await user_answer_repository.create(**{
            "user_id": current_user.id,
            "roadmap_edge_id": edge_id,
            "accuracy": accuracy
        })
