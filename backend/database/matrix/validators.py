from tortoise.validators import Validator
from tortoise.exceptions import ValidationError
from utils.constants import STATUSES_MATRIX, TEMPLATE_GRADE


class ValidationCheckStatus(Validator):

    def __call__(self, value: str):
        if value not in STATUSES_MATRIX:
            raise ValidationError(
                f"Статус матрицы не соответствует шаблону - {STATUSES_MATRIX}"
            )


class ValidationTemplateGrade(Validator):

    def __call__(self, value: str):
        if value not in TEMPLATE_GRADE:
            raise ValidationError(
                f"Оценка не соответствует шаблону - {TEMPLATE_GRADE}"
            )
