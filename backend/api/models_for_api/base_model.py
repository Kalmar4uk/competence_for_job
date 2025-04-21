from datetime import datetime

from api.core.base_from_django_model import (ApiUserFromDjangoModel,
                                             ApiCompanyFromDjangoModel,
                                             ApiBaseModelIfFieldsMatch)
from pydantic import BaseModel, Field


class ApiUser(ApiUserFromDjangoModel):
    """Базовая модель юзера"""
    id: int = Field(examples=[1])
    email: str = Field(examples=["olezha.korotky@mail.ru"])
    first_name: str = Field(examples=["Олежа"])
    last_name: str = Field(examples=["Короткий"])
    middle_name: str | None = Field(default=None, examples=["Длиннович"])
    job_title: str | None = Field(default=None, examples=["Специалист"])
    role: str | None = Field(default=None, examples=["Сотрудник"])


class ApiCompany(ApiCompanyFromDjangoModel):
    """Базовая модель компании"""
    id: int = Field(examples=[1])
    name: str = Field(examples=["Абракадабра"])
    is_active: bool = True


class ApiTemplateMatrix(BaseModel):
    id: int = Field(examples=[1])
    name: str = Field(examples=["Шаблон матрицы"])
    created_at: datetime


class ApiSkills(ApiBaseModelIfFieldsMatch):
    id: int = Field(examples=[1])
    area_of_application: str = Field(examples=["Hard skill"])
    skill: str = Field(examples=["Включать компьютер"])


class ApiBasePagination(BaseModel):
    count: int = Field(examples=[4])
    next: int | None = Field(examples=[2])
    previous: int | None = Field(examples=[1])
