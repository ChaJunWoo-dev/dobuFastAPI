from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.budget import Budget
from models.user import User
from crud.budget import get_budget, update_budget
from auth.login import get_current_active_user
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from database import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/get/budget")
def read_budget(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    budget = get_budget(db, user_id=current_user.id)

    if budget is None:
        raise HTTPException(status_code=404, detail="Budget is None")

    return budget


class BudgetSchema(BaseModel):
    new_budget: int


@router.put("/update/budget")
def update_buget_by_user(
    request: BudgetSchema,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if request.new_budget > 1_000_000_000:
        raise HTTPException(status_code=406, detail="over value")

    new_budget = update_budget(
        db=db, new_budget=request.new_budget, user_id=current_user.id
    )

    return new_budget
