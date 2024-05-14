from celery import Celery
from celery.signals import before_task_publish, after_task_publish
from celery.states import STARTED, RECEIVED
from celery.schedules import crontab

from .settings import settings


celery_app = Celery()
celery_app.config_from_object(obj=settings, namespace="CELERY")
celery_app.autodiscover_tasks(packages=["src"])
celery_app.conf.beat_schedule = {
    "PING": {
        "task": "PING",
        "schedule": crontab(minute="*/1")
    }
}


@before_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    task = celery_app.tasks.get(sender)
    backend = task.backend if task else celery_app.backend
    backend.store_result(headers['id'], None, RECEIVED)


@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    task = celery_app.tasks.get(sender)
    backend = task.backend if task else celery_app.backend
    backend.store_result(headers['id'], None, STARTED)
