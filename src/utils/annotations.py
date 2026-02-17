"""
Diferent annotations
"""

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from redis import Redis

from fastapi import Depends
from src.config.db import get_db_session_class
from src.config.redis import get_redis_client


RedisDep = Annotated[Redis, Depends(get_redis_client)]
SessionDep = Annotated[AsyncSession, Depends(get_db_session_class)]

