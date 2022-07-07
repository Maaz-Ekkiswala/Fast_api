from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.todo import schemas, crud
from app.todo.constants import TodoStatus
from app.todo.models import ToDoItems, ToDo
from app.todo.schemas import TodoSchema, TodoItemsSchema, TodoSchemaById, TodoItemsSchemaById
from db.depandency import get_db

router = APIRouter(tags=["todo"])


def authorize_todo(authorize: AuthJWT = Depends()):
    # try:
    #     authorize.jwt_required()
    # except:
    #     raise HTTPException(status_code=404, detail="Please Signup or login First")
    # user_id = authorize.get_jwt_subject()
    user_id = 1
    return user_id


@router.get("/todo/", response_model=List[TodoSchemaById])
def read_todo(db: Session = Depends(get_db), user=Depends(authorize_todo)):
    todo = crud.get_todo(db, user)
    print(user)
    return todo


@router.post("/todo/", response_model=TodoSchema)
def create_todo(
        todo: schemas.TodoSchemaCreate,
        user=Depends(authorize_todo),
        db_work: Session = Depends(get_db)
):
    todo_items = {'title': todo.title, "user_id": user}
    return crud.create_todo(db=db_work, todo=todo_items)


@router.get("/todo/{id}/", response_model=TodoSchema)
def get_todo_id(id: int, status: Union[int, None] = Query(default=None), db: Session = Depends(get_db),
                user=Depends(authorize_todo)):
    items_id = crud.get_todo_id(db, user, id=id)
    print(items_id)
    if not items_id:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_items = db.query(ToDoItems).filter(ToDoItems.todo_id == id)
    print(todo_items)
    if status:
        todo_items = todo_items.filter(ToDoItems.status == TodoStatus(status).name)
    items_id.todo_items = todo_items.all()
    return items_id


@router.put("/todo/{id}/", response_model=TodoSchema)
def update_todo(todo_update: schemas.TodoSchemaCreate, id: int, db: Session = Depends(get_db),
                user=Depends(authorize_todo)):
    crud.update_todo(db, user, todo=todo_update, id=id)

    return crud.get_todo_id(db, user, id=id)


@router.delete("/todo/{id}/")
def delete_todo(id: int, db: Session = Depends(get_db), user=Depends(authorize_todo)):
    crud.delete_todo(db, user, id=id)
    return {"msg": "data Deleted Successfully"}


# ---------------------------------------------------------------------------------------------------------------------------------------------------
# todo_items start from here *******************************************************************************************
@router.get("/todo_items/", response_model=List[TodoItemsSchema])
def read_todo_items(db: Session = Depends(get_db), user=Depends(authorize_todo)):
    items_desc = crud.get_todo_items(db, user)
    if not items_desc:
        raise HTTPException(status_code=404, detail="User not found")
    return items_desc


@router.post("/todo_items/", response_model=TodoItemsSchema)
def create_items_for_todo(
        todo_items: schemas.TodoItemsSchemaCreate, db_work: Session = Depends(get_db),
        user=Depends(authorize_todo)
):
    print(user)
    todo_id_fetch = db_work.query(ToDo).filter(todo_items.todo_id == ToDo.id, ToDo.user_id == user).first()
    print(todo_id_fetch)
    if not todo_id_fetch:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    todo_items_items = {'todo_id': todo_items.todo_id, 'description': todo_items.description,
                        'title': todo_items.title,
                        'status': todo_items.status}
    return crud.create_todo_items(db_work, todo_items=todo_items_items)


@router.get("/todo_items/{id}/", response_model=TodoItemsSchemaById)
def get_todo_items_id(id: int, db: Session = Depends(get_db), user=Depends(authorize_todo)):
    desc_id = crud.get_todo_items_id(db, user, id=id)
    # if status == 0 and not status:
    #     desc_id.todo_items = db.query(ToDoItems).filter(ToDoItems.status == TodoStatus(status).name).all()
    if not desc_id:
        raise HTTPException(status_code=404, detail="User not found")
    return desc_id


@router.put("/todo_items/{id}/", response_model=TodoItemsSchema)
def update_todo_items(todo_items_update: schemas.TodoItemsSchemaCreate, id: int, db_update: Session = Depends(get_db),
                      user=Depends(authorize_todo)):
    print(db_update)
    crud.update_todo_items(db=db_update, user=user, todo_items=todo_items_update, id=id)
    return crud.get_todo_items_id(db=db_update, user=user, id=id)


@router.delete("/todo_items/{id}/")
def delete_todo_items(id: int, db: Session = Depends(get_db), user=Depends(authorize_todo)):

    desc_id = crud.get_todo_items_id(db, user, id=id)
    print(desc_id)
    if not desc_id:
        raise HTTPException(status_code=404, detail="Data not found")
    crud.delete_todo_items(db, user, id=id)
    return {"msg": "data Deleted Successfully"}
