import re

from api.permissions import get_current_user
from api.exceptions.error_404 import UserNotFound
from api.exceptions.error_422 import UniqueEmailEmployee, NotValidEmail
from api.models_for_api.base_model import ApiUser
from api.models_for_api.model_request import UserRegistration
from api.models_for_api.models_response import (ApiCompanyForUserList,
                                                ApiUserResponse,
                                                ApiUserPagination)
from api.routers.routers import router_users
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, HTTPException, Query, status
from users.models import User


@router_users.get("/me", response_model=ApiUserResponse, responses={401: {}})
def read_users_me(current_user: ApiUserResponse = Depends(get_current_user)):
    """Выводит текущего пользователя из токена"""
    return current_user


@router_users.get(
        "/{user_id}",
        response_model=ApiUserResponse,
        responses={404: {}, 401: {}}
    )
def get_user(
    user_id: int,
    current_user: ApiUserResponse = Depends(get_current_user)
):
    """Выводит пользователя по id"""
    try:
        user = get_object_or_404(User, id=user_id)
    except Http404:
        raise UserNotFound()
    return ApiUserResponse.from_django_model(
        user, ApiCompanyForUserList(
            id=user.company.id, name=user.company.name
        ) if user.company else None
    )


@router_users.get("/", response_model=ApiUserPagination, responses={401: {}})
def get_users_list(
    page: int = Query(
        1,
        description="Номер страницы"
    ),
    limit: int = Query(
        10,
        le=50,
        description="Указать кол-во сотрудников если требуется"
    ),
    current_user: ApiUser = Depends(get_current_user)
):
    """
    Выводит список всех активных пользователей.
    По умолчанию выдает 10 сотрудников
    """
    offset = (page - 1) * limit
    users_data = User.objects.filter(is_active=True).order_by("-id")
    count = users_data.count()
    users = users_data[offset:offset+limit]
    users_api = [
        ApiUserResponse.from_django_model(
            user, ApiCompanyForUserList(
                id=user.company.id, name=user.company.name
            ) if user.company else None
        ) for user in users
    ]
    next = page + 1 if offset + limit < count else None
    previous = page - 1 if page > 1 else None
    return ApiUserPagination(
        count=count,
        next=next,
        previous=previous,
        result=users_api
    )


@router_users.post(
        "/registration",
        response_model=ApiUser,
        status_code=201,
        responses={422: {}, 401: {}}
    )
def registration_user(from_data: UserRegistration):
    """Регистрация пользователя"""
    try:
        validate_password(from_data.password)
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    if User.objects.filter(email=from_data.email).exists():
        raise UniqueEmailEmployee()

    if not re.search(r"^[\w.]+@[\w]+\.+(ru|com)$", from_data.email):
        raise NotValidEmail()

    user_data = from_data.model_dump()
    password = user_data.pop("password")
    new_user = User.objects.create(**user_data)
    new_user.set_password(password)
    new_user.save()
    return ApiUser.from_django_model(new_user)
