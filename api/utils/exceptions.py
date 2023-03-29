from fastapi import HTTPException, status


classroom_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Classroom not found"
)
invalid_join_code_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired join code"
)
no_access_to_classroom_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=(
        "User does not have access to the requested data or"
        " rights to perform the requested operation in this classroom."
        " Make sure you have signed in with correct account"
        " or you are requesting an allowed data or operation."
    ),
)
cant_join_classroom_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=(
        "You cant join this classroom, "
        "because you are already a part of this classroom."
        " If you wish to join in a new role, leave the classroom first, "
        "and then try again."
    ),
)

post_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Requested post is not found in classroom.",
)

quiz_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Requested quiz is not found for user.",
)

question_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Requested question is not found for user.",
)
