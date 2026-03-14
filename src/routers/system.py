"""
Api router for system/dev operations
"""

from fastapi import APIRouter, Request

from src.tasks.system import test_ping_task
from src.utils.responses import CommonJSONResponse

system_router = APIRouter(default_response_class=CommonJSONResponse)


@system_router.get("/ping")
async def ping():
    return "pong"


@system_router.get("/urls")
async def available_urls(req: Request):
    return [
        f"[{", ".join(route.methods) if hasattr(route, "methods") else "ASGIMiddleware"}] {route.path}"
        for route in req.app.routes
    ]


@system_router.get("/celery_test")
async def celery_test(req: Request):
    task = test_ping_task.apply_async()
    return {
        "task_id": task.id,
        "nessage": "TEST CELERY",
    }
