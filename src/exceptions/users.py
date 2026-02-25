"""
Users exceptions
"""

from fastapi import HTTPException, status


class UserAlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "User with this data already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UserNotExistsException(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UserAlreadyBlockedException(HTTPException):
    def __init__(self, detail: str = "User is already blocked"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UserAlreadyActiveException(HTTPException):
    def __init__(self, detail: str = "User is already active"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UserBalanceNotExistsException(HTTPException):
    def __init__(self, detail: str = "User balance with this data not exists"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
