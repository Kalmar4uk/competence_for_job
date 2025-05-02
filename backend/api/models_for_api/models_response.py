from datetime import datetime

from api.core.base_from_django_model import ApiCompanyFromDjangoModel
from api.models_for_api.base_model import (ApiBasePagination, ApiCompany,
                                           ApiGrades, ApiMatrix, ApiSkills,
                                           ApiTemplateMatrix, ApiUser)
from pydantic import BaseModel, Field


class ApiCompanyBaseGet(ApiCompany):
    """Модель компании для ответа"""
    director: ApiUser
    employees: list[ApiUser] | None = None
    created_at: datetime
    closed_at: datetime | None = None


class ApiCompanyForUser(ApiCompanyFromDjangoModel):
    id: int = Field(examples=[1])
    name: str = Field(examples=["Абракадабра"])


class ApiTemplateMatrixBaseGet(ApiTemplateMatrix):
    """Модель шаблона матрицы для ответа"""
    author: ApiUser | None = None
    company: ApiCompany | None = None
    skills: list[ApiSkills]


class ApiUserResponse(ApiUser):
    """Модель юзера с компанией для ответа"""
    company: ApiCompanyForUser | None = None


class ApiUserPagination(ApiBasePagination):
    """Модель пагинации юзера"""
    result: list[ApiUserResponse]


class ApiCompanyPagination(ApiBasePagination):
    """Модель пагинации компании"""
    result: list[ApiCompanyBaseGet]


class ApiTemplateMatrixPaginator(ApiBasePagination):
    """Модель пагинации шаблонов матрицы"""
    result: list[ApiTemplateMatrixBaseGet]


class ApiSkillsPaginator(ApiBasePagination):
    """Модель пагинации навыков"""
    result: list[ApiSkills]


class ApiSkillsAndGradesForMatrix(ApiSkills):
    """Модель навыка с добавленной оценкой"""
    grade: ApiGrades


class ApiMatrixForResponse(ApiMatrix):
    """Модель матрицы с навыками и оценками навыков"""
    skills: list[ApiSkillsAndGradesForMatrix]


class ApiMatrixForResponseRevision(ApiMatrixForResponse):
    """Модель матрицы с комментарием для возвратных"""
    comment: str = Field(examples=[
        "Необходимо отработать повторно, есть сомнения, "
        "что ты на экспертном уровне знаешь как включить ПК"
        ], max_length=100
    )


class ApiMatrixForResponseWithStatusAndLastUpdateFields(BaseModel):
    """Модель матрицы с новым статусои и датой изменения (только эти поля)"""
    status: str = Field(examples=["В процессе"])
    last_update_status: datetime
