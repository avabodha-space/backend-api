from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field
from typing import List
from api.models.user import UserInDB
from datetime import datetime
from enum import Enum
from beanie import PydanticObjectId


class ClassroomIn(BaseModel):
    name: str = Field(default="New Untitled Classroom", max_length=200, min_length=3)
    description: str = Field(default=None, max_length=1000)


class Classroom(Document, ClassroomIn):
    owner_user: Link[UserInDB]
    # we store the id of the user who is the owner of this classroom
    instructors: List[Link[UserInDB]] = []
    # store list of user ids of users who are instructors
    students: List[Link[UserInDB]] = []

    created_time: datetime
    student_join_code: str | None = None
    instructor_join_code: str | None = None


class ClassroomShort(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    owner_name: str | None = None
    name: str
    description: str

    class Settings:
        projection = {
            "owner_name": "$owner_user.username",
            "name": 1,
            "description": 1,
        }


class ClassRoles(str, Enum):
    Owner = "owner"
    Instructor = "instructor"
    Student = "student"


class ClassRolesPlus(str, Enum):
    Owner = "owner"
    Instructor = "instructor"
    Student = "student"
    Norole = "norole"


class UserInClassroom(BaseModel):
    username: str | None = None
    profile_pic: str | None = None


class ClassroomPeople(BaseModel):
    instructor_count: int
    student_count: int
    owner_user: UserInClassroom
    instructors: List[UserInClassroom]
    students: List[UserInClassroom]

    class Settings:
        projection = {
            "instructor_count": {"$size": "$instructors"},
            "student_count": {"$size": "$students"},
            "owner_user.username": 1,
            "owner_user.profile_pic": 1,
            "students.username": 1,
            "instructors.username": 1,
            "students.profile_pic": 1,
            "instructors.profile_pic": 1,
        }
