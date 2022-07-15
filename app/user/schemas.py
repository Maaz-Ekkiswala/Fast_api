from typing import Union

from pydantic import BaseModel


class UserAuth(BaseModel):
    username: str
    email: str
    phone: Union[str, None]
    password: str

    class Config:
        orm_mode = True


class UserForTodo(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    phone: str

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
