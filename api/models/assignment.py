from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field
from typing import List
from api.models.user import UserInDB
from api.models.classroom import Classroom
from api.models.quiz import Quiz
from datetime import datetime


class Assignment(Document):
    quiz: Link[Quiz]
    to_classroom: Link[Classroom]
    deadline: datetime

# class AssignmentIn(BaseModel):
#     pass
# take elements indivisually

class AssignmentOut(BaseModel):
    pass


