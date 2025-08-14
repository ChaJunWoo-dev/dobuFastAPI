from pydantic import BaseModel, EmailStr
from typing import Annotated

Id = Annotated[int, ...]


class UserBase(BaseModel):
    email: EmailStr
    nickname: str
    image: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: Id
    disabled: bool

    class Config:
        from_attributes = True
