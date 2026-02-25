import datetime
from datetime import timedelta

import uvicorn
from db_models import *
from fastapi import Depends, FastAPI, status
from python_models import *
from queries import (
    get_not_rollbacked_deposit_amount,
    get_not_rollbacked_transactions_count,
    get_not_rollbacked_withdraw_amount,
    get_registered_and_deposit_users_count,
    get_registered_and_not_rollbacked_deposit_users_count,
    get_registered_users_count,
    get_transactions_count,
)
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from exceptions import (
    BadRequestDataException,
    CreateTransactionForBlockedUserException,
    NegativeBalanceException,
    TransactionAlreadyRollbackedException,
    TransactionDoesNotBelongToUserException,
    TransactionNotExistsException,
    UpdateTransactionForBlockedUserException,
    UserAlreadyActiveException,
    UserAlreadyBlockedException,
    UserAlreadyExistsException,
    UserNotExistsException,
)


app = FastAPI()


@app.on_event("startup")
async def on_startup(session: AsyncSession = Depends(get_async_session)):
    await create_db_and_tables()


@app.get("/transactions/analysis", response_model=typing.Optional[list] | None, status_code=status.HTTP_200_OK)
async def get_transaction_analysis(session: AsyncSession = Depends(get_async_session)) -> typing.List[dict]:
    dt_gt = datetime.utcnow().date() - timedelta(weeks=1) + timedelta(days=1)
    dt_lt = datetime.utcnow().date()
    results = []
    for i in range(52):
        registered_users_count = await get_registered_users_count(session, dt_gt=dt_gt, dt_lt=dt_lt)
        registered_and_deposit_users_count = await get_registered_and_deposit_users_count(
            session, dt_gt=dt_gt, dt_lt=dt_lt
        )
        registered_and_not_rollbacked_deposit_users_count = await get_registered_and_not_rollbacked_deposit_users_count(
            session, dt_gt=dt_gt, dt_lt=dt_lt
        )
        not_rollbacked_deposit_amount = await get_not_rollbacked_deposit_amount(session, dt_gt=dt_gt, dt_lt=dt_lt)
        not_rollbacked_withdraw_amount = await get_not_rollbacked_withdraw_amount(session, dt_gt=dt_gt, dt_lt=dt_lt)
        transactions_count = await get_transactions_count(session, dt_gt=dt_gt, dt_lt=dt_lt)
        not_rollbacked_transactions_count = await get_not_rollbacked_transactions_count(
            session, dt_gt=dt_gt, dt_lt=dt_lt
        )
        result = {
            "start_date": dt_gt,
            "end_date": dt_lt,
            "registered_users_count": registered_users_count,
            "registered_and_deposit_users_count": registered_and_deposit_users_count,
            "registered_and_not_rollbacked_deposit_users_count": registered_and_not_rollbacked_deposit_users_count,
            "not_rollbacked_deposit_amount": not_rollbacked_deposit_amount,
            "not_rollbacked_withdraw_amount": not_rollbacked_withdraw_amount,
            "transactions_count": transactions_count,
            "not_rollbacked_transactions_count": not_rollbacked_transactions_count,
        }
        for field in (
            "registered_users_count",
            "registered_and_deposit_users_count",
            "registered_and_not_rollbacked_deposit_users_count",
            "not_rollbacked_deposit_amount",
            "not_rollbacked_withdraw_amount",
            "transactions_count",
            "not_rollbacked_transactions_count",
        ):
            if result[field] > 0:
                results.append(result)
                break
        dt_gt -= timedelta(weeks=1)
        dt_lt -= timedelta(weeks=1)
    return results


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7999, reload=True)
