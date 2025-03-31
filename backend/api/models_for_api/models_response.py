from datetime import datetime

from api.models_for_api.base_model import ApiCompanyUpdate, ApiUser
from pydantic import BaseModel


class ApiCompany(ApiCompanyUpdate):
    """Модель компании для ответа"""
    created_at: datetime


class ApiCompanyForUserList(BaseModel):
    id: int
    name: str


class ApiUserResponse(ApiUser):
    """Модель юзера для ответа"""
    company: ApiCompanyForUserList | None = None
