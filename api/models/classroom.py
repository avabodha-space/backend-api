from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field
from typing import List
from api.models.user_id import UserInDB
from datetime import datetime

class ClassroomIn(BaseModel):
    name: str = Field(default="New Untitled Classroom", max_length=200, min_length=3)
    description: str = Field(default=None, max_length=1000)


class ClassroomOut(ClassroomIn):
    owner_user: Link[UserInDB]
    # we store the id of the user who is the owner of this classroom
    instructors: List[Link[UserInDB]] = []
    # store list of user ids of users who are instructors
    students: List[Link[UserInDB]] = []


class Classroom(Document, ClassroomOut):
    created_time: datetime
    student_join_code: str | None = None
    instructor_join_code: str | None = None
