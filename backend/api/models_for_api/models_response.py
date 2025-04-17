from datetime import datetime

from api.core.base_from_django_model import ApiCompanyUpdateFromDkangoModel
from api.models_for_api.base_model import (ApiBasePagination, ApiCompany,
                                           ApiSkills, ApiTemplateMatrix,
                                           ApiUser)
from pydantic import BaseModel


class ApiCompanyBaseGet(ApiCompany, ApiCompanyUpdateFromDkangoModel):
    """Модель компании для ответа"""
    director: ApiUser
    employees: list[ApiUser] | None = None
    created_at: datetime
    closed_at: datetime | None = None


class ApiCompanyForUserList(BaseModel):
    id: int
    name: str


class ApiTemplateMatrixBaseGet(ApiTemplateMatrix):
    """Модель шаблона матрицы для ответа"""
    author: ApiUser | None = None
    company: ApiCompany | None = None
    skills: list[ApiSkills]


class ApiUserResponse(ApiUser):
    """Модель юзера с компанией для ответа"""
    company: ApiCompanyForUserList | None = None


class ApiUserPagination(ApiBasePagination):
    result: list[ApiUserResponse]


class ApiCompanyPagination(ApiBasePagination):
    result: list[ApiCompanyBaseGet]


class ApiTemplateMatrixPaginator(ApiBasePagination):
    result: list[ApiTemplateMatrixBaseGet]
