from datetime import datetime

from api.core.base_from_django_model import ApiUserFromDjangoModel, ApiBaseModelIfFieldsMatch
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


class ApiTemplateMatrix(BaseModel):
    id: int
    name: str
    created_at: datetime


class ApiSkills(ApiBaseModelIfFieldsMatch):
    id: int
    area_of_application: str
    skill: str


class ApiBasePagination(BaseModel):
    count: int
    next: int | None = None
    previous: int | None = None
