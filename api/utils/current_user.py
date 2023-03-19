from fastapi import Depends, HTTPException, status

from api.models.user_id import UserInDB
from api.models.user_profile import UserProfile
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from api.config import CONFIG


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CONFIG.secret_key, algorithms=[CONFIG.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    user = await UserInDB.by_email(email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user),
) -> UserInDB:
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def get_current_active_user_profile(
    current_user: UserInDB = Depends(get_current_active_user),
) -> UserProfile:
    user_profile = await UserProfile.find_one(UserProfile.user.id == current_user.id)

    if user_profile:
        return user_profile
    else:
        user_profile = UserProfile(user=current_user)
        user_profile.insert()
        return user_profile


gcu = get_current_user
gcau = get_current_active_user
gcaup = get_current_active_user_profile
