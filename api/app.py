from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from api.config import CONFIG
from api.models.user import UserInDB
from api.models.classroom import Classroom
from api.models.post import Post
from api.models.question import Question

description = """
# Avabodha LMS

The Sanskrit word "avabodha" (अवबोध) is derived from the root verb "budh" which means "to awaken" or "to know".

"Avabodha" refers to the act of comprehending or understanding deeply, or a clear and complete perception of something.

It can also be translated as "realization" or "enlightenment".

The LMS facilates a smooth flow of interaction between instructors and students.

Teachers can post study material and quizzes which can enhance a student's understaning of a subject.

Our free to use open source LMS is primarily targetted at small institutes and independent private tutors who can manage their batches easily.



Features:
- You can create a classroom
- You can create quizzes


"""
app = FastAPI(title="Avabodha API", version="0.0.1", description=description)


@app.get("/")
async def index() -> dict:
    return {"message": "server is up"}


@app.on_event("startup")
async def start_app():
    client = AsyncIOMotorClient(CONFIG.mongo_uri)
    await init_beanie(
        client.db_name, document_models=[UserInDB, Classroom, Post, Question]
    )
