from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from auth.login import get_current_active_user
from crud.fixed_consume import (
    create_fixed_consume,
    get_fixed_expense,
    del_fixed_expense,
)
from crud.category import get_user_category_by_name
from database import get_db
from schemas.params import AddFixedSchema

router = APIRouter()


@router.post("/fixed-consume")
def add_fixed_expense(
    request: AddFixedSchema,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    category = get_user_category_by_name(
        category_name=request.category_name, db=db, user_id=current_user.id
    )

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    return create_fixed_consume(
        db=db, fixed_consume=request, category=category, user_id=current_user.id
    )


@router.get("/read/fixed-consume")
def fixed_expense(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    return get_fixed_expense(db=db, user_id=current_user.id)


@router.delete("/del/fixed-consume/{hist_id}")
def fixed_expense(
    hist_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return del_fixed_expense(db=db, user_id=current_user.id, item_id=hist_id)
