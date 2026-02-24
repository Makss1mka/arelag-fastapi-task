"""
Payments schemas
"""

from datetime import datetime
from decimal import Decimal
import uuid
from pydantic import BaseModel, ConfigDict, Field

from src.utils.enums import Currency, PaymentTransactionStatus


#
# RESPONSES
#

class PaymentTransactionResponseModel(BaseModel):
    """
    Response model for payment transaction model
    """

    id: uuid.UUID
    from_user_id: uuid.UUID
    to_user_id: uuid.UUID
    currency: Currency
    status: PaymentTransactionStatus
    amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

#
# REQUESTS
#

class PaymentTransactionCreateRequestModel(BaseModel):
    """
    Request model for creating payment transaction
    """

    currency: Currency = Field(...)
    amount: Decimal = Field(..., gt=0, lt=99999)
    send_to: uuid.UUID
