"""
Payments models
"""

import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.utils.enums import Currency, PaymentTransactionStatus


class PaymentTransaction(BaseModel):
    __tablename__ = "transactions"

    from_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    to_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    currency: Mapped[Currency] = mapped_column(
        Enum(Currency), default=Currency.USD, server_default=Currency.USD.value, nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    status: Mapped[PaymentTransactionStatus] = mapped_column(
        Enum(PaymentTransactionStatus),
        default=PaymentTransactionStatus.PENDING,
        server_default=PaymentTransactionStatus.PENDING.value,
        nullable=False,
    )

    from_user: Mapped["User"] = relationship("User", back_populates="transactions_from_me", foreign_keys=[from_user_id])
    to_user: Mapped["User"] = relationship("User", back_populates="transactions_to_me", foreign_keys=[to_user_id])

    __table_args__ = (CheckConstraint("amount >= 0", name="check_transaction_amount_positive"),)
