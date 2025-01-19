from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import GeneralHierarchy
from users.manager import CustomUserManager
from users.validators import validation_min_length_personnal_number


class User(AbstractUser):
    username = None
    email = models.EmailField("Email", unique=True)
    middle_name = models.CharField(
        "Отчество",
        max_length=150,
        blank=True,
        null=True
    )
    personnel_number = models.CharField(
        "Табельный номер",
        max_length=8,
        unique=True,
        null=True,
        validators=[validation_min_length_personnal_number]
    )
    job_title = models.CharField("Должность", max_length=50, null=True)
    group = models.ForeignKey(
        "JobGroup",
        verbose_name="Группа",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.is_active is False and not self.email.startswith("Этот"):
            self.email = f"Этот пидор больше не работает - {self.email}"
        super(User, self).save(*args, **kwargs)

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
        verbose_name_plural = "Департамент"


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
        verbose_name_plural = "Управление"
