from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models.user import User
from schemas.user import User, UserCreate
from database import get_db
from auth.login import get_current_user, get_current_active_user
from auth.hash_pwd import hash_password, verify_password
from crud.user import (
    get_user_by_email,
    get_user_by_nickname,
    get_users,
    get_user,
    update_nickname,
    signup_user,
    delete_user,
)

router = APIRouter()


class SignUpRequest(BaseModel):
    email: str
    password: str
    nickname: str
    categories: list


@router.post("/signup")
def create_user(new_user: SignUpRequest, db: Session = Depends(get_db)):
    try:
        db_user = get_user_by_email(db, email=new_user.email)

        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_create = UserCreate(
            email=new_user.email,
            password=new_user.password,
            nickname=new_user.nickname,
            image="assets/images/default_profile.svg",
        )

        signup_user(db, new_user=user_create, selected_categories=new_user.categories)
    except Exception:
        db.rollback()

        raise HTTPException(status_code=500, detail="Internal server error")

    return {"message": "Signup successful"}


@router.get("/check_use/nickname")
def check_nickname(nickname: str, db: Session = Depends(get_db)):
    db_user = get_user_by_nickname(db=db, nickname=nickname)

    if db_user:
        raise HTTPException(status_code=400, detail="Nickname already registered")

    return True


@router.get("/check_use/email")
def check_email(email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return True


@router.get("/get/me")
async def read_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "nickname": current_user.nickname,
        "image": current_user.image,
    }


@router.get("/get/user/all")
def read_user_all(db: Session = Depends(get_db)):
    return get_users(db)


@router.delete("/delete/user")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)

    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist")

    delete_user(db, db_user)

    return {"msg": "User deleted successfully"}


class ChangePassword(BaseModel):
    passwd: str
    new_passwd: str


@router.put("/update/password")
def password_update(
    request: ChangePassword,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    passwd = request.passwd
    new_passwd = request.new_passwd
    db_user = get_user(db, current_user.id)

    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist")

    if not verify_password(passwd, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    db_user.hashed_password = hash_password(new_passwd)
    db.commit()
    db.refresh(db_user)

    return {"msg": "Password updated successfully"}


class PasswordRequest(BaseModel):
    passwd: str


@router.post("/confirm/password")
def confirm_pwd(
    request: PasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    passwd = request.passwd
    db_user = get_user(db, current_user.id)

    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist")

    if not verify_password(passwd, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"msg": "Password correct"}


class ChangeNickname(BaseModel):
    new_nickname: str


@router.put("/update/nickname")
def nickname_update(
    request: ChangeNickname,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    new_nickname = request.new_nickname

    db_user = get_user_by_nickname(db=db, nickname=new_nickname)
    if db_user:
        raise HTTPException(status_code=400, detail="Nickname already registered")

    db_user = get_user(db, current_user.id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User does not exist")

    update_nickname(new_nickname, db, db_user)
    db.commit()
    db.refresh(db_user)

    return {"msg": "Nickname updated successfully"}
