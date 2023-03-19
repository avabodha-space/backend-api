from decouple import config
from pydantic import BaseModel


class Settings(BaseModel):
    mongo_uri = config("MONGO_URI")
    salt = config("SALT").encode()
    secret_key = config("SECRET_KEY")
    algorithm = "HS256"
    access_token_expire_minutes = 120


CONFIG = Settings()
