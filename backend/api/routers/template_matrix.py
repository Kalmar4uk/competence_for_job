from api.permissions import get_current_user
from api.exceptions.error_404 import UserNotFound
from api.exceptions.error_422 import UniqueEmailEmployee, NotValidEmail
from api.models_for_api.base_model import ApiUser, ApiSkills, ApiCompany
from api.models_for_api.model_request import UserRegistration
from api.models_for_api.models_response import (ApiCompanyForUserList,
                                                ApiUserResponse,
                                                ApiUserPagination,
                                                ApiTemplateMatrixBaseGet,
                                                ApiTemplateMatrixPaginator)
from api.routers.routers import router_template_matrix
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, HTTPException, Query, status
from users.models import User
from companies.models import Company
from matrix.models import TemplateMatrix


@router_template_matrix.get("/", response_model=ApiTemplateMatrixPaginator)
def get_template_matrix_list(
    page: int = Query(
        1,
        description="Номер страницы"
    ),
    limit: int = Query(
        10,
        le=50,
        description="Указать кол-во шаблонов матриц если требуется"
    ),
):
    """Выводит все шаблоны матриц которые есть в базе"""
    template_matrix_data = TemplateMatrix.objects.prefetch_related("skills")

    offset = (page - 1) * limit
    count = template_matrix_data.count()
    template_matrix_limit = template_matrix_data[offset:offset+limit]

    template_matrix: list[ApiTemplateMatrixBaseGet] = []

    for template in template_matrix_limit:
        skills = [
            ApiSkills(
                id=skill.id,
                area_of_application=skill.area_of_application,
                skill=skill.skill
            ) for skill in template.skills.all()
        ]

        author_data = template.author
        author = ApiUser.from_django_model(
            author_data
        ) if author_data else None

        company_data = template.company
        company = ApiCompany(
            id=company_data.id,
            name=company_data.name,
            is_active=company_data.is_active
        ) if company_data else None

        template_matrix.append(
            ApiTemplateMatrixBaseGet(
                id=template.id,
                name=template.name,
                created_at=template.created_at,
                author=author,
                company=company,
                skills=skills
            )
        )
    next = page + 1 if offset + limit < count else None
    previous = page - 1 if page > 1 else None

    return ApiTemplateMatrixPaginator(
        count=count,
        next=next,
        previous=previous,
        result=template_matrix
    )
