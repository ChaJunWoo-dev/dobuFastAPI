from sqlalchemy.orm import Session
from auth.hash_pwd import hash_password, verify_password
from models.user import User
from models.budget import Budget
from models.income import Income
from schemas.user import UserCreate
from crud.category import add_categories_for_signup, update_chart_categories


def get_user(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_nickname(db: Session, nickname: str):
    return db.query(User).filter(User.nickname == nickname).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()

    return {"detail": "User deleted"}


def update_nickname(new_nickname: str, db: Session, db_user: User):
    db_user.nickname = new_nickname
    db.commit()

    return {"detail": "Nickname updated"}


def signup_user(db: Session, new_user: UserCreate, selected_categories: list):
    try:
        hashed_password = hash_password(new_user.password)

        db_user = User(
            email=new_user.email,
            hashed_password=hashed_password,
            nickname=new_user.nickname,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        new_budget = Budget(user_id=db_user.id, cur_budget=0, pre_budget=0)
        new_income = Income(
            user_id=db_user.id, cur_income=0, pre_income=0, two_month_ago_income=0
        )

        db.add(new_budget)
        db.add(new_income)
        db.commit()

        add_categories_for_signup(db=db, user_id=db_user.id)
        update_chart_categories(
            db=db, data_list=selected_categories, user_id=db_user.id
        )

        return db_user

    except:
        db.rollback()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if user and verify_password(password, user.hashed_password):
        return user

    return None


def decode_token(db: Session, token):
    user = get_user_by_email(db, token)

    return user
