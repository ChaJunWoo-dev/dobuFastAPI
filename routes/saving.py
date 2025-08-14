from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
from schemas.saving import SavingCreate
from auth.login import get_current_active_user
from crud.saving import (
    read_saving_list,
    add_saving,
    read_saving_by_recent_months,
    del_saving,
)
from fastapi.security import OAuth2PasswordBearer
from database import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/get/data")
def read_saving(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    savings = read_saving_list(db=db, user_id=current_user.id)

    return savings


@router.get("/group/data")
def read_saving_grouped(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    return read_saving_by_recent_months(db=db, user_id=current_user.id)


@router.post("/add/data")
def read_saving(
    new_saving: SavingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    add_saving(db=db, new_saving=new_saving, user_id=current_user.id)

    savings = read_saving_by_recent_months(db=db, user_id=current_user.id)

    return savings


@router.delete("/del/saving/{item_id}")
def remove_saving(
    item_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    del_saving(db=db, user_id=current_user.id, item_id=item_id)

    return read_saving_by_recent_months(db=db, user_id=current_user.id)
