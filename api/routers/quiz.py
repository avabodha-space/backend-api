# create quiz
# return quiz id


from fastapi import APIRouter
from api.utils.current_user import GcauDep
from api.models.quiz import Quiz, QuizFull, QuizShort
from beanie import PydanticObjectId
from api.utils.exceptions import quiz_not_found_exc

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.get("/all")
async def get_all_quizzes(user: GcauDep):
    return (
        await Quiz.find(Quiz.creator.id == user.id, fetch_links=True)
        .project(QuizShort)
        .to_list()
    )


# drop questions take a list of questions to drop and remove them from quiz. optional parameter: delete question to delete those questions too


# get quiz
@router.get("")
async def get_quiz(user: GcauDep, quiz_id: PydanticObjectId):
    quiz = await Quiz.find_one(Quiz.id == quiz_id, fetch_links=True).project(QuizFull)
    if not quiz:
        raise quiz_not_found_exc
    return quiz


# get all the info of the quiz


# edit quiz
# change basic quiz info

# add questions
# remove questions


# delete quiz
