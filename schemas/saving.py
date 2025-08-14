from pydantic import BaseModel
from datetime import date
from typing import Annotated

Id = Annotated[int, ...]


class SavingBase(BaseModel):
    date: date
    receiver: str
    amount: int


class SavingCreate(SavingBase):
    pass


class Saving(SavingBase):
    id: Id
    user_id: Id

    class Config:
        from_attributes = True
