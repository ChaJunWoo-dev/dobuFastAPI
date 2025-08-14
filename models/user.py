from __future__ import annotations
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(50))
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    image: Mapped[str] = mapped_column(
        String(255), default="assets/images/default_profile.svg", nullable=False
    )

    items = relationship(
        "Category",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    consume_histories = relationship(
        "ConsumeHist",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    budget = relationship(
        "Budget",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    card = relationship(
        "Card",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    fixed_consume = relationship(
        "FixedConsume",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    saving = relationship(
        "Saving",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    income = relationship(
        "Income",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
