from api.exceptions.error_403 import NotRights
from api.exceptions.error_404 import CompanyNotFound, UserNotFound
from api.exceptions.error_422 import (EmployeeDir, EmployeeInCompany,
                                      UniqueNameCompany)
from api.models_for_api.base_model import ApiUser
from api.models_for_api.model_request import (ApiCompanyUpdateEmployees,
                                              ApiCompanyUpdate,
                                              ApiCompanyUpdateDirector,
                                              CompanyRegistration)
from api.models_for_api.models_response import (ApiCompanyBaseGet,
                                                ApiCompanyPagination)
from api.permissions import (dir_group, get_current_user,
                             get_current_user_is_director_or_admin)
from api.routers.utils import added_employees_in_company, delete_employees_with_company
from api.routers.routers import router_companies
from companies.models import Company, OldCompanyEmployee
from django.db.models import Q, QuerySet
from django.db.utils import IntegrityError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from fastapi import Depends, Query
from users.models import User


@router_companies.get(
        "/",
        response_model=ApiCompanyPagination,
        responses={401: {}}
    )
def get_list_companies(
    page: int = Query(
        1,
        description="Номер страницы"
    ),
    limit: int = Query(
        10,
        le=50,
        description="Указать кол-во компаний если требуется"
    ),
    current_user: User = Depends(get_current_user)
):
    """Выводит список всех активных компаний"""

    companies_data = Company.objects.filter(
        is_active=True
    ).prefetch_related(
        "users"
    ).order_by(
        "-created_at"
    )
    offset: int = (page - 1) * limit
    count: int = companies_data.count()
    companies = companies_data[offset:offset+limit]

    api_company_list: list = []

    for company in companies:
        director_data: User = company.director
        director = ApiUser.from_django_model(company.director)
        api_users_list = [
            ApiUser.from_django_model(user)
            for user in company.users.all()
            if user != director_data
        ]
        api_company_list.append(
            ApiCompanyBaseGet.from_django_model(
                company, director, api_users_list
            )
        )

    next: int | None = page + 1 if offset + limit < count else None
    previous: int | None = page - 1 if page > 1 else None

    return ApiCompanyPagination(
        count=count,
        next=next,
        previous=previous,
        result=api_company_list
    )


@router_companies.get(
        "/{company_id}",
        response_model=ApiCompanyBaseGet,
        responses={404: {}, 401: {}}
    )
def get_company(
    company_id: int,
    current_user: ApiUser = Depends(get_current_user)
):
    """Выводит компанию по id"""

    try:
        current_company = get_object_or_404(Company, id=company_id)
    except Http404:
        raise CompanyNotFound()

    director = ApiUser.from_django_model(current_company.director)
    users = [
        ApiUser.from_django_model(
            user
        ) for user in current_company.users.all()
        if not user.groups.filter(id=1).exists()
    ]

    return ApiCompanyBaseGet.from_django_model(
        current_company, director, users
    )


@router_companies.post(
        "/",
        response_model=ApiCompanyBaseGet,
        status_code=201,
        responses={422: {}, 401: {}}
    )
def registration_company(
    from_data: CompanyRegistration,
    current_user: User = Depends(get_current_user)
):
    """
    Регистрация компании.
    Список сотрудников не обязателен, может быть не передан вовсе
    """
    if current_user.company:
        if current_user.groups.filter(id=1):
            raise EmployeeDir()
        else:
            raise EmployeeInCompany()
    try:
        company = Company.objects.create(
            name=from_data.name,
            director=current_user
        )
    except IntegrityError:
        raise UniqueNameCompany()

    current_user.company = company
    current_user.save()
    dir_group(current_user)

    user_api = ApiUser.from_django_model(current_user)

    if from_data.employees:
        api_user_list = added_employees_in_company(
            company=company,
            employees=from_data.employees
        )
        return ApiCompanyBaseGet.from_django_model(
            company,
            user_api,
            api_user_list
        )
    return ApiCompanyBaseGet.from_django_model(
        company,
        user_api
    )


@router_companies.put(
        "/{company_id}",
        response_model=ApiCompanyBaseGet,
        responses={403: {}, 404: {}, 401: {}}
    )
def update_name_and_status_company(
    company_id: int,
    from_data: ApiCompanyUpdate,
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """Обновление названия и статуса компании по id"""
    if current_user.company.id != company_id:
        raise NotRights()

    try:
        current_company = get_object_or_404(Company, id=company_id)
    except Http404:
        raise CompanyNotFound()

    employees_data: QuerySet[User] = (
        current_company.users.exclude(groups__id=1)
    )

    if not from_data.is_active:
        current_company.is_active = from_data.is_active
        current_company.save()

        for employee in employees_data:
            employee.company = None
            employee.date_of_dismissal = timezone.now().date()
            employee.save()
            OldCompanyEmployee.objects.create(
                company=current_company,
                user=employee,
                job_title=employee.job_title,
                date_of_employment=employee.date_of_employment,
                date_of_dismissal=employee.date_of_dismissal,
            )

        user_api = ApiUser.from_django_model(current_user)

        return ApiCompanyBaseGet.from_django_model(
            current_company,
            user_api
        )

    employees_company = [
        ApiUser.from_django_model(
            employee
        ) for employee in employees_data
    ]
    current_company.name = from_data.name
    current_company.save()

    user_api = ApiUser.from_django_model(current_company.director)

    return ApiCompanyBaseGet.from_django_model(
        current_company,
        user_api,
        employees_company
    )


@router_companies.put(
        "/{company_id}/update_director",
        response_model=ApiCompanyBaseGet,
        responses={404: {}, 422: {}, 401: {}}
    )
def update_dir_company(
    company_id: int,
    from_data: ApiCompanyUpdateDirector,
    current_user: User = Depends(get_current_user_is_director_or_admin)

):
    """
    Изменение директора компании, старый директор остается
    в компании, но теряет все привелегии директора
    """
    if current_user.id == from_data.new_director:
        raise EmployeeDir()
    try:
        current_company = get_object_or_404(Company, id=company_id)
    except Http404:
        raise CompanyNotFound()
    try:
        new_dir = get_object_or_404(User, id=from_data.new_director)
    except Http404:
        raise UserNotFound()

    if new_dir.groups.filter(id=1):
        raise EmployeeDir()

    dir_group(current_user, True)

    if new_dir.company != current_company:
        new_dir.company = current_company
        new_dir.save()

    dir_group(new_dir)

    current_company.director = new_dir
    current_company.save()

    new_dir_api = ApiUser.from_django_model(new_dir)
    employees_company = [
        ApiUser.from_django_model(
            employee
        ) for employee in current_company.users.exclude(groups__id=1)
    ]

    return ApiCompanyBaseGet.from_django_model(
        current_company,
        new_dir_api,
        employees_company
    )


@router_companies.put(
        "/{company_id}/update_employees",
        response_model=ApiCompanyBaseGet,
        responses={404: {}, 401: {}, 403: {}}
    )
def update_employees_company(
    company_id: int,
    from_data: ApiCompanyUpdateEmployees,
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """Обновление сотрудников в компании по его id"""

    try:
        current_company = get_object_or_404(Company, id=company_id)
    except Http404:
        raise CompanyNotFound()

    employees_company_data: QuerySet[int] = (
        current_company.users.exclude(
            groups__id=1
        ).values_list(
            "id",
            flat=True
        )
    )

    for employee in employees_company_data:
        if employee not in from_data.employees:
            delete_employees_with_company(
                employee=employee,
                company=current_company
            )

    new_employees = User.objects.filter(
        id__in=from_data.employees
    ).exclude(
        company=current_company
    ).values_list("id", flat=True)

    if new_employees:
        added_employees_in_company(
            employees=new_employees,
            company=current_company
        )

    dir_company = ApiUser.from_django_model(current_company.director)
    employees_company = [
        ApiUser.from_django_model(
            employee
        ) for employee in current_company.users.exclude(
            groups__id=1
        )
    ]
    return ApiCompanyBaseGet.from_django_model(
        current_company,
        dir_company,
        employees_company
    )
