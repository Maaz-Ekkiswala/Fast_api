from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from .models import ToDo, ToDoItems, User
from .schemas import UserInDB, TokenData

from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt, JWTError

from core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)




def create_todo(db: Session, todo):
    print(todo)
    db_work = ToDo(title=todo.title)
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


def create_todo_items(db: Session, todo_items):
    db_work = ToDoItems(todo_id=todo_items.todo_id, description=todo_items.description, title=todo_items.title,
                        status=todo_items.status)
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


def get_todo(db: Session):
    return db.query(ToDo).all()


def get_todo_id(db: Session, id):
    return db.query(ToDo).filter(ToDo.id == id).first()


def get_todo_items(db: Session):
    return db.query(ToDoItems).all()


def update_todo(db: Session, todo, id):
    db_update = db.query(ToDo).filter(ToDo.id == id).update(todo.dict())
    db.commit()
    return db_update


def delete_todo(db: Session, id):
    db_delete = db.query(ToDo).filter(ToDo.id == id).delete()
    db.commit()
    return db_delete


def get_todo_items_id(db: Session, id):
    return db.query(ToDoItems).filter(ToDoItems.id == id).first()


def update_todo_items(db: Session, todo_items, id):
    db_update = db.query(ToDoItems).filter(ToDoItems.id == id).update(todo_items.dict())
    db.commit()
    return db_update


def delete_todo_items(db: Session, id):
    db_delete = db.query(ToDoItems).filter(ToDoItems.id == id).delete()
    db.commit()
    return db_delete


def create_user(db: Session, user):
    password = get_hashed_password(user.password)
    db_user = User(username=user.username, email=user.email, phone=user.phone, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)






