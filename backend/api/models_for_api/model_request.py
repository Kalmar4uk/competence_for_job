from pydantic import BaseModel


class ApiGradeForCreateMatrix(BaseModel):
    grade: str


class ApiSkillsForCreateMatrix(BaseModel):
    skill: str
    grade: ApiGradeForCreateMatrix


class ApiMatrixCreate(BaseModel):
    """Модель для patch запроса матрицы"""
    matrix: list[ApiSkillsForCreateMatrix]


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
    director: int
    employees: list[int] | None = None
