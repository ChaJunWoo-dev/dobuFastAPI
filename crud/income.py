from sqlalchemy.orm import Session
from models.income import Income
from fastapi import HTTPException


def get_income(db: Session, user_id: int):
    db_income = db.query(Income).filter(Income.user_id == user_id).first()

    if db_income is None:
        raise HTTPException(status_code=404, detail="income not found")

    return db_income


def update_income(db: Session, udpated_income: int, user_id: int):
    db_income = get_income(db, user_id=user_id)

    if db_income is None:
        raise HTTPException(status_code=404, detail="income not found")

    db_income.cur_income = udpated_income
    db.commit()
    db.refresh(db_income)

    return db_income
