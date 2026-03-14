"""
User models
"""

import uuid
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.utils.enums import Currency, UserStatus


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[Optional[str]] = mapped_column(String(63), unique=True, index=True, nullable=True)
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus), nullable=False, default=UserStatus.ACTIVE, server_default=UserStatus.ACTIVE.value
    )

    balances: Mapped[List["UserBalance"]] = relationship("UserBalance", back_populates="user")
    transactions_from_me: Mapped[List["PaymentTransaction"]] = relationship(
        "PaymentTransaction", back_populates="from_user", foreign_keys="[PaymentTransaction.from_user_id]"
    )
    transactions_to_me: Mapped[List["PaymentTransaction"]] = relationship(
        "PaymentTransaction", back_populates="to_user", foreign_keys="[PaymentTransaction.to_user_id]"
    )


class UserBalance(BaseModel):
    __tablename__ = "users_balances"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    currency: Mapped[Currency] = mapped_column(
        Enum(Currency), nullable=False, default=Currency.USD, server_default=Currency.USD.value
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0, server_default="0")

    user: Mapped["User"] = relationship("User", back_populates="balances", uselist=False)

    __table_args__ = (
        UniqueConstraint("user_id", "currency", name="uq_user_balance_user_currency"),
        CheckConstraint("amount >= 0", name="check_balance_amount_positive"),
    )
