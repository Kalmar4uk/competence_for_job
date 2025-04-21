from pydantic import BaseModel, Field


class UserUpdate(BaseModel):
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
    name: str = Field(examples=["Template matrix"])
    skills: list[int] = Field(examples=[[1, 2, 3]])


class ApiMatrixCreate(BaseModel):
    name: str | None = Field(default=None, examples=["Назначенная матрица"])
    employee: list[int] = Field(examples=[[1, 2, 3]])
    template_matrix: int = Field(examples=[1])
