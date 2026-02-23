"""
Services annotations
"""

from typing import Annotated

from fastapi import Depends

from src.services.users import UserService, get_user_service

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
