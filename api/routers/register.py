from fastapi import APIRouter, Body, Depends, HTTPException, Response

from pydantic import EmailStr

from api.models.user import UserInDB, UserAuth, UserOut

# from api.utils.mail import send_password_reset_email
from api.utils.password import get_password_hash

router = APIRouter(prefix="/register", tags=["User Registration"])


@router.post("", response_model=UserOut)
async def user_registration(user_auth: UserAuth):
    user = await UserInDB.by_email(user_auth.email)
    if user is not None:
        raise HTTPException(409, "This email is already registered with another user")
    hashed = get_password_hash(user_auth.password)
    user = UserInDB(email=user_auth.email, hashed_password=hashed)
    await user.create()
    return user


# to be implemented
# forgot password
# reset password
# verify email
