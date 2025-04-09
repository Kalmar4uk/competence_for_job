import jwt
from django.conf import settings
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from tokens.models import BlackListAccessToken
from users.models import User
from api.auth import oauth2_scheme


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