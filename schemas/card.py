from pydantic import BaseModel
from datetime import date
from typing import Annotated

Id = Annotated[int, ...]


class CardBase(BaseModel):
    name: str
    company: str
    last_updated_date: date


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: Id
    user_id: Id

    class Config:
        from_attributes = True
