"""
Payments services
"""

import logging
import uuid

from fastapi import Request
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.common import NegativeBalanceException
from src.exceptions.transactions import CreateTransactionForBlockedUserException, TransactionAlreadyRollbackedException, TransactionDoesNotBelongToUserException, TransactionNotExistsException, UpdateTransactionForBlockedUserException
from src.exceptions.users import (
    UserBalanceNotExistsException,
    UserNotExistsException,
)
from src.models.users import User, UserBalance
from src.models.payments import PaymentTransaction
from src.schemas.payments import (
    PaymentTransactionResponseModel,
    PaymentTransactionCreateRequestModel
)
from src.utils.annotations.basic import SessionDep
from src.utils.enums import Currency, UserStatus, PaymentTransactionStatus

logger = logging.getLogger(__name__)


class PaymentService:
    """
    Class contains buisness logic for payments
    """

    def __init__(self, req: Request, session: AsyncSession):
        self._session = session

    async def get_transaction(self, transaction_id: uuid.UUID) -> PaymentTransactionResponseModel:
        """
        Find transaction by it id.
        Returns reponse model.
        """

        return PaymentTransactionResponseModel.model_validate(
            await self._get_transaction(transaction_id)
        )

    async def create_transaction(self, user_id: uuid.UUID, schema: PaymentTransactionCreateRequestModel) -> PaymentTransactionResponseModel:
        """
        Creates payment transaction.
        Finds user balances with currency matching schemas's currency and make transfer.
        """
        
        from_user = await self._get_user(user_id)
        if from_user.status == UserStatus.BLOCKED:
            raise CreateTransactionForBlockedUserException("Your profile is blocked")

        to_user = await self._get_user(schema.send_to)
        if to_user.status == UserStatus.BLOCKED:
            raise CreateTransactionForBlockedUserException("Profile you want to make transaction with is blocked")

        from_user_balance = await self._get_user_balance(from_user.id, schema.currency)
        if from_user_balance.amount - schema.amount < 0:
            raise NegativeBalanceException()

        to_user_balance = await self._get_user_balance(to_user.id, schema.currency)

        from_user_balance.amount -= schema.amount
        to_user_balance.amount += schema.amount

        transaction = PaymentTransaction(
            from_user=from_user,
            to_user=to_user,
            currency=schema.currency,
            amount=schema.amount
        )

        self._session.add(transaction)
        await self._session.flush()
        await self._session.commit()

        return PaymentTransactionResponseModel.model_validate(transaction)

    async def rollback_transaction(self, user_id: uuid.UUID, transaction_id: uuid.UUID) -> str:
        """
        Make transaction rallback.
        Gives sender back his money, reciever balance will be deacreased.
        """

        from_user = await self._get_user(user_id)
        if from_user.status == UserStatus.BLOCKED:
            raise CreateTransactionForBlockedUserException("Your profile is blocked")

        transaction = await self._get_transaction(transaction_id)
        if transaction.from_user_id != from_user.id:
            raise TransactionDoesNotBelongToUserException()
        if transaction.status == PaymentTransactionStatus.RALLBACKED:
            raise TransactionAlreadyRollbackedException()
        
        to_user = await self._get_user(transaction.to_user_id)

        to_user_balance = await self._get_user_balance(to_user.id, transaction.currency)
        from_user_balance = await self._get_user_balance(from_user.id, transaction.currency)
        
        if to_user_balance.amount - transaction.amount < 0:
            raise NegativeBalanceException()

        from_user_balance.amount += transaction.amount
        to_user_balance.amount -= transaction.amount
        transaction.status = PaymentTransactionStatus.RALLBACKED

        await self._session.commit()

        return "Transaction was successfully rollbacked"

    async def delete_transaction(self, transaction_id: uuid.UUID) -> str:
        transaction = await self._get_transaction(transaction_id)

        transaction.is_active = False
        self._session.commit()

        return "Transaction was successfully deleted"

    async def list_transaction(
        self, page_size: int, page_num: int, user_id: uuid.UUID
    ) -> list[PaymentTransactionResponseModel]:
        await self._get_user(user_id)
        
        transactions = (
            await self._session.execute(
                select(PaymentTransaction)
                .order_by(PaymentTransaction.created_at.desc())
                .where(
                    or_(
                       PaymentTransaction.from_user_id == user_id,
                       PaymentTransaction.to_user_id == user_id
                    )
                )
                .limit(page_size)
                .offset(page_num)
            )
        ).scalars().all()

        result = [
            PaymentTransactionResponseModel(
                id=transaction.id,
                from_user_id=transaction.from_user_id,
                to_user_id=transaction.to_user_id,
                currency=transaction.currency,
                status=transaction.status,
                created_at=transaction.created_at,
                amount=transaction.amount if transaction.to_user_id == user_id else -transaction.amount
            )
            for transaction in transactions
        ]

        return result


    async def _get_user(self, user_id: uuid.UUID) -> User:
        """
        Finds user by id
        """

        user = (
            await self._session.execute(
                select(User)
                .where(User.id == user_id)
            )
        ).scalar()

        if not user:
            raise UserNotExistsException()

        return user

    async def _get_transaction(self, transaction_id: uuid.UUID) -> PaymentTransaction:
        """
        Finds transaction by id
        """

        transaction = (
            await self._session.execute(
                select(PaymentTransaction)
                .where(PaymentTransaction.id == transaction_id)
            )
        ).scalar()

        if not transaction:
            raise TransactionNotExistsException()

        return transaction

    async def _get_user_balance(self, user_id: uuid.UUID, currency: Currency) -> UserBalance:
        """
        Finds user balance with given user_id and curency
        """

        user_balance = (
            await self._session.execute(
                select(UserBalance)
                .where(
                    and_(
                        UserBalance.user_id == user_id,
                        UserBalance.currency == currency
                    )
                )
            )
        ).scalar()

        if not user_balance:
            UserBalanceNotExistsException()

        return user_balance


async def get_payment_service(req: Request, session: SessionDep):
    return PaymentService(req=req, session=session)
