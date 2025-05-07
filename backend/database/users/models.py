from database.core.models import BaseModel
from tortoise import fields
from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=128)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=100)
    middle_name = fields.CharField(max_length=100, null=True)
    job_title = fields.CharField(max_length=50, null=True)
    company = fields.ForeignKeyField(
        model_name="models.Company",
        on_delete=fields.SET_NULL,
        related_name="users",
        null=True
    )
    date_of_employment = fields.DateField(null=True)
    date_of_employment = fields.DateField(null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def set_password(self, password: str):
        self.password = context.hash(password)

    def check_password(self, password: str):
        return context.verify(password, self.password)

    async def save(self, *args, **kwargs):
        if self.is_active is False and not self.email.startswith("Сотрудник"):
            self.email = f"Сотрудник больше не работает - {self.email}"
        await super().save(*args, **kwargs)

    class Meta:
        table = 'users'
