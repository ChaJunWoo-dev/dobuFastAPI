from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from auth.login import get_current_active_user
from services import (
    get_current_month_range,
    get_current_week_range,
    get_today_range,
)
from crud.total import get_consume_hist_total
from database import get_db

router = APIRouter()


@router.get("/get/total/consume/period")
def read_period_total(
    startDate: str,
    endDate: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    period_total = get_consume_hist_total(
        db=db, user_id=current_user.id, start_date=startDate, end_date=endDate
    )

    if period_total is None or period_total == 0:
        raise HTTPException(status_code=404, detail="category_total_consume is None")

    return period_total


@router.get("/get/total/consume/period_this_MWD")
def read_period_total_month(
    MWD: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if MWD == "month":
        start_date, end_date = get_current_month_range()
    elif MWD == "week":
        start_date, end_date = get_current_week_range()
    else:
        start_date, end_date = get_today_range()

    period_total = get_consume_hist_total(
        db=db, user_id=current_user.id, start_date=start_date, end_date=end_date
    )

    if period_total is None:
        raise HTTPException(status_code=404, detail="category_total_consume is None")

    return period_total
