"""
Api router for payments
"""

import uuid

from fastapi import APIRouter, status

from src.schemas.payments import PaymentTransactionCreateRequestModel, PaymentTransactionResponseModel
from src.utils.annotations.services import PaymentServiceDep
from src.utils.responses import CommonJSONResponse

payments_router = APIRouter(default_response_class=CommonJSONResponse)


@payments_router.get(
    "/transactions/{transaction_id}",
    response_model=PaymentTransactionResponseModel,
    status_code=status.HTTP_200_OK
)
async def get_transaction(
    payment_service: PaymentServiceDep,
    transaction_id: uuid.UUID,
) -> PaymentTransactionResponseModel:
    return await payment_service.get_transaction(transaction_id=transaction_id)


@payments_router.get(
    "/users/{user_id}/transactions",
    response_model=list[PaymentTransactionResponseModel],
    status_code=status.HTTP_200_OK
)
async def list_transactios(
    payment_service: PaymentServiceDep,
    user_id: uuid.UUID,
    page_size: int = 10,
    page_num: int = 1
) -> list[PaymentTransactionResponseModel]:
    return await payment_service.list_transaction(
        user_id=user_id,
        page_size=page_size,
        page_num=page_num
    )


@payments_router.post(
    "/users/{user_id}/transactions",
    response_model=PaymentTransactionResponseModel,
    status_code=status.HTTP_201_CREATED
)
async def post_transactio(
    payment_service: PaymentServiceDep,
    schema: PaymentTransactionCreateRequestModel,
    user_id: uuid.UUID,
) -> PaymentTransactionResponseModel:
    return await payment_service.create_transaction(
        user_id=user_id,
        schema=schema
    )


@payments_router.patch(
    "/users/{user_id}/transactions/{transaction_id}/rollback",
    response_model=str,
    status_code=status.HTTP_200_OK
)
async def rollback_transactio(
    payment_service: PaymentServiceDep,
    user_id: uuid.UUID,
    transaction_id: uuid.UUID,
) -> str:
    return await payment_service.rollback_transaction(
        user_id=user_id,
        transaction_id=transaction_id
    )


@payments_router.delete(
    "/transactions/{transaction_id}",
    response_model=str,
    status_code=status.HTTP_200_OK
)
async def delete_transactio(
    payment_service: PaymentServiceDep,
    transaction_id: uuid.UUID
) -> str:
    return await payment_service.delete_transaction(transaction_id)

