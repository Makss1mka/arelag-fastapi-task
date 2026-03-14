"""
Services annotations
"""

from typing import Annotated

from fastapi import Depends

from src.services.payments import PaymentService, get_payment_service
from src.services.reports import ReportService, get_report_service
from src.services.users import UserService, get_user_service

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
PaymentServiceDep = Annotated[PaymentService, Depends(get_payment_service)]
ReportServiceDep = Annotated[ReportService, Depends(get_report_service)]
