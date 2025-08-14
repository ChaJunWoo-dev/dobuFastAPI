from __future__ import annotations
from sqlalchemy import Boolean, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("owner_id", "sub_id", name="uq_category_owner_sub"),
        Index("ix_category_owner", "owner_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sub_id: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    icon: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False)
    visible: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    chart: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    owner = relationship("User", back_populates="items")
    consume_histories = relationship(
        "ConsumeHist", back_populates="category", passive_deletes=True
    )
    fixed_consume = relationship(
        "FixedConsume", back_populates="category", passive_deletes=True
    )
