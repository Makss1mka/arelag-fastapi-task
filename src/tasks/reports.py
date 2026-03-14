"""
Tasks for creating reports
"""

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, Tuple

from celery import shared_task
from sqlalchemy import Date, cast, distinct, func, select
from sqlalchemy.orm import Session

from src.models.payments import PaymentTransaction
from src.models.users import User
from src.utils.enums import Currency, PaymentTransactionStatus, ResponseTextStatus

logger = logging.getLogger("reports")


def generate_weeks_grid(weeks_count: int = 52) -> Tuple[Dict[datetime.date, Dict[str, Any]], datetime.date]:
    """
    Generate empty report form
    """

    now = datetime.now(timezone.utc)
    days_since_monday = now.weekday()

    current_week_start = now - timedelta(
        days=days_since_monday, hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond
    )

    report_grid = {}
    for i in range(weeks_count):
        week_start = current_week_start - timedelta(weeks=i)
        week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)

        week_date_key = week_start.date()

        report_grid[week_date_key] = {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "new_users": 0,
            "unique_depositors": 0,
            "total_transactions": 0,
            "successful_transactions": 0,
            "total_deposits_amount": {currency.value: Decimal("0.0") for currency in Currency},
            "total_withdrawals_amount": {currency.value: Decimal("0.0") for currency in Currency},
        }

    oldest_week_start_date = (current_week_start - timedelta(weeks=weeks_count - 1)).date()

    return report_grid, oldest_week_start_date


def create_weekly_reports(session: Session) -> list[Dict[str, Any]]:
    """
    Creates weekly reports
    """

    report_grid, start_date = generate_weeks_grid(52)

    user_week_col = cast(func.date_trunc("week", User.created_at), Date)

    users_stmt = (
        select(user_week_col.label("week_date"), func.count(User.id).label("new_users"))
        .where(cast(User.created_at, Date) >= start_date)
        .group_by(user_week_col)
    )

    for row in session.execute(users_stmt).all():
        if row.week_date in report_grid:
            report_grid[row.week_date]["new_users"] = row.new_users

    tx_week_col = cast(func.date_trunc("week", PaymentTransaction.created_at), Date)

    is_not_cancelled = PaymentTransaction.status != PaymentTransactionStatus.RALLBACKED

    tx_stmt = (
        select(
            tx_week_col.label("week_date"),
            PaymentTransaction.currency.label("currency"),
            func.count(PaymentTransaction.id).label("total_tx"),
            func.count(PaymentTransaction.id).label("success_tx"),
            func.count(distinct(PaymentTransaction.to_user_id)).label("unique_depositors"),
            func.coalesce(func.sum(PaymentTransaction.amount).filter(is_not_cancelled), Decimal("0.0")).label(
                "deposit_sum"
            ),
            func.coalesce(func.sum(PaymentTransaction.amount).filter(is_not_cancelled), Decimal("0.0")).label(
                "withdrawal_sum"
            ),
        )
        .where(cast(PaymentTransaction.created_at, Date) >= start_date)
        .group_by(tx_week_col, PaymentTransaction.currency)
    )

    for row in session.execute(tx_stmt).all():
        if row.week_date in report_grid:
            grid_row = report_grid[row.week_date]

            currency_key = row.currency.value if isinstance(row.currency, Currency) else row.currency

            grid_row["total_transactions"] += row.total_tx
            grid_row["successful_transactions"] += row.success_tx
            grid_row["unique_depositors"] += row.unique_depositors

            if currency_key in grid_row["total_deposits_amount"]:
                grid_row["total_deposits_amount"][currency_key] = row.deposit_sum
                grid_row["total_withdrawals_amount"][currency_key] = row.withdrawal_sum

    keys = sorted(report_grid.keys(), reverse=True)
    sorted_report = []

    for key in keys:
        week_data = report_grid[key]

        week_data["total_deposits_amount"] = {
            curr: str(val) for curr, val in week_data["total_deposits_amount"].items()
        }

        week_data["total_withdrawals_amount"] = {
            curr: str(val) for curr, val in week_data["total_withdrawals_amount"].items()
        }

        sorted_report.append(week_data)

    return sorted_report


@shared_task
def create_report_task():
    """
    Task for creating reports
    """

    from src.config.celery import CelerySession

    with CelerySession() as session:
        try:
            report_data = create_weekly_reports(session)

            logger.info(f"Report generated successfully.")

            return {"status": ResponseTextStatus.SUCCESS, "data": report_data}
        except Exception as e:
            logger.error(f"Failed to generate report: {str(e)}")
            return {"status": ResponseTextStatus.EXCEPTION, "message": str(e)}
