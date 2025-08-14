from sqlalchemy.orm import Session
from models.card import Card
from fastapi import HTTPException


def get_card(db: Session, user_id: int):
    db_budget = db.query(Card).filter(Card.user_id == user_id).first()

    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")

    return db_budget
