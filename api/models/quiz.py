from beanie import Document, Indexed, PydanticObjectId, Link
from pydantic import BaseModel, Field
from typing import List
from api.models.classroom import Classroom
from api.models.question import Question, QuestionOut
from api.models.user import UserInDB


class QuizIn(BaseModel):
    title: Field(default="New Untitled Quiz", min_length=5, max_length=50)
    description: Field(default=None, max_length=500)


class Quiz(Document, QuizIn):
    creator: Link[UserInDB]
    questions: List[Link[Question]]
    # the no of questions in a quiz is limited to 1000


class QuizShort(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    title: str
    description: str | None = None
    creator_name: str
    question_count: int

    class Settings:
        projection = {
            "title": 1,
            "description": 1,
            "creator_name": "$creator.username",
            "question_count": {"$size": "$questions"},
        }


class QuizFull(QuizShort):
    questions: List[QuestionOut]

    class Settings:
        projection = QuizShort.Settings.projection
        projection.update({"questions.creator": 0})
