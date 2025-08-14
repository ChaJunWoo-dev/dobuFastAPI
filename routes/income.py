from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.income import Income
from crud.income import get_income, update_income
from auth.login import get_current_active_user
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from database import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/get/income", response_model=Income)
def read_income(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    income = get_income(db, user_id=current_user.id)

    return income


class IncomeSchema(BaseModel):
    new_income: int


@router.put("/update/income", response_model=Income)
def update_income_a(
    request: IncomeSchema,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if request.new_income > 1_000_000_000:
        raise HTTPException(status_code=406, detail="over value")

    new_income = update_income(
        db=db, udpated_income=request.new_income, user_id=current_user.id
    )

    return new_income
