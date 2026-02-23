"""
Enum classes
"""

from enum import StrEnum


class Currency(StrEnum):
    """
    Enum for currencies
    """

    USD = "USD"
    EUR = "EUR"
    AUD = "AUD"
    CAD = "CAD"
    ARS = "ARS"
    PLN = "PLN"
    BTC = "BTC"
    ETH = "ETH"
    DOGE = "DOGE"
    USDT = "USDT"
    BYN = "BYN"
    RUB = "RUB"


class UserStatus(StrEnum):
    """
    Enum for users statuses
    """

    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    FREEZED = "FREEZED"


class TransactionStatus(StrEnum):
    """
    Enum for payments statuses
    """

    PENDING = "PENDING"
    processed = "PROCESSED"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ResponseTextStatus(StrEnum):
    """
    Common response text statuses
    """

    SUCCESS = "success"
    EXCEPTION = "exception"


class UserBalanceUpdateDirection(StrEnum):
    """
    Enum class for updating user balance, it represents direction of balance change (Up or Down)
    """

    UP = "up"
    DOWN = "down"
