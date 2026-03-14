"""
Celery config
"""

import os

from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.exceptions.celery import CeleryNotEnvs

CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND")
SYNC_DB_URL: str = os.environ.get("SYNC_DB_URL")

if not CELERY_BROKER_URL or not CELERY_RESULT_BACKEND:
    raise CeleryNotEnvs()


engine = create_engine(SYNC_DB_URL, pool_size=10, max_overflow=5, pool_pre_ping=True)
CelerySession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


celery_app = Celery(
    "payment_service",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=15 * 60,
    worker_max_tasks_per_child=200,
    worker_prefetch_multiplier=1,
    result_expires=3600,
)


celery_app.autodiscover_tasks(["src.tasks"])
