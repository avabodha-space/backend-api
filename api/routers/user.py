from fastapi import APIRouter, Depends, HTTPException, status

from api.models.user import UserInDB, UserOut, UserUpdate


from api.utils.current_user import get_current_active_user

router = APIRouter(prefix="/user", tags=["User"])


@router.get("", response_model=UserOut)
async def get_user(user: UserInDB = Depends(get_current_active_user)):
    return user


@router.patch("", response_model=UserOut)
async def update_user(
    update: UserUpdate, user: UserInDB = Depends(get_current_active_user)
):
    user = user.copy(update=update.dict(exclude_unset=True))
    try:
        await user.save()
    except Exception as exc:
        if type(exc).__name__ == "DuplicateKeyError":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="DuplicateKeyError: Another user exists with this email",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Please provide valid values or try again later",
            )

    return user


# update email should have a different route, as we need to except duplicate email case,
# and also send verification link
