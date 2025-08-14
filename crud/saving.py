from sqlalchemy.orm import Session
from models.saving import Saving
from schemas.saving import SavingCreate
from fastapi import HTTPException
from sqlalchemy import extract
from datetime import datetime, timedelta
from sqlalchemy import extract


def get_recent_months():
    today = datetime.today()
    current_month = today.replace(day=1)

    last_month = current_month - timedelta(days=1)
    last_month = last_month.replace(day=1)

    two_months_ago = last_month - timedelta(days=1)
    two_months_ago = two_months_ago.replace(day=1)

    current_month_str = current_month.strftime("%m")
    last_month_str = last_month.strftime("%m")
    two_months_ago_str = two_months_ago.strftime("%m")

    return [current_month_str, last_month_str, two_months_ago_str]


def read_saving_by_recent_months(db: Session, user_id: int):
    recent_months = get_recent_months()
    grouped = {month: [] for month in recent_months}

    results = (
        db.query(
            extract("month", Saving.date).label("month"),
            Saving.id,
            Saving.receiver,
            Saving.amount,
            Saving.date,
        )
        .filter(Saving.user_id == user_id)
        .all()
    )

    for (
        month,
        id,
        receiver,
        amount,
        date,
    ) in results:
        month_str = f"{int(month):02d}"

        if month_str in grouped:
            grouped[month_str].append(
                {
                    "receiver": receiver,
                    "amount": amount,
                    "date": date,
                    "id": id,
                }
            )

    return grouped


def add_saving(db: Session, new_saving: SavingCreate, user_id: int):
    saving = Saving(
        date=new_saving.date,
        receiver=new_saving.receiver,
        amount=new_saving.amount,
        user_id=user_id,
    )

    db.add(saving)
    db.commit()
    db.refresh(saving)

    return saving


def read_saving_list(db: Session, user_id: int):
    savings = db.query(Saving).filter(Saving.user_id == user_id).all()

    if not savings:
        raise HTTPException(status_code=404, detail="savings not found")

    return savings


def del_saving(db: Session, user_id: int, item_id: int):
    saving = (
        db.query(Saving).filter(Saving.id == item_id, Saving.user_id == user_id).first()
    )

    if not saving:
        raise HTTPException(status_code=404, detail="saving not found")

    try:
        db.delete(saving)
        db.commit()

        return
    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500, detail=f"Failed to delete saving: {str(e)}"
        )
