"""
Transaction exceptions
"""

from fastapi import HTTPException, status


class TransactionNotExistsException(HTTPException):
    def __init__(self, detail: str = "Transaction not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class TransactionDoesNotBelongToUserException(HTTPException):
    def __init__(self, detail: str = "Transaction does not belong to this user"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class CreateTransactionForBlockedUserException(HTTPException):
    def __init__(self, detail: str = "Cannot create transaction for blocked user"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class UpdateTransactionForBlockedUserException(HTTPException):
    def __init__(self, detail: str = "Cannot update transaction for blocked user"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class TransactionAlreadyRollbackedException(HTTPException):
    def __init__(self, detail: str = "Transaction has already been rollbacked"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
