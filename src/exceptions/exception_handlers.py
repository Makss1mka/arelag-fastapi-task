"""
Exception handlers
"""

from src.utils.enums import ResponseTextStatus
from src.utils.responses import CommonResponseModel

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, status

import logging

logger: logging.Logger = logging.getLogger(__name__)


async def http_exception_handler(req: Request, ex: HTTPException):
    """
    Exception handler for all HttpExceptions
    """

    return JSONResponse(
        status_code=ex.status_code,
        content=CommonResponseModel(
            status=ResponseTextStatus.EXCEPTION,
            message=ex.detail,
        ).model_dump(exclude_unset=True)
    )


async def pydantic_exception_handler(req: Request, exc: RequestValidationError):
    """
    Exception handler for pydantic validation exceptions
    """

    errors = []
    for error in exc.errors():
        field = " -> ".join(map(str, error.get("loc")))
        message = error.get("msg")
        error_type = error.get("type")

        errors.append({
            "field": field,
            "message": message,
            "type": error_type
        })

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=CommonResponseModel(
            status=ResponseTextStatus.EXCEPTION,
            message="Validation failed",
            data=errors
        ).model_dump()
    )


async def common_exception_handler(req: Request, ex: Exception):
    """
    Common exception handler
    """

    return JSONResponse(
        status_code=500,
        content=CommonResponseModel(
            status=ResponseTextStatus.EXCEPTION,
            message="Internal server error",
        ).model_dump(exclude_unset=True)
    )

