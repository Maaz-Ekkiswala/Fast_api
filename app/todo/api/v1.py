from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.todo import schemas, crud
from app.todo.constants import TodoStatus
from app.todo.models import ToDoItems
from app.todo.schemas import TodoSchema, TodoItemsSchema
from db.depandency import get_db

router = APIRouter()


@router.post("/todo/", response_model=schemas.TodoSchema)
def create_todo(
        todo: schemas.TodoSchemaCreate, db_work: Session = Depends(get_db)
):
    return crud.create_todo(db=db_work, todo=todo)


@router.post("/todo_items/", response_model=schemas.TodoItemsSchema)
def create_items_for_work(
        todo_items: schemas.TodoItemsSchemaCreate, db_work: Session = Depends(get_db)
):
    return crud.create_todo_items(db=db_work, todo_items=todo_items)


@router.get("/todo/", response_model=List[schemas.TodoSchema])
def read_todo(db: Session = Depends(get_db)):
    items = crud.get_todo(db)
    if db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return items


@router.get("/todo_items/", response_model=List[schemas.TodoItemsSchema])
def read_todo(db: Session = Depends(get_db)):
    items_desc = crud.get_todo_items(db)
    return items_desc


@router.put("/todo/{id}", response_model=schemas.TodoSchema)
def update_todo(todo_update: schemas.TodoSchemaCreate, id: int, db_update: Session = Depends(get_db)):
    crud.update_todo(db=db_update, todo=todo_update, id=id)
    return crud.get_todo_id(db=db_update, id=id)


@router.get("/todo/{id}", response_model=schemas.TodoSchema)
def read_todo_id(id: int, status: Union[int, None] = Query(default=None), db: Session = Depends(get_db)):
    items_id = crud.get_todo_id(db, id=id)
    if status == 0 and not status:
        items_id.todo_items = db.query(ToDoItems).filter(ToDoItems.status == TodoStatus(status).name).all()
    return items_id


@router.delete("/todo/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, id=id)
    return {"msg": "data Deleted Successfully"}


@router.get("/todo_items/{id}", response_model=schemas.TodoItemsSchemaById)
def read_todo_items_id(id: int, db: Session = Depends(get_db)):
    desc_id = crud.get_todo_items_id(db, id=id)
    # if status == 0 and not status:
    #     desc_id.todo_items = db.query(ToDoItems).filter(ToDoItems.status == TodoStatus(status).name).all()
    if desc_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    return desc_id



@router.put("/todo_items/{id}", response_model=schemas.TodoItemsSchema)
def update_todo_items(todo_items_update: schemas.TodoItemsSchemaCreate, id: int, db_update: Session = Depends(get_db)):
    print(todo_items_update)
    crud.update_todo_items(db=db_update, todo_items=todo_items_update, id=id)
    return crud.get_todo_items_id(db=db_update, id=id)


@router.delete("/todo_items/{id}")
def delete_todo_items(id: int, db: Session = Depends(get_db)):
    crud.delete_todo_items(db, id=id)
    return {"msg": "data Deleted Successfully"}
