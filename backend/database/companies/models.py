from database.core.models import BaseModel
from tortoise import fields
from datetime import datetime


class Company(BaseModel):
    name = fields.CharField(max_length=250, unique=True)
    director = fields.ForeignKeyField(
        model_name="models.User",
        on_delete=fields.SET_NULL,
        related_name="director_company",
        null=True
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    closed_at = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)

    async def save(self, *args, **kwargs):
        if self.is_active is False:
            self.closed_at = datetime.now()
        await super().save(*args, **kwargs)

    class Meta:
        table = "companies"


class LegalDetailsCompany(BaseModel):
    company = fields.ForeignKeyField(
        model_name="models.Company",
        related_name="company",
    )

    class Meta:
        table = "legaldetailscompany"


class OldCompanyEmployee(BaseModel):
    company = fields.ForeignKeyField(
        model_name="models.Company",
        on_delete=fields.SET_NULL,
        related_name="old_company",
        null=True
    )
    user = fields.ForeignKeyField(
        model_name="models.User",
        on_delete=fields.CASCADE,
        related_name="user_old_company"
    )
    job_title = fields.CharField(max_length=50)
    date_of_emplyment = fields.DateField(null=True)
    date_of_dismissal = fields.DateField(null=True)

    class Meta:
        table = "oldcompanyemployee"
