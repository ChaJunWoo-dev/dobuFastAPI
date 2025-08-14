from __future__ import annotations
from datetime import date
import enum
from sqlalchemy import Integer, String, Date, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class RepeatCycle(enum.Enum):
    monthly = "monthly"
    weekly = "weekly"
    yearly = "yearly"


class FixedConsume(Base):
    __tablename__ = "fixed_consume"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    receiver: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    card: Mapped[str | None] = mapped_column(String(50))
    next_date: Mapped[date] = mapped_column(Date, nullable=False)
    repeat_cycle: Mapped[RepeatCycle] = mapped_column(
        SAEnum(RepeatCycle, name="repeat_cycle"),
        nullable=False,
        default=RepeatCycle.monthly,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )

    category = relationship("Category", back_populates="fixed_consume")
    user = relationship("User", back_populates="fixed_consume")
    consume_histories = relationship(
        "ConsumeHist", back_populates="fixed_consume", passive_deletes=True
    )
