from datetime import timedelta
from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    access_token_expires: timedelta = timedelta(minutes=120)


class RefreshToken(AccessToken):
    refresh_token: str
    refresh_token_expires: timedelta = timedelta(days=90)
