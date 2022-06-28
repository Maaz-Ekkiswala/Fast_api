from typing import Union, List

from pydantic import BaseModel

from app.todo.constants import TodoStatus


class TodoSchemaCreate(BaseModel):
    title: str

    class Config:
        orm_mode = True


class TodoItemsSchemaCreate(BaseModel):
    todo_id: int
    title: str
    status: TodoStatus
    description: Union[str, None] = None

    class Config:
        orm_mode = True


class TodoItemsSchema(BaseModel):
    id: int
    todo_id: int
    title: str
    status: TodoStatus
    description: Union[str, None] = None

    class Config:
        orm_mode = True


class TodoSchema(BaseModel):
    id: int
    title: str
    todo_items: List[TodoItemsSchema]

    class Config:
        orm_mode = True


class TodoSchemaById(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class TodoItemsSchemaById(BaseModel):
    id: int
    title: str
    status: TodoStatus
    description: Union[str, None] = None
    todo: TodoSchemaById

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    username: str
    email: str
    phone: Union[str, None] = None
    password: str

    class Config:
        orm_mode = True


class UserInDB(UserAuth):
    hashed_password: str


class UserOut(BaseModel):
    username: str
    email: str
    phone: int

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    # token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Union[str, None] = None


class Login(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True