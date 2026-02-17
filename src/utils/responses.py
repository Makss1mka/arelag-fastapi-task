"""
Response models
"""

from typing import Optional, Any
from pydantic import BaseModel, Field
from src.utils.enums import ResponseTextStatus


class CommonResponseModel(BaseModel):
    """
    Common response model
    """

    status: ResponseTextStatus
    message: Optional[str] = None
    data: Optional[Any] = None
