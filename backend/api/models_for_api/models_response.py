from datetime import datetime
from pydantic import BaseModel
from base_model import ApiSkills, ApiGradeSkill, ApiUser


class ApiMatrixGet(BaseModel):
    """Модель для get запроса матрицы"""
    skills: list[ApiSkills]
    grade: list[ApiGradeSkill]


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
