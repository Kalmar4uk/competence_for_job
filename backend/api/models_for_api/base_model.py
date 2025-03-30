from datetime import datetime
from api.core.base_from_django_model import ApiBaseModelIfFieldsMatch, ApiUserFromDjangoModel, ApiMatrixFromDjangoModel
from pydantic import BaseModel


class ApiUser(ApiUserFromDjangoModel):
    """Модель юзера для ответа"""
    id: int
    email: str
    first_name: str
    last_name: str
    job_title: str


class ApiCompany(BaseModel):
    """Модель компании для ответа"""
    id: int
    name: str
    director: ApiUser
    employees: list[ApiUser] | None = None
    created_at: datetime
    closed_at: datetime | None = None
    is_active: bool = True


class ApiSkills(ApiBaseModelIfFieldsMatch):
    """Модель скиллов для ответа"""
    id: int
    area_of_application: str
    skill: str


class ApiMatrix(ApiMatrixFromDjangoModel):
    """Базова модель матрицы для ответа"""
    id: int
    name: str
    user: ApiUser
    status: str
    skills: list[ApiSkills]
    created_at: datetime
    completed_at: datetime | None


class ApiGradeSkill(ApiBaseModelIfFieldsMatch):
    """Модель оценки для ответа"""
    id: int
    grade: str
    evaluation_number: int


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class UserLogin(BaseModel):
    """Модель для получения токена"""
    email: str
    password: str



