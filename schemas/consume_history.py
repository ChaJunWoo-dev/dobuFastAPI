from pydantic import BaseModel
from datetime import date
from typing import Optional
from typing import Annotated

Id = Annotated[int, ...]


class ConsumeHistBase(BaseModel):
    receiver: str
    date: date
    amount: int
    installment: int
    card: Optional[str] = None
    fixed_id: Optional[Id] = None


class ConsumeHistCreate(ConsumeHistBase):
    pass


class ConsumeHist(ConsumeHistBase):
    id: Id
    user_id: Id
    category_id: Id

    class Config:
        from_attributes = True
