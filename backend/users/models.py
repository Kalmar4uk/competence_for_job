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
    job_title = models.CharField("Должность", max_length=50, null=True, blank=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        verbose_name="Компания",
        related_name="users",
        null=True,
        blank=True
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
