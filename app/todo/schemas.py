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
