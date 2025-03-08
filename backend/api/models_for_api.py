from pydantic import BaseModel
from typing import List


class ApiUser(BaseModel):
    """Модель юзера для ответа"""
    id: int
    email: str
    first_name: str
    last_name: str
    job_title: str


class ApiSkills(BaseModel):
    """Модель скиллов для ответа"""
    id: int
    area_of_application: str
    skill: str


class ApiGradeSkill(BaseModel):
    """Модель оценки для ответа"""
    id: int
    grade: str
    evaluation_number: int


class ApiMatrixGet(BaseModel):
    """Модель для get запроса матрицы"""
    skills: list[ApiSkills]
    grade: list[ApiGradeSkill]


class ApiSkillsGradeMatrix(BaseModel):
    """Модель для post запросов матрицы.
    Получение скилла и оценки по одному полю."""
    skills: str
    grade: str


class ApiMatrixCreate(BaseModel):
    """Модель для post запросов матрицы.
    Получение юзера по id и модели получения скилла и оценки
    в виде списка объекта."""
    user: int
    matrix: list[ApiSkillsGradeMatrix]


class ApiSkillsGradeMatrixResponse(BaseModel):
    """Модель для ответа на пост запрос матрицы.
    Скилл и оценка в виде объекта."""
    skills: ApiSkills
    grade: ApiGradeSkill


class ApiMatrixCreateResponse(BaseModel):
    """Модель для ответа на пост запрос матрицы.
    Юзер в виде объекта и список объектов силла и оценки."""
    user: ApiUser
    matrix: list[ApiSkillsGradeMatrixResponse]
