"""
Some tasks for testing celery
"""

import logging

from celery import shared_task

logger = logging.getLogger("system")


@shared_task
def test_ping_task():
    """
    Task that for testing celery working
    """
    logger.info("PING")
