from pydantic import BaseModel


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