"""
Api router for reports
"""

import uuid

from fastapi import APIRouter, status

from src.utils.annotations.services import ReportServiceDep
from src.utils.responses import CommonJSONResponse

report_router = APIRouter(default_response_class=CommonJSONResponse)


@report_router.get("/reports/{report_id}", response_model=list, status_code=status.HTTP_200_OK)
async def get_report(
    report_service: ReportServiceDep,
    report_id: uuid.UUID,
) -> list:
    return await report_service.get_report(report_id=report_id)


@report_router.post("/reports", response_model=dict, status_code=status.HTTP_201_CREATED)
async def post_report(
    report_service: ReportServiceDep,
) -> dict:
    return await report_service.create_report()
