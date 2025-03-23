from api.core.base_from_django_model import ApiBaseModelIfFieldsMatch
from pydantic import BaseModel


class ApiUser(BaseModel):
    """Модель юзера для ответа"""
    id: int
    email: str
    first_name: str
    last_name: str
    job_title: str


class ApiSkills(ApiBaseModelIfFieldsMatch):
    """Модель скиллов для ответа"""
    id: int
    area_of_application: str
    skill: str


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
    email: str
    password: str
