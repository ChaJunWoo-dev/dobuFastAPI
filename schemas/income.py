from pydantic import BaseModel
from typing import Annotated

Id = Annotated[int, ...]


class IncomeBase(BaseModel):
    cur_income: int
    pre_income: int
    two_month_ago_income: int


class IncomeCreate(IncomeBase):
    pass


class Income(IncomeBase):
    id: Id
    user_id: Id

    class Config:
        from_attributes = True
