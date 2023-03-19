from fastapi import APIRouter, HTTPException, Depends, Response, status

from api.models.classroom import Classroom, ClassroomIn
from api.models.user_id import UserInDB
from api.models.user_profile import UserProfile
from api.utils.current_user import gcau, gcaup
from typing import List
from datetime import datetime
from beanie import PydanticObjectId
from enum import Enum

router = APIRouter(prefix="/classroom", tags=["Classroom"])


class ClassRoles(str, Enum):
    Owner = "owner"
    Instructor = "instructor"
    Student = "student"


@router.get("/all")
async def list_classrooms(
    class_role: ClassRoles,
    user_profile: UserProfile = Depends(gcaup),
) -> List[Classroom | None]:
    # if class_role == ClassRoles.Owner:
    # classrooms = Classroom.find(Classroom.owner_user.id == user.id)
    # return await classrooms.to_list()
    # elif class_role == ClassRoles.Instructor:
    await user_profile.fetch_all_links()
    if class_role == ClassRoles.Owner:
        return user_profile.owner_of_classrooms

    elif class_role == ClassRoles.Instructor:
        return user_profile.instructor_of_classrooms
    elif class_role == ClassRoles.Student:
        return user_profile.student_of_classrooms

    # user_profile.student_of_classrooms


@router.post("/new")
async def create_new_classroom(
    classroom_in: ClassroomIn, user_profile: UserProfile = Depends(gcaup)
) -> dict[str, str]:
    classroom = Classroom(
        **classroom_in.dict(), owner_user=user_profile.user, created_time=datetime.now()
    )
    await classroom.insert()
    user_profile.owner_of_classrooms.append(classroom)
    await user_profile.save()
    return {"message": "success: created new classroom"}


@router.get("/{classroom_id}")
async def get_classroom(classroom_id: PydanticObjectId, user: UserInDB = Depends(gcau)):
    classroom = await Classroom.get(classroom_id)
    if classroom is not None:
        return classroom
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found"
        )


# @router.post("/{classroom_id}/join/{join_code}")
# async def join_classroom(user:UserInDB = Depends(get_current_active_user),classroom_id,join_code)

# @router.patch("/update/{classroom_id}")
# async def update_classroom(user: UserInDB = Depends(get_current_active_user)):
#     pass


# @router.delete("/delete/{classroom_id}")
# async def delete_classroom(user: UserInDB = Depends(get_current_active_user)):
#     pass
