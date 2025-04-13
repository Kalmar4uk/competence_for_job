from datetime import datetime

from api.core.base_from_django_model import ApiUserFromDjangoModel
from pydantic import BaseModel


class ApiUser(ApiUserFromDjangoModel):
    """Базовая модель юзера"""
    id: int
    email: str
    first_name: str
    last_name: str
    job_title: str
    role: str | None = None


class ApiCompany(BaseModel):
    """Базовая модель компании"""
    id: int
    name: str
    is_active: bool = True
