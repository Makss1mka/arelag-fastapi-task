"""
Base annotations
"""

from typing import Annotated, Type

from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.db import get_db_session, get_db_session_class
from src.config.redis import get_redis_client

RedisDep = Annotated[Redis, Depends(get_redis_client)]
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]
SessionClassDep = Annotated[Type[AsyncSession], Depends(get_db_session_class)]
