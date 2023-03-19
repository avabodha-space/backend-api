from beanie import Document, Indexed, PydanticObjectId,Link
from pydantic import BaseModel, Field
from typing import List
from api.models.classroom import Classroom

class AnswerOption(BaseModel):
    text: str = Field(max_length=1000)



class Question(BaseModel):
    question: str = Field(max_length=1000)
    options: List[AnswerOption] = []
    correct: List[int] = []
    points: int | None = None
    # creator: PydanticObjectId
    # sharing: str  # public, private, shared with limited
    # shared_with: List[PydanticObjectId] = []
    # tag: PydanticObjectId
    # store list of indexes of correct options 0-based


class Quiz(Document):
    classroom: Link[Classroom]
    title: Field(default="New Untitled Quiz", min_length=5, max_length=50)
    description: Field(default=None, max_length=500)
    questions: List[Link[Question]]
    # the no of questions in a quiz is limited to 1000
