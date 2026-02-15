"""
Payments models
"""

import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.utils.enums import CurrencyEnum, TransactionStatusEnum


class Transaction(BaseModel):
    __tablename__ = "transactions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    currency: Mapped[CurrencyEnum] = mapped_column(
        Enum(CurrencyEnum), default=CurrencyEnum.USD, server_default=CurrencyEnum.USD.value, nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    status: Mapped[TransactionStatusEnum] = mapped_column(
        Enum(TransactionStatusEnum),
        default=TransactionStatusEnum.PENDING,
        server_default=TransactionStatusEnum.PENDING.value,
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="transactions")

    __table_args__ = (CheckConstraint("amount >= 0", name="check_transaction_amount_positive"),)
