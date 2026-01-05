import json

from fastapi import APIRouter, Depends

from src.api.depends import get_profile_repository, get_uow, get_current_user, get_openai_service, \
    get_roadmap_edge_repository
from src.api.schemas.profiles import ProfileCreate
from src.api.schemas.responses import RoadmapResponse
from src.app.uow import UoW
from src.repositories import ProfileRepository, RoadmapEdgesRepository
from src.services.openai_service import OpenAIService

router = APIRouter(prefix="/profile", tags=["users"])


@router.post("/onboard", response_model=ProfileCreate, status_code=201)
async def create_profile(
        data: ProfileCreate,
        profile_repository: ProfileRepository = Depends(get_profile_repository),
        edge_repository: RoadmapEdgesRepository = Depends(get_roadmap_edge_repository),
        uow: UoW = Depends(get_uow),
        current_user=Depends(get_current_user),
        openai_service: OpenAIService = Depends(get_openai_service)
):
    print(data)
    prompt = """
You are an expert Gamified Curriculum Designer and Map Level Architect. Output ONLY valid JSON (no extra text).
INPUT:
- user_level: "<A1|A2|B1|B2|C1>"
- user_interests: ["..."]
- total_items: 100

TASK:
Generate a JSON array of roadmap nodes for English learning.
Progression rule:
- If user_level is below C1, generate a smooth progression from user_level up to C1.
- If user_level is C1, generate advanced C1 practice only (no lower levels).

OUTPUT:
Return an array of exactly total_items objects. Each object MUST contain ONLY:
- "title": short catchy topic (2–5 words, English, unique, no emojis, no numbering)
- "description": very short hint of what will be learned/practiced (6–14 words)
- "x": -1 | 0 | 1 (map position)

CONSTRAINTS:
- Difficulty increases steadily; final ~10 nodes are C1-level (or C1 practice if already C1).
- Topics should frequently reflect user_interests while still covering core skills (vocab, grammar, speaking/listening, reading/writing).
- "x" must form a smooth snake path:
  - first x = 0
  - step change ≤ 1
  - never jump -1↔1 directly
  - no same x more than 4 times in a row
  - avoid hard zigzag (no alternating every step for >3 steps)
"""
    data_dict = data.dict()
    data_dict['user_id'] = current_user.id
    async with uow:
        created = await profile_repository.create(
            **data_dict,
        )
        print(created)
        response: RoadmapResponse = await openai_service.request(
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": json.dumps(data_dict),
                }
            ],
            response_format=RoadmapResponse
        )
        insert_data_dict = []
        for edge in response.edges:
            for e in edge.roadmap_edges:
                mutable_dict = e.dict()
                mutable_dict['level'] = edge.level
                mutable_dict['user_id'] = current_user.id
                mutable_dict['x'] = e.x.value
                insert_data_dict.append(
                    mutable_dict
                )
        await edge_repository.bulk_insert(insert_data_dict)
    return ProfileCreate.from_orm(created)
