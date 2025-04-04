from datetime import datetime

from api.core.base_from_django_model import ApiCompanyUpdateFromDkangoModel
from api.models_for_api.base_model import ApiCompany, ApiUser
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


class ApiUserResponse(ApiUser):
    """Модель юзера с компанией для ответа"""
    company: ApiCompanyForUserList | None = None
