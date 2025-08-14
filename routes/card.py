from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
from crud.card import get_card
from auth.login import get_current_active_user
from fastapi.security import OAuth2PasswordBearer
from database import get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/get/card.list")
def read_cards(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    cards = get_card(db, user_id=current_user.id)

    return cards
