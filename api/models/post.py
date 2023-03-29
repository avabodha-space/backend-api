from datetime import datetime
from typing import Optional

from beanie import Document, Indexed, Link

from pydantic import BaseModel
from api.models.classroom import Classroom
from typing import List
from beanie import PydanticObjectId


class PostIn(BaseModel):
    title: str
    description: str | None = None
    body: str | None = None
    attachments: List[str] = []


class PostOut(PostIn):
    id: PydanticObjectId

    class Settings:
        projection = {
            "id": "$_id",
            "title": 1,
            "description": 1,
            "body": 1,
            "attachments": 1,
        }


# need to return post id when returning list of posts


class Post(Document, PostIn):
    classroom: Link[Classroom]
    created: datetime | None = None
    last_updated: datetime | None = None
