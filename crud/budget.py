from sqlalchemy.orm import Session
from models.budget import Budget
from schemas.budget import Budget
from fastapi import HTTPException
from crud.total import del_total_data


def get_budget(db: Session, user_id: int):
    db_budget = db.query(Budget).filter(Budget.user_id == user_id).first()

    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    return db_budget


def update_budget(db: Session, new_budget: Budget, user_id: int):
    budget = get_budget(db, user_id=user_id)

    if budget is None:
        raise HTTPException(status_code=404, detail="Budget is None")

    budget.cur_budget = new_budget

    db.commit()
    db.refresh(budget)

    return budget


def create_budget(db: Session, user_id: int):
    db_budget = Budget(cur_budget=0, pre_budget=0, user_id=user_id)

    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    del_total_data(user_id=user_id)

    return db_budget
