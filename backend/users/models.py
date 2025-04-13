from companies.models import Company
from core.models import GeneralHierarchy
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.manager import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField("Email", unique=True)
    middle_name = models.CharField(
        "Отчество",
        max_length=150,
        blank=True,
        null=True
    )
    job_title = models.CharField("Должность", max_length=50, null=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        verbose_name="Компания",
        related_name="users",
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        "JobGroup",
        verbose_name="Группа",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    date_of_employment = models.DateField(
        "Дата трудоустройства",
        null=True,
        blank=True
    )
    date_of_dismissal = models.DateField(
        "Дата увольнения",
        null=True,
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.is_active is False and not self.email.startswith("Этот"):
            self.email = f"Сотрудник больше не работает - {self.email}"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.middle_name:
            return f"{self.first_name} {self.last_name} {self.middle_name}"
        return f"{self.first_name} {self.last_name}"


class JobGroup(GeneralHierarchy):
    parent = models.ForeignKey(
        "JobDepartment",
        on_delete=models.SET_NULL,
        verbose_name="Департамент",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class JobDepartment(GeneralHierarchy):
    parent = models.ForeignKey(
        "JobManagement",
        verbose_name="Управление",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    children = models.ForeignKey(
        JobGroup,
        verbose_name="Группа",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"


class JobManagement(GeneralHierarchy):
    children = models.OneToOneField(
        JobDepartment,
        verbose_name="Департамент",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Управление"
        verbose_name_plural = "Управления"
