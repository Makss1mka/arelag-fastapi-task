"""
Users services
"""

import logging
import uuid
from typing import Optional

from fastapi import Request
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.exceptions.users import (
    UserAlreadyActiveException,
    UserAlreadyBlockedException,
    UserAlreadyExistsException,
    UserBalanceNotExistsException,
    UserBalanceUpdateLessZeroException,
    UserNotExistsException,
)
from src.models.users import User, UserBalance
from src.schemas.users import (
    UserBalanceUpdateRequestModel,
    UserCreateRequestModel,
    UserResponseModel,
    UserUpdateRequestModel,
)
from src.utils.annotations.basic import SessionDep
from src.utils.enums import Currency, UserBalanceUpdateDirection, UserStatus

logger = logging.getLogger(__name__)


class UserService:
    """
    Class contains buisness logic for users models
    """

    def __init__(self, req: Request, session: AsyncSession):
        self._session = session

    #
    # USERS
    #

    async def get_user(self, user_id: uuid.UUID) -> UserResponseModel:
        user = (
            await self._session.execute(select(User).where(User.id == user_id).options(joinedload(User.balances)))
        ).scalar()

        if not user:
            raise UserNotExistsException()

        return UserResponseModel.model_validate(user)

    async def create_user(self, schema: UserCreateRequestModel) -> UserResponseModel:
        existing_user = (await self._session.execute(select(User).where(User.email == schema.email))).scalar()

        if existing_user:
            raise UserAlreadyExistsException("User with such email already exists")

        new_user = User(email=schema.email)
        new_user.balances = [UserBalance(currency=cur.value) for cur in Currency]

        self._session.add(new_user)
        await self._session.flush()
        await self._session.commit()

        return UserResponseModel.model_validate(new_user)

    async def update_user(self, user_id: uuid.UUID, schema: UserUpdateRequestModel) -> UserResponseModel:
        user = (
            await self._session.execute(select(User).where(User.id == user_id).options(joinedload(User.balances)))
        ).scalar()

        if not user:
            raise UserNotExistsException()

        if user.status == schema.status == UserStatus.BLOCKED:
            raise UserAlreadyBlockedException()

        if user.status == schema.status == UserStatus.ACTIVE:
            raise UserAlreadyActiveException()

        user.status = schema.status
        await self._session.commit()

        return UserResponseModel.model_validate(user)

    async def delete_user(self, user_id: uuid.UUID) -> str:
        user = (
            await self._session.execute(select(User).where(User.id == user_id).options(joinedload(User.balances)))
        ).scalar()

        if not user:
            raise UserNotExistsException()

        for balance in user.balances:
            balance.is_active = False

        user.is_active = False
        user.email = None

        self._session.commit()

        return "User and all balances was deleted"

    async def list_users(
        self, user_id: Optional[uuid.UUID] = None, email: Optional[str] = None, user_status: Optional[UserStatus] = None
    ) -> list[UserResponseModel]:
        query = select(User).order_by(User.created_at.desc()).options(selectinload(User.balances))

        if user_id:
            query = query.where(User.id == user_id)
        if email:
            query = query.where(User.email == email)
        if user_status:
            query = query.where(User.status == user_status)

        users = (await self._session.execute(query)).scalars().all()

        return [UserResponseModel.model_validate(user) for user in users]

    #
    # USER BALANCES
    #

    async def add_user_balances(self, user: User):
        pass

    async def delete_user_balances(self, user: User):
        pass

    async def update_user_balance(self, user_id: uuid.UUID, schema: UserBalanceUpdateRequestModel):
        user = (
            await self._session.execute(select(User).where(User.id == user_id).options(joinedload(User.balances)))
        ).scalar()

        if not user:
            raise UserNotExistsException()

        updating_balacne = None
        for balance in user.balances:
            if balance.currency == schema.currency:
                updating_balacne = balance

        if not updating_balacne:
            raise UserBalanceNotExistsException()

        if schema.direction == UserBalanceUpdateDirection.DOWN and updating_balacne.amount - schema.amount < 0:
            raise UserBalanceUpdateLessZeroException()

        if schema.direction == UserBalanceUpdateDirection.DOWN:
            updating_balacne.amount -= schema.amount
        else:
            updating_balacne.amount += schema.amount

        await self._session.commit()

        return UserResponseModel.model_validate(user)


async def get_user_service(req: Request, session: SessionDep):
    return UserService(req=req, session=session)
