from typing import List, Union
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session
from starlette import status

from app.todo import schemas, crud
from app.todo.constants import TodoStatus
from app.todo.crud import verify_password
from app.todo.models import ToDoItems, User
from app.todo.schemas import TodoSchema, TodoItemsSchema, TodoSchemaById, TodoItemsSchemaById, UserOut, UserAuth, \
    TokenSchema
from db.depandency import get_db

router = APIRouter()


@router.post('/signup/', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth, db_user: Session = Depends(get_db)):
    # querying database to check if user already exist
    user = db_user.query(User).filter(User.email == data.email, User.username == data.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email OR username already exist"
        )

    return crud.create_user(db=db_user, user=data)


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(login_u: schemas.Login, Authorize: AuthJWT = Depends(), db_user: Session = Depends(get_db)):
    user = db_user.query(User).filter(User.username == login_u.username).first()
    access_token = Authorize.create_access_token(subject=user.username, fresh=True)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username"
        )
    hashed_pass = user.password
    if not verify_password(login_u.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/todo/", response_model=TodoSchema)
def create_todo(
        todo: schemas.TodoSchemaCreate,
        Authorize: AuthJWT = Depends(),
        db_work: Session = Depends(get_db)
):
    Authorize.jwt_required()
    return crud.create_todo(db=db_work, todo=todo)


@router.post("/todo_items/", response_model=TodoItemsSchema)
def create_items_for_work(
        todo_items: schemas.TodoItemsSchemaCreate, db_work: Session = Depends(get_db)
):
    return crud.create_todo_items(db=db_work, todo_items=todo_items)


@router.get("/todo/", response_model=List[TodoSchemaById])
def read_todo(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    items = crud.get_todo(db)
    Authorize.jwt_required()
    if db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return items


@router.get("/todo_items/", response_model=List[TodoItemsSchema])
def read_todo(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    items_desc = crud.get_todo_items(db)
    Authorize.jwt_required()
    return items_desc


@router.put("/todo/{id}/", response_model=TodoSchema)
def update_todo(todo_update: schemas.TodoSchemaCreate, id: int, db_update: Session = Depends(get_db),
                Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    crud.update_todo(db=db_update, todo=todo_update, id=id)
    return crud.get_todo_id(db=db_update, id=id)


@router.get("/todo/{id}/", response_model=TodoSchema)
def read_todo_id(id: int, status: Union[int, None] = Query(default=None), db: Session = Depends(get_db),
                 Authorize: AuthJWT = Depends()):
    items_id = crud.get_todo_id(db, id=id)
    Authorize.jwt_required()
    todo_items = db.query(ToDoItems).filter(ToDoItems.todo_id == id)
    if status:
        todo_items = todo_items.filter(ToDoItems.status == TodoStatus(status).name)
    items_id.todo_items = todo_items.all()
    return items_id


@router.delete("/todo/{id}/")
def delete_todo(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    crud.delete_todo(db, id=id)
    return {"msg": "data Deleted Successfully"}


@router.get("/todo_items/{id}/", response_model=TodoItemsSchemaById)
def read_todo_items_id(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    desc_id = crud.get_todo_items_id(db, id=id)
    # if status == 0 and not status:
    #     desc_id.todo_items = db.query(ToDoItems).filter(ToDoItems.status == TodoStatus(status).name).all()
    if desc_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    return desc_id


@router.put("/todo_items/{id}/", response_model=TodoItemsSchema)
def update_todo_items(todo_items_update: schemas.TodoItemsSchemaCreate, id: int, db_update: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends()):
    print(todo_items_update)
    Authorize.jwt_required()
    crud.update_todo_items(db=db_update, todo_items=todo_items_update, id=id)
    return crud.get_todo_items_id(db=db_update, id=id)


@router.delete("/todo_items/{id}/")
def delete_todo_items(id: int, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    desc_id = crud.get_todo_items_id(db, id=id)
    Authorize.jwt_required()
    print(desc_id)
    if not desc_id:
        raise HTTPException(status_code=404, detail="Data not found")
    crud.delete_todo_items(db, id=id)

    return {"msg": "data Deleted Successfully"}
