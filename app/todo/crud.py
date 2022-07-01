from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .models import ToDo, ToDoItems

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_todo(db: Session, todo):
    print(todo)

    db_work = ToDo(**todo)
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


def create_todo_items(db: Session, todo_items):
    db_work = ToDoItems(**todo_items)
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


def get_todo(db: Session, id):
    todo = db.query(ToDo).filter(ToDo.user_id == id).all()
    return todo


def get_todo_id(db: Session, user, id):
    return db.query(ToDo).filter(ToDo.id == id, ToDo.user_id == user).first()


def get_todo_items(db: Session, id):
    return db.query(ToDoItems).join(ToDo).filter(ToDo.user_id == id).all()


def update_todo(db: Session, user, todo, id):
    db_update = db.query(ToDo).filter(ToDo.id == id, ToDo.user_id == user).update(todo.dict())
    db.commit()
    return db_update


def delete_todo(db: Session, user, id):
    db_delete = db.query(ToDo).filter(ToDo.id == id, ToDo.user_id == user).delete()
    db.commit()
    return db_delete


def get_todo_items_id(db: Session, user, id):
    return db.query(ToDoItems).join(ToDo).filter(ToDoItems.id == id, ToDo.user_id == user).first()


def update_todo_items(db: Session, user, todo_items, id):
    item_instance = db.query(ToDoItems).filter(ToDoItems.id == id)
    if not item_instance.first():
        raise HTTPException(status_code=404, detail="Invalid credentials")
    db_update = db.query(ToDoItems).join(ToDo).filter(
        ToDoItems.id == id, ToDoItems.todo_id == item_instance.first().todo_id, ToDo.user_id == user
    ).first()
    if db_update:
        item_instance.update(todo_items.dict())
    else:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    db.commit()
    return item_instance


def delete_todo_items(db: Session, user, id):
    item_instance = db.query(ToDoItems).filter(ToDoItems.id == id)
    if not item_instance.first():
        raise HTTPException(status_code=404, detail="Invalid credentials")
    db_delete = db.query(ToDoItems).join(ToDo).filter(
        ToDoItems.id == id, ToDoItems.todo_id == item_instance.first().todo_id, ToDo.user_id == user
    ).first()
    if db_delete:
        item_instance.delete()
    else:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    db.commit()
    return item_instance
