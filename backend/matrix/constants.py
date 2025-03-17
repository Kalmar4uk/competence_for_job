from django.utils import timezone


CURRENT_DATE = timezone.now().date()
CURRENT_MONTH = timezone.now().month
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
