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
    is_director: bool


class ApiCompanyUpdate(BaseModel):
    """Модель компании для обновления"""
    id: int
    name: str
    director: ApiUser
    employees: list[ApiUser] | None = None
    is_active: bool = True
    closed_at: datetime | None = None
