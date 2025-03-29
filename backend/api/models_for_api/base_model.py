from datetime import datetime
from api.core.base_from_django_model import ApiBaseModelIfFieldsMatch, ApiUserFromDjangoModel, ApiMatrixFromDjangoModel
from pydantic import BaseModel


class ApiUser(ApiUserFromDjangoModel):
    """Модель юзера для ответа"""
    id: int
    email: str
    personnel_number: str | None
    first_name: str
    last_name: str
    job_title: str


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


class UserRegistration(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    job_title: str
