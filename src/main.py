"""
Entrypoint 
"""

import http
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from src.config.logger import setup_logging
from src.config.redis import init_redis, RedisPoolConfig
from src.config.db import init_db, DbPoolConfig
from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI, HTTPException

import logging
import os

from src.exceptions.exception_handlers import common_exception_handler, http_exception_handler, pydantic_exception_handler
from src.utils.annotations import RedisDep


REDIS_URL: str = os.environ.get("REDIS_URL")
DB_URL: str = os.environ.get("DB_URL")

LOGS_LEVEL: int = logging.DEBUG
LOGS_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    setup_logging(logs_level=LOGS_LEVEL, logs_format=LOGS_FORMAT)

    logger: logging.Logger = logging.getLogger(__name__)

    async with (
        init_db(app, connection_url=DB_URL, pool_config=DbPoolConfig()),
        init_redis(app, connection_url=REDIS_URL, pool_config=RedisPoolConfig())
    ):
        logger.info(f"Server is started")
        yield
        logger.error("Server shutdown...")


app = FastAPI(lifespan=app_lifespan)

app.add_exception_handler(RequestValidationError, pydantic_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, common_exception_handler)


@app.get("/ping")
async def ping():
    return {
        "status": "success",
        "message": "pong",
    }
