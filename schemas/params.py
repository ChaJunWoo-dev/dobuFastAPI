from pydantic import BaseModel
from datetime import date
from typing import Optional


class AddFixedSchema(BaseModel):
    receiver: str
    date: date
    amount: int
    repeat: bool
    card: Optional[str] = None
    category_name: str
