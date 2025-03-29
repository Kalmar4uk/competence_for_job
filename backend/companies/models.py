from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField("Название", max_length=250, unique=True)
    created_at = models.DateTimeField("Создана от", auto_now_add=True)
    closed_at = models.DateTimeField("Закрыта от", null=True, blank=True)
    is_active = models.BooleanField("Статус", default=True)

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

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
