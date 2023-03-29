from beanie import Document, Indexed, PydanticObjectId, Link
from pydantic import BaseModel, Field
from typing import List
from api.models.user import UserInDB

from datetime import datetime


class AnswerOption(BaseModel):
    text: str = Field(max_length=1000)


class QuestionIn(BaseModel):
    question: str = Field(max_length=1000)
    options: List[AnswerOption | None] = []
    correct: List[int | None] = []
    points: int = 1
    tags: List[str]


class Question(QuestionIn, Document):
    creator: Link[UserInDB]
    created_time: datetime
    last_edited: datetime


class QuestionOut(QuestionIn):
    id: PydanticObjectId = Field(alias="_id")

    class Settings:
        projection = {"creator": 0}

    # creator: PydanticObjectId
    # sharing: str  # public, private, shared with limited
    # shared_with: List[PydanticObjectId] = []
    # tag: PydanticObjectId
    # store list of indexes of correct options 0-based
