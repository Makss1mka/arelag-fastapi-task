"""
Payments models
"""

import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.utils.enums import Currency, TransactionStatus


class Transaction(BaseModel):
    __tablename__ = "transactions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    currency: Mapped[Currency] = mapped_column(
        Enum(Currency), default=Currency.USD, server_default=Currency.USD.value, nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus),
        default=TransactionStatus.PENDING,
        server_default=TransactionStatus.PENDING.value,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="transactions")

    __table_args__ = (CheckConstraint("amount >= 0", name="check_transaction_amount_positive"),)
