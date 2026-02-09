from celery.utils.log import get_task_logger
import requests

from celery_app import app as celery_app

logger = get_task_logger(__name__)


@celery_app.task(auto_retry_for=(Exception,))
def call_webhook(webhook_url: str, task_id: str):
    payload = {"task_id": task_id}
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()
