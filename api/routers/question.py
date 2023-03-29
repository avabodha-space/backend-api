# add question to quiz
# quiz id is optional param, if not provided, the question wont be part of any quiz
# question data + quiz id
from fastapi import APIRouter

from api.utils.current_user import GcauDep
from api.models.question import Question, QuestionIn, QuestionOut
from beanie import PydanticObjectId
from datetime import datetime
from api.models.quiz import Quiz
from api.utils.exceptions import quiz_not_found_exc
from typing import List

router = APIRouter(prefix="/question", tags=["Question"])


@router.get("/all")
async def get_all_questions(user: GcauDep) -> List[QuestionOut]:
    return (
        await Question.find(Question.creator.id == user.id)
        .project(QuestionOut)
        .to_list()
    )


@router.post("/new")
async def create_new_question(
    user: GcauDep,
    question_in: QuestionIn,
    quiz_id: PydanticObjectId | None = None,
) -> PydanticObjectId:
    # optional, if a quiz id is passed, then add this question to that quiz
    now = datetime.now()

    question = Question(
        **question_in.dict(), created_time=now, last_edited=now, creator=user
    )
    await question.insert()

    if quiz_id:
        quiz = await Quiz.find_one(
            Quiz.id == quiz_id, Quiz.creator.id == user.id, fetch_links=True
        )
        if not quiz:
            raise quiz_not_found_exc
        quiz.questions.append(question)
    return question.id


@router.patch("/edit")
async def edit_question(user: GcauDep, question_id: PydanticObjectId):
    pass


@router.delete("/delete")
async def delete_question(user: GcauDep, question_id: PydanticObjectId):
    pass
