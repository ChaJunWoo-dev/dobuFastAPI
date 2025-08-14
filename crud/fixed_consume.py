from sqlalchemy.orm import Session
from models.fixed_consume import FixedConsume, RepeatCycle
from models.card import Card
from models.category import Category
from datetime import date
import datetime
from crud.consume import add_fixed_consume
import calendar
from fastapi import HTTPException
from schemas.params import AddFixedSchema


def calculate_next_date(start_date: date, repeat_cycle: str) -> date:
    current_date = datetime.datetime.today().date()

    if repeat_cycle == RepeatCycle.monthly:
        year = current_date.year + (current_date.month // 12)
        month = (current_date.month % 12) + 1

        day = start_date.day
        last_day_of_next_month = calendar.monthrange(year, month)[1]

        if day > last_day_of_next_month:
            day = last_day_of_next_month

        return date(year, month, day)

    raise ValueError(f"Unsupported repeat_cycle: {repeat_cycle}")


def process_monthly_expenses(db: Session):
    today = datetime.datetime.now().date()
    fixed_expenses = (
        db.query(FixedConsume).filter(FixedConsume.next_date == today).all()
    )

    for fixed_expense in fixed_expenses:
        try:
            add_fixed_consume(
                db=db,
                fixed_consume=fixed_expense,
                add_date=today,
                user_id=fixed_expense.user_id,
            )

            fixed_expense.next_date = calculate_next_date(
                fixed_expense.next_date, RepeatCycle.monthly
            )
        except Exception as e:
            print(f"Error during process_monthly_expenses execution: {e}")


def create_fixed_consume(
    db: Session, fixed_consume: AddFixedSchema, category: Category, user_id: int
):
    next_date = calculate_next_date(fixed_consume.date, RepeatCycle.monthly)
    try:
        db_fixed = FixedConsume(
            receiver=fixed_consume.receiver,
            start_date=fixed_consume.date,
            amount=fixed_consume.amount,
            card=fixed_consume.card,
            repeat_cycle=RepeatCycle.monthly,
            user_id=user_id,
            category_id=category.id,
            next_date=next_date,
        )

        db.add(db_fixed)
        db.commit()
        db.refresh(db_fixed)

        add_fixed_consume(
            db=db, fixed_consume=db_fixed, add_date=fixed_consume.date, user_id=user_id
        )

        return get_fixed_expense(db=db, user_id=user_id)
    except Exception:
        db.rollback()

        raise


def get_fixed_expense(db: Session, user_id: int):
    res = (
        db.query(
            FixedConsume.id,
            FixedConsume.receiver,
            FixedConsume.start_date,
            FixedConsume.amount,
            Category.name.label("category_name"),
            Card.name.label("name"),
        )
        .join(Category, Category.id == FixedConsume.category_id)
        .filter(FixedConsume.user_id == user_id)
        .all()
    )

    return [
        {
            "id": row[0],
            "receiver": row[1],
            "start_date": row[2],
            "amount": row[3],
            "category_name": row[4],
            "card": row[5],
        }
        for row in res
    ]


def del_fixed_expense(db: Session, user_id: int, item_id: int):
    fixed_consume = (
        db.query(FixedConsume)
        .filter(FixedConsume.id == item_id, FixedConsume.user_id == user_id)
        .first()
    )

    if not fixed_consume:
        raise HTTPException(status_code=404, detail="FixedConsume not found")

    try:
        db.delete(fixed_consume)
        db.commit()

        return fixed_consume.id
    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500, detail=f"Failed to delete FixedConsume: {str(e)}"
        )
