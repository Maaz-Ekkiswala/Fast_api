from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.user.models import User


from passlib.context import CryptContext

from core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_user(db: Session, user):
    password = get_hashed_password(user.password)
    db_user = User(username=user.username, email=user.email, phone=user.phone, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
