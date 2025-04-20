from pydantic import BaseModel


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
    employees: list[int] | None = None


class ApiCompanyUpdate(BaseModel):
    """Модель запроса обновления компании"""
    name: str
    is_active: bool


class ApiCompanyUpdateDirector(BaseModel):
    """Модель обновления директора компании"""
    new_director: int


class ApiCompanyUpdateEmployees(BaseModel):
    """Модель удаления сотрудников из компании"""
    employees: list[int]


class ApiRefreshToken(BaseModel):
    """Модель для получения рефреш токена"""
    refresh_token: str


class ApiTemplateMatrixUpdateOrCreate(BaseModel):
    name: str
    skills: list[int]
