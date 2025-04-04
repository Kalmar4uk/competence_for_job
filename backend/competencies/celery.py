import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "competencies.settings")
app = Celery("competencies")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-matrix-first-monday': {
        'task': 'matrix.tasks.generate_matrix_for_user',
        'schedule': crontab(day_of_week='mon', day_of_month='1-7', hour=9, minute=45),
    },
    'generate-matrix-third-monday': {
        'task': 'matrix.tasks.generate_matrix_for_user',
        'schedule': crontab(day_of_week='mon', day_of_month='15-21', hour=9, minute=45),
    },
}
