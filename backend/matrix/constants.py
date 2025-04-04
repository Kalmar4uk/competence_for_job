from django.utils import timezone

CURRENT_DATETIME = timezone.now()
CURRENT_DATE = CURRENT_DATETIME.date()
CURRENT_MONTH = CURRENT_DATETIME.month
JOB_TITLE_USERS = [
    "Консультант",
    "Ведущий консультант",
    "Старший специалист",
    "Специалист",
    "Старший специалист"
]
NAME_FOR_TASK_MATRIX = "Назначенная матрица"
CHOICES = (
    ("Новая", "Новая"),
    ("Завершена", "Завершена"),
    ("Просрочена", "Просрочена")
)
