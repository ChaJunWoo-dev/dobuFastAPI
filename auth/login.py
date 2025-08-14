from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from models.user import User
import uuid
from crud.user import authenticate_user, get_user
from redisConfig import rd
from starlette.config import Config
from database import get_db

config = Config(".env")

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 1

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class RefreshTokenData(BaseModel):
    refresh_token: str


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")

        if rd.get(jti):
            raise HTTPException(status_code=401, detail="Token has been blacklisted")

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, id=token_data.user_id)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(
        db=db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id}, expires_delta=refresh_token_expires
    )

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh")
async def refresh_access_token(
    refresh_token: str = Form(...), db: Session = Depends(get_db)
) -> Token:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, id=token_data.user_id)

    if user is None:
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.delete("/delete_account")
async def delete_account(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    jti = payload.get("jti")

    if jti:
        rd.setex(jti, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "blacklisted")

    return {"msg": "User account has been deleted successfully"}
