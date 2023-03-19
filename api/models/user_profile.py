from datetime import datetime
from typing import Optional

from beanie import Document, Indexed, Link

from pydantic import BaseModel, EmailStr
from api.models.classroom import Classroom
from api.models.user_id import UserInDB
from typing import List


class UserProfile(Document):
    user: Link[UserInDB]
    owner_of_classrooms: List[Link[Classroom]] = []
    instructor_of_classrooms: List[Link[Classroom]] = []
    student_of_classrooms: List[Link[Classroom]] = []
