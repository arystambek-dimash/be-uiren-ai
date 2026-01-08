import json
from collections import defaultdict
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.api.depends import get_current_user, get_roadmap_edge_repository, get_openai_service, get_study_word_repo, \
    get_question_repo, get_uow
from src.api.schemas.questions import QuestionRead
from src.api.schemas.responses import ListEdgeRelationsResponse
from src.api.schemas.roadmaps import RoadmapRead, ListOfRoadmapRead, RoadmapDetailRead, StudyWordRead
from src.api.schemas.users import UserRead
from src.app.uow import UoW
from src.repositories import RoadmapEdgesRepository, StudyWordRepository, QuestionRepository
from src.services.openai_service import OpenAIService

router = APIRouter(prefix="/roadmaps", tags=["Roadmaps"])


@router.get("/", response_model=List[ListOfRoadmapRead])
async def get_roadmaps(
        roadmap_repository: RoadmapEdgesRepository = Depends(get_roadmap_edge_repository),
        current_user: UserRead = Depends(get_current_user),
):
    db_roadmaps = await roadmap_repository.get_by_user_id(current_user.id)

    grouped = defaultdict(list)
    prev_user_answer = None
    for idx, edge in enumerate(db_roadmaps):
        pydantic_edge = RoadmapRead.from_orm(edge)
        pydantic_edge.is_looked = False if idx == 0 or prev_user_answer else True
        grouped[edge.level].append(pydantic_edge)
        prev_user_answer = edge.user_answers

    return [{"level": level, "edges": edges} for level, edges in grouped.items()]


@router.get("/{edge_id}", response_model=RoadmapDetailRead)
async def get_roadmap_detail(
        edge_id: int,
        uow: UoW = Depends(get_uow),
        roadmap_repository: RoadmapEdgesRepository = Depends(get_roadmap_edge_repository),
        study_word_repo: StudyWordRepository = Depends(get_study_word_repo),
        question_repo: QuestionRepository = Depends(get_question_repo),
        openai_service: OpenAIService = Depends(get_openai_service),
        current_user: UserRead = Depends(get_current_user),
):
    db_roadmap = await roadmap_repository.get_with_all_relations(edge_id)
    if not db_roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    if not db_roadmap.study_words or not db_roadmap.questions:
        interests_str = ", ".join(
            current_user.profile.interests) if current_user.profile.interests else "General English"

        system_prompt = """
                You are an expert AI Curriculum Developer for a language learning app.
                Your goal is to generate a personalized micro-lesson in strict JSON format.

                ### TASK:
                1. Generate 5 new **Study Words** based on the Lesson Title and Description.
                2. Generate 5 **Questions** to practice these EXACT words.

                ### CONTENT RULES:
                - **Target Level:** {level}
                - **User Interests:** {interests} (Adapt context sentences to these topics).
                - **Localization:** Provide translations in Kazakh (kk) and Russian (ru).
                - **Consistency:** Questions MUST test the generated Study Words.

                ### QUESTION TYPES & JSON STRUCTURE (Strictly follow this):

                1. TYPE: "fill_gap"
                   Structure:
                   {
                     "type": "fill_gap",
                     "text": "Instruction text (e.g. Fill in the blank)",
                     "content": {
                       "sentence_parts": ["Prefix part", "Suffix part"], 
                       "hidden_word": "Target word (must be from study_words)",
                       "options": ["wrong1", "target_word", "wrong2", "wrong3"],
                       "translation": "Translation of the full sentence (kk)"
                     }
                   }

                2. TYPE: "translate"
                   Structure:
                   {
                     "type": "translate",
                     "text": "Choose the correct translation",
                     "content": {
                       "source_sentence": "Sentence in English using a study word",
                       "correct_option_id": "opt_1",
                       "options": [
                         {{ "id": "opt_1", "text": "Correct translation in KK" }},
                         {{ "id": "opt_2", "text": "Wrong translation 1" }},
                         {{ "id": "opt_3", "text": "Wrong translation 2" }}
                       ]
                     }
                   }

                3. TYPE: "match_pairs"
                   Structure:
                   {
                     "type": "match_pairs",
                     "text": "Match the words",
                     "content": {
                       "pairs": [
                         {{ "id": "p1", "left": "English Word 1", "right": "Kazakh Translation 1" }},
                         {{ "id": "p2", "left": "English Word 2", "right": "Kazakh Translation 2" }},
                         {{ "id": "p3", "left": "English Word 3", "right": "Kazakh Translation 3" }}
                       ]
                     }
                   }
                """

        user_prompt = f"""
                GENERATE LESSON CONTENT:
                - **Title:** {db_roadmap.title}
                - **Description:** {db_roadmap.description_of_edge or "General vocabulary"}
                - **Level:** {current_user.profile.current_english_level}
                - **Interests:** {interests_str}
                """

        try:
            response_json: ListEdgeRelationsResponse = await openai_service.request(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": json.dumps(user_prompt, ensure_ascii=False),
                    }
                ],
                response_format=ListEdgeRelationsResponse
            )
        except Exception as e:
            print(e)
            raise HTTPException(500, f"AI Error: {str(e)}")

        async with uow:
            generated_words = []
            for w in response_json.study_words:
                mutable_dict = w.dict()
                mutable_dict["edge_id"] = edge_id
                try:
                    generated_words.append(await study_word_repo.create(**mutable_dict))
                except Exception as e:
                    raise HTTPException(500, f"AI Error: {str(e)}")
            generated_questions = []
            for q in response_json.questions:
                mutable_dict = q.dict()
                mutable_dict["edge_id"] = edge_id
                mutable_dict["content"] = q.content.dict()
                try:
                    generated_questions.append(await question_repo.create(**mutable_dict))
                except Exception as e:
                    raise HTTPException(500, f"AI Error: {str(e)}")

        db_roadmap.study_words = generated_words
        db_roadmap.questions = generated_questions
    pydantic_model = RoadmapDetailRead.from_orm(db_roadmap)
    pydantic_model.study_words = [StudyWordRead.from_orm(generated_word) for generated_word in db_roadmap.study_words]
    pydantic_model.questions = [QuestionRead.from_orm(question) for question in db_roadmap.questions]
    return pydantic_model
