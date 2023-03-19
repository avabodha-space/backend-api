from datetime import datetime
from typing import Optional

from beanie import Document, Indexed, Link

from pydantic import BaseModel, EmailStr
from api.models.classroom import Classroom
from typing import List


class PostIn(BaseModel):
    title: str
    description: str | None = None
    body: str | None = None
    attachments: List[str] = []


class Post(Document, PostIn):
    created: datetime | None = None
    last_updated: datetime | None = None
