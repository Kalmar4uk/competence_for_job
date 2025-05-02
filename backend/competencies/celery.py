import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "competencies.settings")
app = Celery("competencies")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "status_matrix_to_expired": {
        "task": "matrix.tasks.change_matrix_status_to_expired",
        "schedule": crontab(hour=21, minute=00)
    }
}
