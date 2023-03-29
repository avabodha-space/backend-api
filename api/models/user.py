from datetime import datetime
from typing import Optional

from beanie import Document, Indexed, Link

from pydantic import BaseModel, EmailStr

# from api.models.classroom import Classroom
from typing import List


class UserAuth(BaseModel):
    # what comes in user login form
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    # what comes in user update request
    email: EmailStr | None = None
    username: str | None = None
    bio: str | None = None
    profile_pic: str | None = None


class UserOut(UserUpdate):
    # what is given in response
    email: Indexed(EmailStr, unique=True)
    disabled: bool = False


class UserInDB(Document, UserOut):
    # what is stored in db
    hashed_password: str
    email_confirmed_at: Optional[datetime] = None

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return str(self.email)

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UserInDB):
            return self.email == other.email
        return False

    @property
    def created(self) -> datetime:
        return self.id.generation_time

    @classmethod
    async def by_email(cls, email: str) -> "UserInDB":
        return await cls.find_one(cls.email == email)


class UserInClassroomView(BaseModel):
    username: str | None = None
    profile_pic: str | None = None

    class Settings:
        projection = {
            "username": 1,
            "profile_pic": 1,
        }
