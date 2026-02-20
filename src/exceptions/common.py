"""
Common exceptions
"""

from fastapi import HTTPException, status


class BadRequestDataException(HTTPException):
    def __init__(self, detail: str = "Invalid request data"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NegativeBalanceException(HTTPException):
    def __init__(self, detail: str = "Insufficient funds on balance"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

