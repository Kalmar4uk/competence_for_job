from datetime import datetime

from api.core.base_from_django_model import ApiMatrixFromDjangoModel
from pydantic import BaseModel

from .base_model import ApiGradeSkill, ApiMatrix, ApiSkills, ApiUser


class ApiMatrixSkillsGrade(ApiSkills):
    grade: ApiGradeSkill


class ApiMatrixListSkills(ApiMatrix):
    """Модель скиллов для ответа"""
    skills: list[ApiSkills]


class ApiMatrixWithGrade(ApiMatrix):
    """Модель для запроса матрицы c оценками"""
    skills: list[ApiMatrixSkillsGrade]


class ApiSkillsGradeMatrixResponse(BaseModel):
    """Модель для ответа на пост запрос матрицы.
    Скилл и оценка в виде объекта."""
    skills: ApiSkills
    grade: ApiGradeSkill
    created_at: datetime


class ApiMatrixCreateResponse(BaseModel):
    """Модель для ответа на пост запрос матрицы.
    Юзер в виде объекта и список объектов силла и оценки."""
    user: ApiUser
    competence: list[ApiSkillsGradeMatrixResponse]
