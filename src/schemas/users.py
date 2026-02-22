"""
User schemas
"""

import uuid
from pydantic import BaseModel
from typing import Optional, List

from src.utils.enums import Currency, UserStatus


#
# RESPONSES
#

class UserBalanceResponseModel(BaseModel):
    """
    Response model for user balance
    """

    currency: Currency
    amount: float


class UserResponseModel(BaseModel):
    """
    Response model for user
    """

    id: uuid.UUID
    email: str
    status: UserStatus
    balances: Optional[List[UserBalanceResponseModel]] = None


#
# REQUESTS
#

class UserCreateRequestModel(BaseModel):
    """
    User create request model
    """

    email: str


class UserUpdateRequestModel(BaseModel):
    """
    User update request model
    """

    status: UserStatus
