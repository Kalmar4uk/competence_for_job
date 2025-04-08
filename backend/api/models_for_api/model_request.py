from pydantic import BaseModel

from .base_model import ApiCompany, ApiUser


class UserRegistration(BaseModel):
    """Модель для регистрации юзера"""
    email: str
    password: str
    first_name: str
    last_name: str
    job_title: str


class CompanyRegistration(BaseModel):
    """Модель регистрации компании"""
    name: str
    employees: list[int] | None = None


class ApiCompanyUpdate(BaseModel):
    """Модель запроса обновления компании"""
    name: str
    employees: list[int] | None = None
    is_active: bool


class ApiCompanyUpdateDirector(BaseModel):
    """Модель обновления директора компании"""
    new_director: int


class ApiCompanyDeleteEmployees(BaseModel):
    """Модель удаления сотрудников из компании"""
    employees: list[int]
