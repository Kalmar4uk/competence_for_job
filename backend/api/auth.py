from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


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
