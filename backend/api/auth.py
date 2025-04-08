from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from tokens.models import BlackListAccessToken
from users.models import User
from api.models_for_api.model_request import ApiRefreshToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(email: str, password: str):
    user = authenticate(email=email, password=password)
    if not user:
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = timezone.now() + expires_delta
    else:
        expire = timezone.now() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY_JWT,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_access_and_refresh_tekens(data: dict):
    data_for_access = data.copy()
    data_for_access.update(token_type="access_token")
    exp_access_token = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data_for_access,
        expires_delta=exp_access_token
    )

    data_for_refresh = data.copy()
    data_for_refresh.update(token_type="refresh_token")
    exp_refresh_token = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_token(
        data_for_refresh,
        expires_delta=exp_refresh_token
    )

    return access_token, refresh_token


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Необходимо авторизоваться",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY_JWT,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    if BlackListAccessToken.objects.filter(token=token).exists():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен",
        )

    try:
        user = get_object_or_404(User, email=email)
    except Http404:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Сотрудник не найден"
        )

    return user


def get_current_user_is_director_or_admin(
        current_user: User = Depends(get_current_user)
):
    if current_user.is_director or current_user.is_staff:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Недостаточно прав",
    )
