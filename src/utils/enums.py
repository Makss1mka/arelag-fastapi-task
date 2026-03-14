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


class PaymentTransactionStatus(StrEnum):
    """
    Enum for payments statuses
    """

    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    RALLBACKED = "RALLBACKED"


class ResponseTextStatus(StrEnum):
    """
    Common response text statuses
    """

    SUCCESS = "success"
    EXCEPTION = "exception"
    PENDING = "pending"


class UserBalanceUpdateDirection(StrEnum):
    """
    Enum class for updating user balance, it represents direction of balance change (Up or Down)
    """

    UP = "UP"
    DOWN = "DOWN"
