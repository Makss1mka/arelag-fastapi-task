"""
Api router for users
"""

import uuid
from typing import Optional

from fastapi import APIRouter, status

from src.schemas.users import (
    UserBalanceUpdateRequestModel,
    UserCreateRequestModel,
    UserResponseModel,
    UserUpdateRequestModel,
)
from src.utils.annotations.services import UserServiceDep
from src.utils.enums import UserStatus
from src.utils.responses import CommonJSONResponse

users_router = APIRouter(default_response_class=CommonJSONResponse)


@users_router.get("/{user_id}", response_model=UserResponseModel, status_code=status.HTTP_200_OK)
async def get_user(user_service: UserServiceDep, user_id: uuid.UUID) -> UserResponseModel:
    return await user_service.get_user(user_id)


@users_router.get("/", response_model=list[UserResponseModel], status_code=status.HTTP_200_OK)
async def list_users(
    user_service: UserServiceDep,
    user_id: Optional[uuid.UUID] = None,
    email: Optional[str] = None,
    user_status: Optional[UserStatus] = None,
) -> list[UserResponseModel]:
    return await user_service.list_users(
        user_id=user_id,
        email=email,
        user_status=user_status,
    )


@users_router.post("/", response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def post_user(user_service: UserServiceDep, schema: UserCreateRequestModel) -> UserResponseModel:
    return await user_service.create_user(schema)


@users_router.patch("/{user_id}", response_model=UserResponseModel, status_code=status.HTTP_200_OK)
async def patch_user(
    user_service: UserServiceDep,
    schema: UserUpdateRequestModel,
    user_id: uuid.UUID,
) -> UserResponseModel:
    return await user_service.update_user(user_id, schema)


@users_router.delete("/{user_id}", response_model=str, status_code=status.HTTP_200_OK)
async def delete_user(
    user_service: UserServiceDep,
    user_id: uuid.UUID,
) -> str:
    return await user_service.delete_user(user_id)


@users_router.patch("/{user_id}/balances", response_model=UserResponseModel, status_code=status.HTTP_200_OK)
async def change_balance(
    user_service: UserServiceDep,
    schema: UserBalanceUpdateRequestModel,
    user_id: uuid.UUID,
) -> UserResponseModel:
    return await user_service.update_user_balance(user_id, schema)
