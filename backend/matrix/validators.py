from django.core.exceptions import ValidationError
from matrix.constants import TEMPLATE_GRADE, STATUSES_MATRIX


def validation_check_status(data):
    if data not in STATUSES_MATRIX:
        raise ValidationError(
            f"Статус не соответствует шаблону - {STATUSES_MATRIX}"
        )


def validation_max_number(data):
    if data > 5:
        raise ValidationError(
            "Оценка больше 5"
        )


def validation_template_grade(data):
    if data not in TEMPLATE_GRADE:
        raise ValidationError(
            f"Оценка не соответствует шаблону - {TEMPLATE_GRADE}"
        )
