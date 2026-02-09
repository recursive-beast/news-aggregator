import os

from celery import Celery

DB_URI = os.getenv("DB_URI")

app = Celery("sidecar", broker="redis://redis:6379/0", backend=f"db+{DB_URI}")

app.conf.update(
    worker_max_tasks_per_child=100,
    task_time_limit=300,  # 5 mins
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    result_extended=True,
    timezone="UTC",
    enable_utc=True,
)

app.autodiscover_tasks(["tasks"], force=True)
