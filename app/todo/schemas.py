from typing import Union

from pydantic import BaseModel

from app.todo.constants import TodoStatus


class TodoSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


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
