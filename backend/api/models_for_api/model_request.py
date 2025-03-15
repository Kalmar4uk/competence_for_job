from pydantic import BaseModel


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
