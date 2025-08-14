from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.consume_history import ConsumeHistCreate
from auth.login import get_current_active_user
from services import get_3month_range
from crud.consume import (
    get_consume_history,
    create_consume_hist,
    delete_consume_hist,
    update_consume_hist,
)
from crud.user import get_user
from crud.category import get_user_category_by_name
from database import get_db

router = APIRouter()


@router.get("")
def read_consume_history(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    date_list = get_3month_range(0, 0)
    user = get_user(db, id=current_user.id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    consume_hist_list = []

    for i in range(0, 6, 2):
        consume_history = get_consume_history(
            db,
            user_id=current_user.id,
            start_date=date_list[i],
            end_date=date_list[i + 1],
        )

        if len(consume_history) == 0:
            continue

        consume_hist_list.append(consume_history)

    return consume_hist_list


@router.post("/add/new_history")
def create_consume_history(
    new_hist: ConsumeHistCreate,
    category_name: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    category = get_user_category_by_name(
        category_name=category_name, db=db, user_id=current_user.id
    )

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return create_consume_hist(
        db=db, u_id=current_user.id, c_id=category.id, new_hist=new_hist
    )


class editSchema(ConsumeHistCreate):
    editItemId: int


@router.put("/edit/history")
def update_consume_history(
    edit_data: editSchema,
    category_name: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    category = get_user_category_by_name(
        category_name=category_name, db=db, user_id=current_user.id
    )

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return update_consume_hist(
        db=db, user_id=current_user.id, category=category, edit_data=edit_data
    )


@router.delete("/{hist_id}")
def delete_consume_history(
    hist_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return delete_consume_hist(db, hist_id=hist_id, user_id=current_user.id)
