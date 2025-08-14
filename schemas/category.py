from pydantic import BaseModel
from typing import Annotated
from typing import Optional

Id = Annotated[int, ...]


class CategoryBase(BaseModel):
    sub_id: Id
    name: str
    icon: str
    color: str
    visible: bool
    chart: bool


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: Id
    owner_id: Id

    class Config:
        from_attributes = True
