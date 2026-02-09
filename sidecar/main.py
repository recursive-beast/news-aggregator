from http import HTTPStatus
from typing import Any, Dict, List, Optional

from celery import uuid
from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException
from kombu.exceptions import OperationalError
from pydantic import BaseModel, Field

from celery_app import app as celery_app


class TaskRequest(BaseModel):
    task_name: str
    args: Optional[List[Any]] = Field(default_factory=list)
    kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict)
    webhook_url: Optional[str] = None


app = FastAPI()


@app.post("/tasks", status_code=HTTPStatus.ACCEPTED)
async def run_task(request: TaskRequest):
    if request.task_name not in celery_app.tasks:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")

    task_id = uuid()

    call_webhook_signature = None
    if request.webhook_url:
        call_webhook_signature = celery_app.signature(
            "tasks.call_webhook",
            args=(request.webhook_url, task_id),
            immutable=True,
        )

    try:
        result = celery_app.send_task(
            request.task_name,
            args=request.args,
            kwargs=request.kwargs,
            task_id=task_id,
            link=call_webhook_signature,
            link_error=call_webhook_signature,
        )
        return {"task_id": result.id}

    except OperationalError:
        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Queue unavailable",
        )


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    result: AsyncResult = celery_app.AsyncResult(task_id)

    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")

    return {
        "task_id": result.task_id,
        "status": result.status,
        "traceback": result.traceback if result.failed() else None,
        "result": result.result if result.ready() else None,
    }
