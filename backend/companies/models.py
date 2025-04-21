from django.conf import settings
from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField("Название", max_length=250, unique=True)
    director = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="director_company",
        verbose_name="Директор"
    )
    created_at = models.DateTimeField("Создана от", auto_now_add=True)
    closed_at = models.DateTimeField("Закрыта от", null=True, blank=True)
    is_active = models.BooleanField("Активна?", default=True)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active is False:
            self.closed_at = timezone.now()
        super().save(*args, **kwargs)


class LegalDetailsCompany(models.Model):
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="company",
        verbose_name="Компания"
    )

    class Meta:
        verbose_name = "Юридические данные"
        verbose_name_plural = "Юридические данные"

    def __str__(self):
        return f"Юридические данные компании {self.company.company.name}"


class OldCompanyEmployee(models.Model):
    company = models.ForeignKey(
        Company,
        verbose_name="Старая компания",
        on_delete=models.SET_NULL,
        related_name="old_company",
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Сотрудник",
        related_name="user_old_company",
        on_delete=models.CASCADE
    )
    job_title = models.CharField(
        "Должность которая была в этой компании",
        max_length=50
    )
    date_of_employment = models.DateField(
        "Дата трудоустройства",
        null=True,
    )
    date_of_dismissal = models.DateField(
        "Дата увольнения",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Старая компания сотрудника"
        verbose_name_plural = "Старые компании сотрудников"

    def __str__(self):
        return (
            f"Старая компания сотрудника "
            f"{self.user.first_name} {self.user.last_name}"
        )
