from sqlalchemy.orm import Session
from models.consume_history import ConsumeHist
from models.category import Category
from schemas.consume_history import ConsumeHistCreate
from schemas.fixed_consume import FixedConsume
from fastapi import HTTPException
from redisConfig import rd
import json
from datetime import datetime
from sqlalchemy import select
from services import date_converter
from datetime import date
import calendar
from crud.total import del_total_data


def getYM(date):
    return date.strftime("%Y-%m")


def create_consume_hist(db: Session, new_hist: ConsumeHistCreate, c_id: int, u_id: int):
    year_month = str(new_hist.date)[:7]
    cache_key = f"user:{u_id}:consume_hist:{year_month}"
    cached_data = rd.get(cache_key)

    if cached_data:
        data_list = json.loads(cached_data)
    else:
        data_list = []

    db_hist = ConsumeHist(
        receiver=new_hist.receiver,
        date=new_hist.date,
        amount=new_hist.amount,
        user_id=u_id,
        fixed_id=None,
        category_id=c_id,
        card=new_hist.card,
        installment=new_hist.installment,
    )

    db.add(db_hist)
    db.commit()
    db.refresh(db_hist)
    del_total_data(user_id=u_id)

    category = db.query(Category).filter(Category.id == c_id).first()

    data_list.append(
        {
            "id": db_hist.id,
            "receiver": db_hist.receiver,
            "date": db_hist.date.strftime("%Y-%m-%d"),
            "amount": db_hist.amount,
            "installment": db_hist.installment,
            "card": db_hist.card,
            "fixed_id": db_hist.fixed_id,
            "sub_id": category.sub_id,
            "icon": category.icon,
            "name": category.name,
            "color": category.color,
            "chart": category.chart,
            "visible": category.visible,
        }
    )

    rd.set(cache_key, json.dumps(data_list), ex=60 * 5)
    cached_data = rd.get(cache_key)

    if cached_data:
        data_list = json.loads(cached_data)
        new_data_date = new_hist.date.strftime("%Y-%m-%d")
        filtered_data = [item for item in data_list if item["date"] == new_data_date]
    return filtered_data


def get_consume_history(db: Session, user_id: int, start_date: str, end_date: str):
    year_month = start_date[:7]
    cache_key = f"user:{user_id}:consume_hist:{year_month}"
    cached_data = rd.get(cache_key)

    if cached_data:
        restored_data = json.loads(cached_data)
        return {year_month: restored_data}

    stmt = (
        select(
            ConsumeHist.id,
            ConsumeHist.receiver,
            ConsumeHist.date,
            ConsumeHist.amount,
            ConsumeHist.installment,
            ConsumeHist.card,
            ConsumeHist.fixed_id,
            Category.sub_id,
            Category.icon,
            Category.name,
            Category.color,
            Category.chart,
            Category.visible,
        )
        .join(Category, ConsumeHist.category_id == Category.id)
        .filter(
            ConsumeHist.user_id == user_id,
            ConsumeHist.date >= start_date,
            ConsumeHist.date <= end_date,
        )
    )

    data = db.execute(stmt).fetchall()

    if len(data) > 0:
        data_group = [
            {
                "id": row.id,
                "receiver": row.receiver,
                "date": row.date.isoformat(),
                "amount": row.amount,
                "installment": row.installment,
                "fixed_id": row.fixed_id,
                "card": row.card if row.card else "",
                "sub_id": row.sub_id,
                "icon": row.icon,
                "name": row.name,
                "color": row.color,
                "chart": row.chart,
                "visible": row.visible,
            }
            for row in data
        ]

        data_dict = {year_month: data_group}
        rd.set(cache_key, json.dumps(data_group, default=date_converter), ex=60 * 5)
        return data_dict
    else:
        return {}


def delete_consume_hist(db: Session, hist_id: int, user_id: int):
    db_hist = get_consume_hist_by_id(db=db, hist_id=hist_id, user_id=user_id)

    if db_hist is None:
        raise HTTPException(status_code=404, detail="Consume history not found")

    year_month = str(db_hist.date)[:7]
    cache_key = f"user:{user_id}:consume_hist:{year_month}"
    cached_data = rd.get(cache_key)

    if cached_data:
        data_list = json.loads(cached_data)
    else:
        data_list = []

    if len(data_list) != 0:
        for item in data_list:
            if item["id"] == db_hist.id:
                data_list.remove(item)

                break

    rd.set(cache_key, json.dumps(data_list), ex=60 * 5)
    cached_data = rd.get(cache_key)

    if cached_data:
        data_list = json.loads(cached_data)
        data_date = db_hist.date.strftime("%Y-%m-%d")
        filtered_data = [item for item in data_list if item["date"] == data_date]

    db.delete(db_hist)
    db.commit()

    del_total_data(user_id=user_id)
    return filtered_data


def get_consume_hist_by_id(db: Session, hist_id: int, user_id: int):
    db_hist = (
        db.query(ConsumeHist)
        .filter(ConsumeHist.id == hist_id, ConsumeHist.user_id == user_id)
        .first()
    )

    if db_hist is None:
        raise HTTPException(status_code=404, detail="Consume history not found")

    return db_hist


class editSchema(ConsumeHistCreate):
    editItemId: int


def update_consume_hist(
    db: Session, edit_data: editSchema, category: Category, user_id: int
):
    year_month = str(edit_data.date)[:7]
    cache_key = f"user:{user_id}:consume_hist:{year_month}"
    cached_data = rd.get(cache_key)

    if cached_data:
        data_list = json.loads(cached_data)
    else:
        data_list = []

    db_hist = get_consume_hist_by_id(
        db=db, hist_id=edit_data.editItemId, user_id=user_id
    )

    if db_hist is None:
        raise HTTPException(status_code=404, detail="Consume history not found")

    db_hist.receiver = edit_data.receiver
    db_hist.date = edit_data.date
    db_hist.amount = edit_data.amount
    db_hist.card = edit_data.card
    db_hist.fixed_id = edit_data.fixed_id
    db_hist.installment = edit_data.installment
    db_hist.category_id = category.id

    for item in data_list:
        if item["id"] == db_hist.id:
            item.update(
                {
                    "id": db_hist.id,
                    "receiver": edit_data.receiver,
                    "date": edit_data.date.strftime("%Y-%m-%d"),
                    "amount": edit_data.amount,
                    "installment": db_hist.installment,
                    "fixed_id": db_hist.fixed_id,
                    "card": edit_data.card,
                    "sub_id": category.sub_id,
                    "icon": category.icon,
                    "name": category.name,
                    "color": category.color,
                    "chart": category.chart,
                    "visible": category.visible,
                }
            )

            break

    rd.set(cache_key, json.dumps(data_list), ex=60 * 5)
    cached_data = rd.get(cache_key)

    if cached_data:
        data_list = json.loads(cached_data)
        new_data_date = db_hist.date.strftime("%Y-%m-%d")
        filtered_data = [item for item in data_list if item["date"] == new_data_date]

    db.commit()
    db.refresh(db_hist)
    del_total_data(user_id=user_id)

    return filtered_data


def add_fixed_consume(
    db: Session, fixed_consume: FixedConsume, add_date: date, user_id: int
):
    year_month = str(add_date)[:7]
    current_date = datetime.today().date()
    year_diff = current_date.year - add_date.year
    month_diff = current_date.month - add_date.month
    total_months = year_diff * 12 + month_diff

    months_to_add = [
        (
            add_date.year + (add_date.month + i - 1) // 12,
            (add_date.month + i - 1) % 12 + 1,
        )
        for i in range(total_months + 1)
    ]
    if len(months_to_add) != 0:
        del_total_data(user_id=user_id)

    for year, month in months_to_add:
        try:
            add_date_for_month = date(year, month, fixed_consume.start_date.day)
        except:
            _, last_day_of_month = calendar.monthrange(year, month)
            if add_date_for_month.day > last_day_of_month:
                add_date_for_month = date(year, month, last_day_of_month)

        year_month = f"{year}-{month}"
        cache_key = f"user:{user_id}:consume_hist:{year_month}"
        cached_data = rd.get(cache_key)

        if cached_data:
            data_list = json.loads(cached_data)
        else:
            data_list = []

        db_consume = ConsumeHist(
            receiver=fixed_consume.receiver,
            date=add_date_for_month,
            amount=fixed_consume.amount,
            card=fixed_consume.card,
            installment=0,
            user_id=fixed_consume.user_id,
            category_id=fixed_consume.category_id,
            fixed_id=fixed_consume.id,
        )

        db.add(db_consume)
        db.commit()
        db.refresh(db_consume)

        category = (
            db.query(Category).filter(Category.id == db_consume.category_id).first()
        )

        data_list.append(
            {
                "id": db_consume.id,
                "receiver": db_consume.receiver,
                "date": db_consume.date.strftime("%Y-%m-%d"),
                "amount": db_consume.amount,
                "installment": db_consume.installment,
                "card": db_consume.card,
                "fixed_id": db_consume.fixed_id,
                "sub_id": category.sub_id,
                "icon": category.icon,
                "name": category.name,
                "color": category.color,
                "chart": category.chart,
                "visible": category.visible,
            }
        )

        rd.set(cache_key, json.dumps(data_list), ex=60 * 5)

    return
