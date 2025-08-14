from __future__ import annotations
from datetime import date
from sqlalchemy import Integer, String, Date, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class ConsumeHist(Base):
    __tablename__ = "consume_hist"
    __table_args__ = (Index("ix_consume_hist_date_user", "date", "user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    receiver: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    installment: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    card: Mapped[str | None] = mapped_column(String(50))
    fixed_id: Mapped[int | None] = mapped_column(
        ForeignKey("fixed_consume.id", ondelete="SET NULL"), nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True
    )

    user = relationship("User", back_populates="consume_histories")
    category = relationship("Category", back_populates="consume_histories")
    fixed_consume = relationship("FixedConsume", back_populates="consume_histories")
