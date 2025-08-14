from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
from auth.login import get_current_active_user
from pydantic import BaseModel
from services import all_categories
from crud.category import (
    get_user_categories,
    get_chart_categories,
    update_invisible_categories,
)
from database import get_db

router = APIRouter()


@router.get("/categories")
def read_user_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    categories = get_user_categories(db=db, user_id=current_user.id)

    return categories


@router.get("/categories/for_chart/data")
def read_category_ids(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    category_ids = get_chart_categories(db=db, user_id=current_user.id)

    return category_ids


@router.get("/all_categories")
def get_all_categories():
    return all_categories()


class UpdateRequest(BaseModel):
    update_list: list


@router.put("/categories/edit/user_sync")
def sync_invisible(
    dataSchema: UpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return update_invisible_categories(
        db=db, user_id=current_user.id, data_list=dataSchema.update_list
    )
