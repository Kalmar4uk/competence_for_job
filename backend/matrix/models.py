from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from matrix.constants import CHOICES, NAME_FOR_TASK_MATRIX
from matrix.validators import validation_check_status


class Skill(models.Model):
    area_of_application = models.CharField(
        "Область", max_length=11
    )
    skill = models.CharField("Навык", max_length=150)

    class Meta:
        ordering = ["area_of_application"]
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.skill


class GradeCompetenceJobTitle(models.Model):
    job_title = models.CharField("Должность сотрудника", max_length=50)
    min_grade = models.ForeignKey(
        "GradeSkill",
        on_delete=models.CASCADE,
        verbose_name="Минимальная оценка"
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="grade_competence",
        verbose_name="Навык"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Уровень навыков по должности"
        verbose_name_plural = "Уровень навыков по должностям"

    def __str__(self):
        return f"Минимальная оценка ({self.id})"


class Competence(models.Model):
    skill = models.ForeignKey(
        Skill,
        related_name="skill_competence",
        verbose_name="Навык",
        on_delete=models.CASCADE
    )
    grade_skill = models.ForeignKey(
        "GradeSkill",
        verbose_name="Оценка",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    matrix = models.ForeignKey("Matrix", on_delete=models.CASCADE, related_name="competencies")

    class Meta:
        verbose_name = "Компетенция"
        verbose_name_plural = "Компетенции"


class GradeSkill(models.Model):
    grade = models.CharField("Оценка", max_length=10)
    evaluation_number = models.PositiveSmallIntegerField("Числовая оценка")

    class Meta:
        verbose_name = "Шаблон оценки навыка"
        verbose_name_plural = "Шаблон оценок навыков"

    def __str__(self):
        return self.grade


class Matrix(models.Model):
    name = models.CharField(
        "Наименование",
        max_length=20,
        default=NAME_FOR_TASK_MATRIX
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Сотрудник"
    )
    status = models.CharField(
        "Статус",
        max_length=10,
        default="Новая",
        choices=CHOICES,
        validators=[validation_check_status]
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    completed_at = models.DateTimeField(
        "Дата завершения",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Матрица"
        verbose_name_plural = "Матрицы"

    def __str__(self):
        return self.name
