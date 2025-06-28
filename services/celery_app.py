# services/celery_app.py
import logging

from celery import Celery

from config.settings import settings

celery_app = Celery("aurelius", broker=settings.broker_url, backend=settings.broker_url)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task
def process_document(doc_id: str) -> None:
    logging.info(f"Processing document {doc_id}")
    # Task implementation placeholder
    return None
