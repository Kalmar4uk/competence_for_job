from companies.models import Company
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
    template_matrix = models.ForeignKey(
        "TemplateMatrix",
        on_delete=models.CASCADE,
        verbose_name="Шаблон на основании которого создана матрица",
        related_name="matrix"
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
    skills = models.ManyToManyField(
        Skill,
        through="GradeSkillMatrix",
        related_name="matrix"
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True
    )
    last_update_status = models.DateTimeField(
        "Последнее изменение статуса",
        null=True,
        blank=True
    )
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


class TemplateMatrix(models.Model):
    name = models.CharField("Название", max_length=100)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        verbose_name="Компания",
        related_name="temmplate_matrix",
        null=True,
        blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор шаблона",
        related_name="temmplate_matrix",
        null=True,
        blank=True
    )
    skills = models.ManyToManyField(
        Skill,
        verbose_name="Навыки",
        related_name="template_matrix"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Шаблон матрицы"
        verbose_name_plural = "Шаблоны матриц"

    def __str__(self):
        return self.name


class GradeSkillMatrix(models.Model):
    matrix = models.ForeignKey(
        Matrix,
        on_delete=models.CASCADE,
        verbose_name="Матрица",
        related_name="gradeskillmatrix"
    )
    skills = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name="Навык",
        related_name="gradeskillmatrix"
    )
    grades = models.ForeignKey(
        GradeSkill,
        on_delete=models.CASCADE,
        verbose_name="Оценка",
        related_name="gradeskillmatrix",
        default=1
    )
