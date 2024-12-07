from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

CHOICES_GRADE = (
    ("No Skills", "No Skills"),
    ("Basic", "Basic"),
    ("Good", "Good"),
    ("Good+", "Good+"),
    ("Strong", "Strong"),
    ("Expert", "Expert")
)


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
    min_grade = models.CharField("Минимальная оценка", max_length=50)
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
    user = models.ForeignKey(
        User,
        related_name="competence",
        on_delete=models.CASCADE,
        verbose_name="Сотрудник"
    )
    skill = models.ManyToManyField(Skill, through="SkillCompetence")

    class Meta:
        ordering = ['user']
        verbose_name = "Компетенция"
        verbose_name_plural = "Компетенции"

    def __str__(self):
        return f"{self.user}"


class SkillCompetence(models.Model):
    competence = models.ForeignKey(
        Competence,
        related_name="skill_competence",
        verbose_name="Компетенция",
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        Skill,
        related_name="skill_competence",
        verbose_name="Навык",
        on_delete=models.CASCADE
    )
    grade_skill = models.CharField(
        "Оценка",
        max_length=10,
        choices=CHOICES_GRADE
    )
    date = models.DateTimeField("Дата оценки", auto_now_add=True)

    class Meta:
        verbose_name = "Оценка навыка сотрудника"
        verbose_name_plural = "Оценки навыков сотрудников"

    def __str__(self):
        return f"Оценка сотрудника {self.competence}"
