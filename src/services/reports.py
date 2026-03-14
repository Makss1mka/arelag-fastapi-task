"""
Reports services
"""

import json
import logging
import uuid

from fastapi import Request
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.reports import ReportNotExistsException
from src.tasks.reports import create_report_task
from src.utils.annotations.basic import RedisDep, SessionDep
from src.utils.enums import ResponseTextStatus

logger = logging.getLogger(__name__)


class ReportService:
    """
    Class contains buisness logic for payments
    """

    def __init__(self, req: Request, session: AsyncSession, redis: Redis):
        self._session = session
        self._redis = redis

    async def create_report(self) -> dict:
        """
        Creates report
        """

        task = create_report_task.apply_async()

        return {
            "status": ResponseTextStatus.PENDING,
            "data": {
                "task_id": task.id,
            },
        }

    async def get_report(self, report_id: uuid.UUID) -> list:
        """
        Get report by it id
        """

        raw_report = await self._redis.get("celery-task-meta-" + str(report_id))

        if not raw_report:
            raise ReportNotExistsException()

        json_report = json.loads(raw_report)

        final_report = json_report.get("result", {}).get("data", [])

        return final_report


async def get_report_service(req: Request, session: SessionDep, redis: RedisDep):
    return ReportService(req=req, session=session, redis=redis)
