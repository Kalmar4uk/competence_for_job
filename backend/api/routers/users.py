from datetime import timedelta

from api.auth import (get_access_and_refresh_tekens, get_current_user,
                      oauth2_scheme)
from api.models_for_api.auth_models import Token, UserLogin
from api.models_for_api.base_model import ApiUser
from api.models_for_api.model_request import UserRegistration
from api.models_for_api.models_response import (ApiCompanyForUserList,
                                                ApiUserResponse,
                                                ApiUserPagination)
from api.routers.routers import router_token, router_users
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from fastapi import Depends, HTTPException, Query, status
from tokens.models import (BlackListAccessToken, BlackListRefreshToken,
                           RefreshToken)

User = get_user_model()


@router_users.get("/me", response_model=ApiUserResponse)
def read_users_me(current_user: ApiUserResponse = Depends(get_current_user)):
    """Выводит текущего пользователя из токена"""
    return current_user


@router_users.get("/{user_id}", response_model=ApiUserResponse)
def get_user(
    user_id: int,
    current_user: ApiUserResponse = Depends(get_current_user)
):
    """Выводит пользователя по id"""
    try:
        user = get_object_or_404(User, id=user_id)
    except Http404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сотрудника с id {user_id} нет в базе"
        )
    return ApiUserResponse.from_django_model(
        user, ApiCompanyForUserList(
            id=user.company.id, name=user.company.name
        ) if user.company else None
    )


@router_users.get("/", response_model=ApiUserPagination)
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


@router_users.post("/registration", response_model=ApiUser)
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегестрирован."
        )
    user_data = from_data.model_dump()
    password = user_data.pop("password")
    new_user = User.objects.create(**user_data)
    new_user.set_password(password)
    new_user.save()
    return ApiUser.from_django_model(new_user)


@router_token.post("/login", response_model=Token)
def login_for_access_token(form_data: UserLogin):
    """Авторизация пользователя/получение токенов"""
    user = authenticate(email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, refresh_token = get_access_and_refresh_tekens(
        data={"sub": user.email}
    )

    exp_refresh_token = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    RefreshToken.objects.create(
        user=user,
        refresh_token=refresh_token,
        expires_at=timezone.now() + exp_refresh_token
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )


@router_token.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(
    current_user: ApiUser = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Выход пользователя из авторизации"""
    user = User.objects.get(email=current_user.email)
    refresh_tokens = RefreshToken.objects.filter(user=user)
    for refresh in refresh_tokens:
        BlackListRefreshToken.objects.create(
            user=user,
            token=refresh.refresh_token,
            expires_at=refresh.expires_at
        )
        refresh.delete()

    BlackListAccessToken.objects.create(
        user=user,
        token=token
    )
