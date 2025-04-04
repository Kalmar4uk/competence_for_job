from django.core.exceptions import ValidationError

statuses = ["Новая", "Завершена", "Просрочена"]


def validation_check_status(data):
    if data not in statuses:
        raise ValidationError(
            f"Статус не соответствует шаблону - {statuses}"
        )
