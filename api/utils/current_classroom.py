from fastapi import Depends

from api.models.user import UserInDB
from api.models.classroom import Classroom
from pydantic import BaseModel
from api.models.classroom import ClassRolesPlus
from beanie import PydanticObjectId
from api.utils.current_user import GcauDep
from api.utils.exceptions import classroom_not_found_exc, no_access_to_classroom_exc
from typing import Annotated


class RoledClassroom(BaseModel):
    user: UserInDB
    classroom: Classroom
    # classroom_full_proj
    role: ClassRolesPlus


def get_user_role(user: UserInDB, classroom: Classroom) -> ClassRolesPlus:
    if user.id == classroom.owner_user.id:
        role = ClassRolesPlus.Owner
    elif user in classroom.instructors:
        role = ClassRolesPlus.Instructor
    elif user in classroom.students:
        role = ClassRolesPlus.Student
    else:
        role = ClassRolesPlus.Norole
    return role


async def get_roled_classroom(
    classroom_id: PydanticObjectId, user: GcauDep
) -> RoledClassroom:
    # determine the role of the requesting user
    classroom = await Classroom.get(classroom_id, fetch_links=True)
    if not classroom:
        raise classroom_not_found_exc
    return RoledClassroom(
        user=user, classroom=classroom, role=get_user_role(user, classroom)
    )


RoledClassroomDep = Annotated[RoledClassroom, Depends(get_roled_classroom)]
RCDep = RoledClassroomDep


async def privilege_student_plus(rc: RCDep) -> RoledClassroom:
    # check if user has privilege of student or above
    if rc.role in (
        ClassRolesPlus.Student,
        ClassRolesPlus.Instructor,
        ClassRolesPlus.Owner,
    ):
        return rc
    raise no_access_to_classroom_exc


async def privilege_instructor_plus(rc: RCDep) -> RoledClassroom:
    # check if user has privilege of instructor or above
    if rc.role in (
        ClassRolesPlus.Instructor,
        ClassRolesPlus.Owner,
    ):
        return rc
    raise no_access_to_classroom_exc


async def privilege_owner(rc: RCDep) -> RoledClassroom:
    if rc.role == ClassRolesPlus.Owner:
        return rc
    raise no_access_to_classroom_exc


RC_sp_Dep = Annotated[RoledClassroom, Depends(privilege_student_plus)]
RC_ip_Dep = Annotated[RoledClassroom, Depends(privilege_instructor_plus)]
RC_o_Dep = Annotated[RoledClassroom, Depends(privilege_owner)]
