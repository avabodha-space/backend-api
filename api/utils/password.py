from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str):
    return pwd_context.hash(password.encode())
