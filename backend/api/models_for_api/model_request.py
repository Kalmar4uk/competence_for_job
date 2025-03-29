from pydantic import BaseModel
from .models_response import ApiMatrixSkillsGrade


class ApiGradeForCreateMatrix(BaseModel):
    grade: str


class ApiSkillsForCreateMatrix(BaseModel):
    skill: str
    grade: ApiGradeForCreateMatrix


class ApiMatrixCreate(BaseModel):
    """Модель для patch запроса матрицы"""
    matrix: list[ApiSkillsForCreateMatrix]
