from matrix.constants import AREA_OF_APPLICATION
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class UserUpdate(BaseModel):
    """Модель обновления юзера"""
    email: str = Field(examples=["olezha.korotky@mail.ru"])
    first_name: str = Field(examples=["Олежа"])
    last_name: str = Field(examples=["Короткий"])
    middle_name: str | None = Field(default=None, examples=["Длиннович"])


class UserRegistration(UserUpdate):
    """Модель для регистрации юзера"""
    password: str = Field(examples=["Aotydfsabfdsjk145"])


class UserSetPassword(BaseModel):
    """Модель для обновления пароля"""
    current_password: str = Field(examples=["Aotydfsabfdsjk145"])
    new_password: str = Field(examples=["Idfsfjdsfg091"])


class CompanyRegistration(BaseModel):
    """Модель регистрации компании"""
    name: str = Field(examples=["Абракадабра"])
    employees: list[int] | None = Field(default=None, examples=[[1, 2, 3]])


class ApiCompanyUpdate(BaseModel):
    """Модель запроса обновления компании"""
    name: str = Field(examples=["Абракадабра"])
    is_active: bool


class ApiCompanyUpdateDirector(BaseModel):
    """Модель обновления директора компании"""
    new_director: int = Field(examples=[1])


class ApiCompanyUpdateEmployees(BaseModel):
    """Модель удаления сотрудников из компании"""
    employees: list[int] = Field(examples=[[1, 2, 3]])


class ApiRefreshToken(BaseModel):
    """Модель для получения рефреш токена"""
    refresh_token: str = Field(examples=["dasgdshaj123ghjdsgahjdf.fdhsjkfhds"])


class ApiTemplateMatrixUpdateOrCreate(BaseModel):
    """Модель создания или обновления шаблона матрицы"""
    name: str = Field(examples=["Template matrix"])
    skills: list[int] = Field(examples=[[1, 2, 3]])


class ApiMatrixCreate(BaseModel):
    """Модель создания матрицы"""
    name: str | None = Field(default=None, examples=["Назначенная матрица"])
    employee: list[int] = Field(examples=[[1, 2, 3]])
    template_matrix: int = Field(examples=[1])
    deadline: datetime | None = None


class ApiMatrixInWorkStatus(BaseModel):
    """Модель обновления статуса"""
    status: str = Field(examples=["В процессе"])

    @field_validator("status")
    @classmethod
    def check_status(cls, value: str) -> str:
        if value != "В процессе":
            raise ValueError(
                f"Некорректный статус для матрицы - {value}"
            )
        return value


class ApiGradeForMatrixCompeted(BaseModel):
    """Модель оценки для завершения матрицы"""
    evaluation_number: int = Field(examples=[1])

    @field_validator("evaluation_number")
    @classmethod
    def check_min_max_number(cls, value: int) -> int:
        if value < 0 or value > 5:
            raise ValueError(
                "Значение оценки меньше 0 или больше 5"
            )
        return value


class ApiSkillForMatrixCompleted(BaseModel):
    """Модель навыка для завершения матрицы"""
    skill: str = Field(examples=["Включать компьютер"])
    grade: ApiGradeForMatrixCompeted


class ApiMatrixCompeted(BaseModel):
    """Модель завершения матрицы"""
    name: str = Field(examples=["Назначенная матрица"])
    status: str = Field(examples=["Завершена"])
    skills: list[ApiSkillForMatrixCompleted]

    @field_validator("status")
    @classmethod
    def check_status(cls, value: str) -> str:
        if value != "Завершена":
            raise ValueError(
                f"Некорректный статус для матрицы - {value}"
            )
        return value


class ApiSkillsCreate(BaseModel):
    area_of_application: str = Field(examples=["Hard skill"])
    skill: str = Field(examples=["Включать компьютер"])

    @field_validator("area_of_application")
    @classmethod
    def check_status(cls, value: str) -> str:
        if value not in AREA_OF_APPLICATION:
            raise ValueError(
                f"Некорректный тип навыка - {value}"
            )
        return value
