from api.models_for_api.base_model import ApiCompany, ApiUser, ApiCompanyUpdate
from api.models_for_api.model_request import CompanyRegistration
from api.routers.routers import router_companies
from companies.models import Company
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, HTTPException, status

User = get_user_model()


@router_companies.post("/registration", response_model=ApiCompany)
def registration_company(from_data: CompanyRegistration):
    try:
        user = get_object_or_404(User, id=from_data.director)
    except Http404 as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
    if user.company:
        if user.is_director:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Сотрудник уже является директором компании"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Сотруднику необходимо сначала выйти из компании"
            )
    try:
        company = Company.objects.create(name=from_data.name)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Такое название компании уже используется"
        )
    user.company = company
    user.is_director = True
    user.save()
    user_api = ApiUser.from_django_model(user)
    return ApiCompany(
        id=company.id,
        name=company.name,
        director=user_api,
        created_at=company.created_at
    )


@router_companies.patch("/{company_id}")
def update_company(from_data: ApiCompanyUpdate):
    pass
