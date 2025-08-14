from sqlalchemy.orm import Session
from models.consume_history import ConsumeHist
from redisConfig import rd
from sqlalchemy import select, func


def del_total_data(user_id: int):
    total_key_pattern = f"user:{user_id}:consume_hist_total:*"
    matching_keys = rd.keys(total_key_pattern)

    for key in matching_keys:
        rd.delete(key)


def get_consume_hist_total(
    db: Session, user_id: int, start_date: str, end_date: str
) -> int:
    cache_key = f"user:{user_id}:consume_hist_total:{start_date}:{end_date}"
    cached_data = rd.get(cache_key)

    if cached_data:
        return cached_data

    stmt = select(func.sum(ConsumeHist.amount).label("total_amount")).filter(
        ConsumeHist.user_id == user_id,
        ConsumeHist.date >= start_date,
        ConsumeHist.date <= end_date,
    )

    result = db.execute(stmt).scalar_one_or_none()
    total_amount = result if result is not None else 0

    rd.set(cache_key, total_amount, ex=60 * 5)

    return total_amount
