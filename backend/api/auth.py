from datetime import datetime, timedelta, timezone

import jwt
from api.models_for_api.base_model import ApiUser, TokenData
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

User = get_user_model()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(email: str):
    try:
        user = get_object_or_404(User, email=email)
        return ApiUser(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            job_title=user.job_title
        )
    except Http404:
        return None


def authenticate_user(email: str, password: str):
    user = authenticate(email=email, password=password)
    if not user:
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY_JWT,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_access_and_refresh_tekens(data: dict):
    exp_access_token = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data, expires_delta=exp_access_token)

    exp_refresh_token = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_token(data, expires_delta=exp_refresh_token)

    return access_token, refresh_token


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
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
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
        current_user: ApiUser = Depends(get_current_user)
):
    return current_user
