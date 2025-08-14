from __future__ import annotations
from sqlalchemy import Integer, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base


class Income(Base):
    __tablename__ = "income"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cur_income: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pre_income: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    two_month_ago_income: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    last_updated_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    user = relationship("User", back_populates="income")
