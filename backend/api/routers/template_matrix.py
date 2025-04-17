from api.exceptions.error_404 import (CompanyNotFound,
                                      UserNotFound,
                                      TemplateMatrixNotFound)
from api.exceptions.error_422 import NotValidEmail, UniqueEmailEmployee
from api.models_for_api.base_model import ApiCompany, ApiSkills, ApiUser
from api.models_for_api.model_request import ApiTemplateMatrixCreate
from api.models_for_api.models_response import (ApiCompanyForUserList,
                                                ApiTemplateMatrixBaseGet,
                                                ApiTemplateMatrixPaginator,
                                                ApiUserPagination,
                                                ApiUserResponse)
from api.permissions import get_current_user
from api.routers.routers import router_template_matrix
from companies.models import Company
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, HTTPException, Query, status
from matrix.models import TemplateMatrix, Skill
from users.models import User


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
    company: int = Query(None, description="ID компании"),
    author: int = Query(None, description="ID автора"),
    current_user: User = Depends(get_current_user)
):
    """Выводит все шаблоны матриц которые есть в базе"""
    if company:
        if author:
            try:
                author_data = get_object_or_404(User, id=author)
            except Http404:
                raise UserNotFound
            try:
                company_data = get_object_or_404(Company, id=company)
                template_matrix_data = (
                    company_data.template_matrix.filter(
                        author=author_data
                    ).prefetch_related(
                        "skills"
                    )
                )
            except Http404:
                raise CompanyNotFound
        else:
            try:
                company_data = get_object_or_404(Company, id=company)
                template_matrix_data = (
                    company_data.template_matrix.prefetch_related("skills")
                )
            except Http404:
                raise CompanyNotFound
    elif author:
        try:
            author_data = get_object_or_404(User, id=author)
            template_matrix_data = (
                author_data.template_matrix.prefetch_related("skills")
            )
        except Http404:
            raise UserNotFound
    else:
        template_matrix_data = TemplateMatrix.objects.prefetch_related(
            "skills"
        )

    offset = (page - 1) * limit
    count = template_matrix_data.count()
    template_matrix_limit = template_matrix_data[offset:offset+limit]

    template_matrix: list[ApiTemplateMatrixBaseGet] = []

    for template in template_matrix_limit:
        skills = [
            ApiSkills.from_django_model(
                skill
            ) for skill in template.skills.all()
        ]

        try:
            if author_data:
                pass
        except UnboundLocalError:
            author_data = template.author

        author_api = ApiUser.from_django_model(
            author_data
        ) if author_data else None

        try:
            if company_data:
                pass
        except UnboundLocalError:
            company_data = template.company

        company_api = ApiCompany(
            id=company_data.id,
            name=company_data.name,
            is_active=company_data.is_active
        ) if company_data else None

        template_matrix.append(
            ApiTemplateMatrixBaseGet.from_django_model(
                template,
                author_api,
                company_api,
                skills
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


@router_template_matrix.get("/{template_matrix_id}", response_model=ApiTemplateMatrixBaseGet)
def get_template_matrix(template_matrix_id: int):
    """Выводит шаблон матрицы по id"""
    try:
        template_matrix_data = get_object_or_404(TemplateMatrix, id=template_matrix_id)
    except Http404:
        raise TemplateMatrixNotFound

    author_data = template_matrix_data.author
    author_api = ApiUser.from_django_model(author_data) if author_data else None

    company_data = template_matrix_data.company
    company_api = ApiCompany(
        id=company_data.id,
        name=company_data.name,
        is_active=company_data.is_active
    ) if company_data else None

    skills_api = [
        ApiSkills.from_django_model(
            skill
        ) for skill in template_matrix_data.skills.all()
    ]

    return ApiTemplateMatrixBaseGet.from_django_model(
        template_matrix_data,
        author_api,
        company_api,
        skills_api
    )


@router_template_matrix.post("/", response_model=ApiTemplateMatrixBaseGet)
def matrix_template(from_data: ApiTemplateMatrixCreate):
    name = from_data.name
    try:
        author_data = get_object_or_404(User, id=from_data.author)
    except Http404:
        raise UserNotFound
    company_data = author_data.company
    skills = Skill.objects.filter(id__in=from_data.skills)
    template_matrix = TemplateMatrix.objects.create(
        name=name,
        author=author_data,
        company=company_data
    )
    template_matrix.skills.set(skills)

    author_api = ApiUser.from_django_model(author_data)
    company_api = ApiCompany(
        id=company_data.id,
        name=company_data.name,
        is_active=company_data.is_active
    )
    skills_api = [
        ApiSkills.from_django_model(skill) for skill in skills
    ]

    return ApiTemplateMatrixBaseGet.from_django_model(
        template_matrix,
        author_api,
        company_api,
        skills_api
    )
