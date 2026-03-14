"""
User schemas
"""

import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.utils.enums import Currency, UserBalanceUpdateDirection, UserStatus

#
# RESPONSES
#


class UserBalanceResponseModel(BaseModel):
    """
    Response model for user balance
    """

    id: uuid.UUID
    currency: Currency
    amount: float

    model_config = ConfigDict(from_attributes=True)


class UserResponseModel(BaseModel):
    """
    Response model for user
    """

    id: uuid.UUID
    email: str
    status: UserStatus
    balances: Optional[List[UserBalanceResponseModel]] = None

    model_config = ConfigDict(from_attributes=True)


#
# REQUESTS
#


class UserCreateRequestModel(BaseModel):
    """
    User create request model
    """

    email: EmailStr = Field(..., min_length=10, max_length=50)


class UserUpdateRequestModel(BaseModel):
    """
    User update request model
    """

    status: UserStatus = Field(...)


class UserBalanceUpdateRequestModel(BaseModel):
    """
    Request model for updating one user balance
    """

    amount: int = Field(..., gt=0)
    direction: UserBalanceUpdateDirection = Field(...)
    currency: Currency = Field(...)
