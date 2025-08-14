from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional, Annotated

Id = Annotated[int, ...]


class RepeatCycle(str, Enum):
    monthly = "monthly"
    yearly = "yearly"


class FixedConsumeBase(BaseModel):
    receiver: str
    start_date: date
    amount: int
    card: Optional[str] = None
    repeat_cycle: RepeatCycle = RepeatCycle.monthly
    next_date: date


class FixedConsumeCreate(FixedConsumeBase):
    pass


class FixedConsume(FixedConsumeBase):
    id: Id
    user_id: Id
    category_id: Id

    class Config:
        from_attributes = True
