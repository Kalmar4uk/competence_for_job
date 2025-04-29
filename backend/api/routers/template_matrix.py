from api.exceptions.error_403 import NotRights
from api.exceptions.error_404 import (CompanyNotFound, TemplateMatrixNotFound,
                                      UserNotFound)
from api.models_for_api.base_model import ApiCompany, ApiSkills, ApiUser
from api.models_for_api.model_request import ApiTemplateMatrixUpdateOrCreate
from api.models_for_api.models_response import (ApiTemplateMatrixBaseGet,
                                                ApiTemplateMatrixPaginator)
from api.permissions import (get_current_user,
                             get_current_user_is_director_or_admin)
from api.routers.routers import router_template_matrix
from companies.models import Company
from django.db.models import QuerySet
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, Query
from matrix.models import TemplateMatrix
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
                raise UserNotFound(user_id=author)
            try:
                company_data = get_object_or_404(Company, id=company)
                template_matrix_data: QuerySet[TemplateMatrix] = (
                    company_data.template_matrix.filter(
                        author=author_data
                    ).prefetch_related(
                        "skills"
                    )
                )
            except Http404:
                raise CompanyNotFound(company_id=company)
        else:
            try:
                company_data = get_object_or_404(Company, id=company)
                template_matrix_data: QuerySet[TemplateMatrix] = (
                    company_data.template_matrix.prefetch_related("skills")
                )
            except Http404:
                raise CompanyNotFound(company_id=company)
    elif author:
        try:
            author_data = get_object_or_404(User, id=author)
            template_matrix_data: QuerySet[TemplateMatrix] = (
                author_data.template_matrix.prefetch_related("skills")
            )
        except Http404:
            raise UserNotFound
    else:
        template_matrix_data: QuerySet[TemplateMatrix] = (
            TemplateMatrix.objects.prefetch_related(
                "skills"
            )
        )

    offset: int = (page - 1) * limit
    count: int = template_matrix_data.count()
    template_matrix_limit: QuerySet[TemplateMatrix] = (
        template_matrix_data[offset:offset+limit]
    )

    template_matrix: list[ApiTemplateMatrixBaseGet] = []

    for template in template_matrix_limit:
        skills = [
            ApiSkills.from_django_model(
                skill
            ) for skill in template.skills.all()
        ]

        if not author:
            author_data: User = template.author

        author_api = ApiUser.from_django_model(
            model=author_data
        ) if author_data else None

        if not company:
            company_data: Company = template.company

        company_api = (
            ApiCompany.from_django_model(model=company_data)
            if company_data else None
        )

        template_matrix.append(
            ApiTemplateMatrixBaseGet.from_django_model(
                model=template,
                author=author_api,
                company=company_api,
                skills=skills
            )
        )
    next: int = page + 1 if offset + limit < count else None
    previous: int = page - 1 if page > 1 else None

    return ApiTemplateMatrixPaginator(
        count=count,
        next=next,
        previous=previous,
        result=template_matrix
    )


@router_template_matrix.get(
        "/{template_matrix_id}",
        response_model=ApiTemplateMatrixBaseGet
    )
def get_template_matrix(
    template_matrix_id: int,
    current_user: User = Depends(get_current_user)
):
    """Выводит шаблон матрицы по id"""
    try:
        template_matrix_data = get_object_or_404(
            TemplateMatrix,
            id=template_matrix_id
        )
    except Http404:
        raise TemplateMatrixNotFound(template_id=template_matrix_id)

    author_api = (
        ApiUser.from_django_model(author_data)
        if (author_data := template_matrix_data.author) else None
    )

    company_api = (
        ApiCompany.from_django_model(model=company)
        if (company := template_matrix_data.company) else None
    )

    skills_api = [
        ApiSkills.from_django_model(
            model=skill
        ) for skill in template_matrix_data.skills.all()
    ]

    return ApiTemplateMatrixBaseGet.from_django_model(
        model=template_matrix_data,
        author=author_api,
        company=company_api,
        skills=skills_api
    )


@router_template_matrix.post("/", response_model=ApiTemplateMatrixBaseGet)
def template_matrix(
    from_data: ApiTemplateMatrixUpdateOrCreate,
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """Создание шаблона матрицы"""
    name: str = from_data.name
    company_data = current_user.company
    template_matrix = TemplateMatrix.objects.create(
        name=name,
        author=current_user,
        company=company_data
    )
    template_matrix.skills.set(from_data.skills)

    author_api = ApiUser.from_django_model(model=current_user)
    company_api = ApiCompany.from_django_model(model=company_data)
    skills_api = [
        ApiSkills.from_django_model(
            model=skill
        ) for skill in template_matrix.skills.all()
    ]

    return ApiTemplateMatrixBaseGet.from_django_model(
        model=template_matrix,
        author=author_api,
        company=company_api,
        skills=skills_api
    )


@router_template_matrix.patch(
        "/{template_matrix_id}",
        response_model=ApiTemplateMatrixBaseGet
    )
def update_template_matrix(
    template_matrix_id: int,
    from_data: ApiTemplateMatrixUpdateOrCreate,
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """Обновление шаблона матрицы"""
    try:
        template_matrix_data = get_object_or_404(
            TemplateMatrix,
            id=template_matrix_id
        )
    except Http404:
        raise TemplateMatrixNotFound(template_id=template_matrix_id)

    if template_matrix_data.author != current_user:
        raise NotRights()

    template_matrix_data.name = from_data.name
    template_matrix_data.skills.set(from_data.skills)
    template_matrix_data.save()
    author_api = ApiUser.from_django_model(model=template_matrix_data.author)
    company_api = (
        ApiCompany.from_django_model(model=company)
        if (company := template_matrix_data.company) else None
    )
    skills_api = [
        ApiSkills.from_django_model(
            model=skill
        ) for skill in template_matrix_data.skills.all()
    ]

    return ApiTemplateMatrixBaseGet.from_django_model(
        model=template_matrix_data,
        author=author_api,
        company=company_api,
        skills=skills_api
    )
