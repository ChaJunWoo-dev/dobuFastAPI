from sqlalchemy.orm import Session
from models.category import Category
from fastapi import HTTPException
from services import all_categories


def get_user_category_by_id(db: Session, user_id: int, category_id: int):
    return (
        db.query(Category)
        .filter(Category.owner_id == user_id, Category.id == category_id)
        .first()
    )


def get_user_category_by_name(db: Session, user_id: int, category_name: str):
    return (
        db.query(Category)
        .filter(Category.owner_id == user_id, Category.name == category_name)
        .first()
    )


def add_categories_for_signup(db: Session, user_id: int):
    for category in all_categories():
        db_category = Category(
            owner_id=user_id,
            sub_id=category["sub_id"],
            icon=category["icon"],
            name=category["name"],
            color=category["color"],
        )
        db.add(db_category)

    db.commit()
    db.refresh(db_category)


def update_chart_categories(db: Session, selected_categories: list, user_id: int):
    if len(selected_categories) != 4:
        raise ValueError("선택한 카테고리가 4개가 아닙니다.")

    user_categories = get_user_categories(db=db, user_id=user_id)
    category_dict = {category.name: category for category in user_categories}

    for selected in selected_categories:
        if selected not in category_dict:
            raise ValueError(f"존재하지 않는 카테고리입니다: {selected}")

        category_dict[selected].chart = True

    db.commit()


def get_user_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.owner_id == user_id).all()


def get_user_categories_visible(db: Session, user_id: int):
    return db.query(Category).filter(
        Category.owner_id == user_id, Category.visible == True
    )


def get_user_categories_invisible(db: Session, user_id: int):
    return db.query(Category).filter(
        Category.owner_id == user_id, Category.visible == False
    )


def get_chart_categories(db: Session, user_id: int):
    return db.query(Category).filter(
        Category.owner_id == user_id, Category.chart == True
    )


def update_invisible_categories(db: Session, user_id: int, data_list: list):
    for category_id in data_list:
        db_category = get_user_category_by_id(
            db=db, user_id=user_id, category_id=category_id
        )
        if not db_category:
            raise HTTPException(status_code=404, detail="카테고리가 존재하지 않습니다")

        db_category.visible = not db_category.visible

    db.commit()
    db.refresh(db_category)

    return get_user_categories(db=db, user_id=user_id)
