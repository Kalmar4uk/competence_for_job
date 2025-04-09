from datetime import timedelta

import jwt
from api.auth import get_access_and_refresh_tekens, oauth2_scheme
from api.permissions import get_current_user
from api.models_for_api.auth_models import Token, UserLogin
from api.models_for_api.base_model import ApiUser
from api.models_for_api.model_request import ApiRefreshToken
from api.routers.routers import router_token
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from tokens.models import (BlackListAccessToken, BlackListRefreshToken,
                           RefreshToken)
from users.models import User


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


@router_token.post("/refresh_token", response_model=Token)
def update_tokens_through_refresh(
    refresh_token_request: ApiRefreshToken,
    current_user: User = Depends(get_current_user)
):
    try:
        payload = jwt.decode(
            refresh_token_request.refresh_token,
            settings.SECRET_KEY_JWT,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        token_type: str = payload.get("token_type")
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный токен"
        )
    if current_user.email != email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не принадлежит сотруднику"
        )
    if token_type != "refresh_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Тип токена не соответствует"
        )

    refresh_token_in_db = RefreshToken.objects.get(
        refresh_token=refresh_token_request.refresh_token,
        user=current_user
    )
    if (
        refresh_token_in_db.expires_at < timezone.now() or
        BlackListRefreshToken.objects.filter(
            token=refresh_token_in_db
        ).exists()
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректный токен"
        )

    BlackListRefreshToken.objects.create(
        user=current_user,
        token=refresh_token_in_db.refresh_token,
        expires_at=refresh_token_in_db.expires_at
    )

    access_token, refresh_token = get_access_and_refresh_tekens(
        data={"sub": current_user.email}
    )

    exp_refresh_token = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    RefreshToken.objects.create(
        user=current_user,
        refresh_token=refresh_token,
        expires_at=timezone.now() + exp_refresh_token
    )

    refresh_token_in_db.delete()

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )
