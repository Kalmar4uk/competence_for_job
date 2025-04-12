from api.permissions import (get_current_user,
                             get_current_user_is_director_or_admin)
from api.models_for_api.base_model import ApiUser
from api.models_for_api.model_request import (ApiCompanyDeleteEmployees,
                                              ApiCompanyUpdate,
                                              ApiCompanyUpdateDirector,
                                              CompanyRegistration)
from api.exceptions.error_404 import CompanyNotFound, UserNotFound
from api.exceptions.error_422 import (EmployeeDir,
                                      EmployeeInCompany,
                                      UniqueNameCompany)
from api.exceptions.error_403 import NotRights
from api.models_for_api.models_response import ApiCompanyBaseGet
from api.routers.routers import router_companies
from companies.models import Company
from django.db.utils import IntegrityError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from fastapi import Depends, status
from users.models import User
from fastapi.exception_handlers import http_exception_handler


@router_companies.get("/", response_model=list[ApiCompanyBaseGet], responses={401: {}})
def get_list_companies(current_user: User = Depends(get_current_user)):
    """Выводит список всех активных компаний"""
    companies = Company.objects.filter(
        is_active=True
    ).prefetch_related(
        "users"
    ).order_by(
        "-created_at"
    )

    api_company_list = []
    api_users_list = []

    for company in companies:
        director_data = company.director
        director = ApiUser.from_django_model(director_data)
        for user in company.users.all():
            if user == director_data:
                continue
            api_users_list.append(ApiUser.from_django_model(user))
        api_company_list.append(
            ApiCompanyBaseGet.from_django_model(
                company, director, api_users_list
            )
        )
        api_users_list.clear()

    return api_company_list


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
        if current_user.is_director:
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
    current_user.is_director = True
    current_user.save()
    user_api = ApiUser.from_django_model(current_user)
    if from_data.employees:
        api_user_list = []
        for employee in from_data.employees:
            try:
                user_data = get_object_or_404(User, id=employee)
            except Http404:
                print(f"Сотрудника с id {employee} в базе нет")  # Вывести в логи при добавлении логов, а принт убрать
            else:
                user_data.company = company
                api_user_list.append(ApiUser.from_django_model(user_data))
        return ApiCompanyBaseGet.from_django_model(
            company,
            user_api,
            api_user_list
        )
    return ApiCompanyBaseGet.from_django_model(
        company,
        user_api
    )


@router_companies.patch(
        "/{company_id}",
        response_model=ApiCompanyBaseGet,
        responses={403: {}, 404: {}, 401: {}}
    )
def update_company(
    company_id: int,
    from_data: ApiCompanyUpdate,
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """Обновление компании по id"""
    if current_user.company.id != company_id:
        raise NotRights()

    try:
        current_company = get_object_or_404(Company, id=company_id)
    except Http404:
        raise CompanyNotFound()

    if from_data.is_active:
        if from_data.employees:
            User.objects.filter(
                id__in=from_data.employees,
                company__isnull=True
            ).update(
                company=current_company,
                date_of_employment=timezone.now().date(),
                date_of_dismissal=None
            )
        employees_data = current_company.users.exclude(groups__id=1)
        employees_company = [
            ApiUser.from_django_model(
                employee
            ) for employee in employees_data
        ]
        current_company.name = from_data.name
        current_company.save()

        user_api = ApiUser.from_django_model(current_user)

        return ApiCompanyBaseGet.from_django_model(
            current_company,
            user_api,
            employees_company
        )

    if not from_data.is_active:
        User.objects.filter(
            company=current_company,
            is_director=False
        ).update(
            company=None
        )
        current_company.is_active = from_data.is_active
        current_company.save()

        user_api = ApiUser.from_django_model(current_user)

        return ApiCompanyBaseGet.from_django_model(
            current_company,
            user_api
        )


@router_companies.patch(
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

    if new_dir.is_director:
        raise EmployeeDir()

    current_user.is_director = False
    current_user.save()

    new_dir.is_director, new_dir.company = True, current_company
    new_dir.save()

    current_company.director = new_dir
    current_company.save()

    new_dir_api = ApiUser.from_django_model(new_dir)
    employees_company = [
        ApiUser.from_django_model(
            employee
        ) for employee in current_company.users.exclude(
            is_director=True
        )
    ]

    return ApiCompanyBaseGet.from_django_model(
        current_company,
        new_dir_api,
        employees_company
    )


@router_companies.delete(
        "/{company_id}/delete_employees",
        response_model=ApiCompanyBaseGet,
        responses={404: {}, 401: {}}
    )
def delete_employees_company(
    company_id: int,
    from_data: ApiCompanyDeleteEmployees,
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """Удаление сотрудника из компании по его id"""
    try:
        current_company = get_object_or_404(Company, id=company_id)
    except Http404:
        raise CompanyNotFound()

    for employee in current_company.users.all():
        if employee.id in from_data.employees:
            employee.company = None
            employee.date_of_dismissal = timezone.now().date()
            employee.save()
    dir_company = ApiUser.from_django_model(current_user)
    employees_company = [
        ApiUser.from_django_model(
            employee
        ) for employee in current_company.users.exclude(
            is_director=True
        )
    ]
    return ApiCompanyBaseGet.from_django_model(
        current_company,
        dir_company,
        employees_company
    )
