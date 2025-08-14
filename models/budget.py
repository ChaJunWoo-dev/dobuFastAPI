from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cur_budget: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    pre_budget: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    last_updated_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    user = relationship("User", back_populates="budget")
