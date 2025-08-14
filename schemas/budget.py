from datetime import date
from typing import Annotated
from pydantic import BaseModel, ConfigDict

Id = Annotated[int, ...]


class BudgetBase(BaseModel):
    cur_budget: int
    pre_budget: int
    last_updated_date: date


class BudgetCreate(BudgetBase):
    user_id: Id


class Budget(BudgetBase):
    id: Id
    user_id: Id
    model_config = ConfigDict(from_attributes=True)
