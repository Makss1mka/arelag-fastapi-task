"""
User models
"""

import uuid
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.utils.enums import CurrencyEnum, UserStatusEnum


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[Optional[str]] = mapped_column(String(63), unique=True, index=True, nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[UserStatusEnum] = mapped_column(
        Enum(UserStatusEnum), nullable=False, default=UserStatusEnum.ACTIVE, server_default=UserStatusEnum.ACTIVE.value
    )

    balances: Mapped[List["UserBalance"]] = relationship("UserBalance", back_populates="user")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="user")


class UserBalance(BaseModel):
    __tablename__ = "users_balances"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    currency: Mapped[CurrencyEnum] = mapped_column(
        Enum(CurrencyEnum), nullable=False, default=CurrencyEnum.USD, server_default=CurrencyEnum.USD.value
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0, server_default="0")

    user: Mapped["User"] = relationship("User", back_populates="balances", uselist=False)

    __table_args__ = (
        UniqueConstraint("user_id", "currency", name="uq_user_balance_user_currency"),
        CheckConstraint("amount >= 0", name="check_balance_amount_positive"),
    )
