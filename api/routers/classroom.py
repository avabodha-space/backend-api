import string
import random

from fastapi import APIRouter, HTTPException, Depends, Response, status
from typing import List
from api.models.classroom import (
    Classroom,
    ClassroomIn,
    ClassroomShort,
    ClassRoles,
    ClassRolesPlus,
    ClassroomPeople,
)
from api.models.user import UserInDB
from api.utils.current_user import GcauDep
from api.utils.exceptions import (
    invalid_join_code_exc,
    no_access_to_classroom_exc,
    cant_join_classroom_exc,
)
from datetime import datetime
from beanie import PydanticObjectId
from api.utils.current_classroom import (
    RC_ip_Dep,
    RC_o_Dep,
    RC_sp_Dep,
    RCDep,
)


router = APIRouter(prefix="/classroom", tags=["Classroom"])


def random_join_code(n: int) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


@router.get("/all")
async def list_classrooms(
    class_role: ClassRoles,
    user: GcauDep,
) -> List[ClassroomShort | None]:
    pass
    if class_role == ClassRoles.Owner:
        return (
            await Classroom.find(Classroom.owner_user.id == user.id, fetch_links=True)
            .project(ClassroomShort)
            .to_list()
        )
    elif class_role == ClassRoles.Instructor:
        return (
            await Classroom.find(Classroom.instructors.id == user.id, fetch_links=True)
            .project(ClassroomShort)
            .to_list()
        )
    elif class_role == ClassRoles.Student:
        return (
            await Classroom.find(Classroom.students.id == user.id, fetch_links=True)
            .project(ClassroomShort)
            .to_list()
        )


@router.post("/new")
async def create_new_classroom(
    classroom_in: ClassroomIn, user: GcauDep
) -> PydanticObjectId:
    classroom = Classroom(
        **classroom_in.dict(),
        owner_user=user,
        created_time=datetime.now(),
        student_join_code=random_join_code(7),
        instructor_join_code=random_join_code(12)
    )
    await classroom.insert()

    return classroom.id


# @router.get("")
# async def get_classroom(
#     rc: RC_sp_Dep,
# ) -> ClassroomShort:
#     classroom = rc.classroom

#     return ClassroomShort(
#         owner_name=classroom.owner_user.username,
#         name=classroom.name,
#         description=classroom.description,
#     )


@router.get("/people")
async def get_classroom_people(rc: RC_sp_Dep) -> ClassroomPeople:
    classroom_people = await Classroom.find_one(
        Classroom.id == rc.classroom.id,
        fetch_links=True,
    ).project(ClassroomPeople)
    return classroom_people


@router.post("/join")
async def join_classroom(join_code: str, rc: RCDep) -> ClassroomShort:
    if not rc.role == ClassRolesPlus.Norole:
        raise cant_join_classroom_exc
    classroom = rc.classroom
    if classroom.student_join_code == join_code:
        classroom.students.append(rc.user)

    elif classroom.instructor_join_code == join_code:
        classroom.instructors.append(rc.user)
    else:
        raise invalid_join_code_exc
    await classroom.save()
    return ClassroomShort(
        owner_name=classroom.owner_user.username,
        name=classroom.name,
        description=classroom.description,
        student_count=0,
    )


# get student join code
@router.get("/student-join-code")
async def get_student_join_code(rc: RC_ip_Dep) -> str:
    return rc.classroom.student_join_code


@router.get("/instructor-join-code")
async def get_instructor_join_code(rc: RC_o_Dep) -> str:
    return rc.classroom.instructor_join_code


@router.post("/student-join-code")
async def reset_student_join_code(
    rc: RC_o_Dep,
) -> str:
    rc.classroom.student_join_code = random_join_code(7)
    await rc.classroom.save()
    return rc.classroom.student_join_code


@router.post("/instructor-join-code")
async def reset_instructor_join_code(rc: RC_o_Dep) -> str:
    rc.classroom.instructor_join_code = random_join_code(12)
    await rc.classroom.save()
    return rc.classroom.instructor_join_code


# @router.post("/leave")
# async def leave_classroom(
#     roled_classroom: RoledClassroom = Depends(get_roled_classroom),
# ):
#     pass


# get instructor join code


# reset student join code
# reset instructor join code
# remove member

# @router.patch("/update/{classroom_id}")
# async def update_classroom(user: UserInDB = Depends(get_current_active_user)):
#     pass


# @router.delete("/delete/{classroom_id}")
# async def delete_classroom(user: UserInDB = Depends(get_current_active_user)):
#     pass

