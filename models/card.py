from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, Date, ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Card(Base):
    __tablename__ = "cards"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_card_user_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    company: Mapped[str] = mapped_column(String(50), nullable=False)

    last_updated_date: Mapped[datetime] = mapped_column(
        Date,
        nullable=False,
        server_default=text("(CURRENT_DATE)"),
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    user = relationship("User", back_populates="cards")
