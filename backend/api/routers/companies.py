from api.auth import get_current_user, get_current_user_is_director_or_admin
from api.models_for_api.base_model import ApiCompany, ApiUser
from api.models_for_api.model_request import (ApiCompanyUpdate,
                                              ApiCompanyUpdateDirector,
                                              CompanyRegistration)
from api.models_for_api.models_response import ApiCompanyBaseGet
from api.routers.routers import router_companies
from companies.models import Company
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, HTTPException, status
from users.models import User


@router_companies.get("/", response_model=list[ApiCompanyBaseGet])
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
        director = ApiUser.from_django_model(company.director)
        for user in company.users.all():
            api_users_list.append(ApiUser.from_django_model(user))
        api_company_list.append(
            ApiCompanyBaseGet.from_django_model(
                company, director, api_users_list
            )
        )
        api_users_list.clear()

    return api_company_list


@router_companies.get("/{company_id}", response_model=ApiCompanyBaseGet)
def get_company(
    company_id: int,
    current_user: ApiUser = Depends(get_current_user)
):
    """Выводит компанию по id"""

    try:
        current_company = get_object_or_404(Company, id=company_id)
    except Http404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Комапнии с id {company_id} в базе нет"
        )

    director = ApiUser.from_django_model(current_company.director)
    users = [
        ApiUser.from_django_model(
            user
        ) for user in current_company.users.all()
    ]

    return ApiCompanyBaseGet.from_django_model(
        current_company, director, users
    )


@router_companies.post("/", response_model=ApiCompanyBaseGet)
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
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Сотрудник уже является директором компании"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Сотруднику необходимо сначала выйти из компании"
            )
    try:
        company = Company.objects.create(
            name=from_data.name,
            director=current_user
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Такое название компании уже используется"
        )
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


@router_companies.patch("/{company_id}", response_model=ApiCompanyBaseGet)
def update_company(
    company_id: int,
    from_data: ApiCompanyUpdate,
    current_user: User = Depends(get_current_user_is_director_or_admin)
):
    """Обновление компании по id"""
    if current_user.company.id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )

    try:
        current_company = get_object_or_404(Company, id=company_id)
    except Http404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Комапнии с id {company_id} в базе нет"
        )

    if from_data.is_active:
        if from_data.employees:
            User.objects.filter(
                id__in=from_data.employees,
                company__isnull=True
            ).update(
                company=current_company
            )
        employees_data = current_company.users.exclude(is_director=True)
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
        response_model=ApiCompanyBaseGet
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Сотрудник уже является директором этой компании"
        )
    try:
        current_company = get_object_or_404(Company, id=company_id)
    except Http404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Комапнии с id {company_id} в базе нет"
        )
    try:
        new_dir = get_object_or_404(User, id=from_data.new_director)
    except Http404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сотрудника с id {from_data.new_director} в базе нет"
        )
    if new_dir.is_director:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Сотрудник уже является директором другой компании"
        )

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
