import jwt
from api.exceptions.error_401 import NotValidToken, NotAuth
from api.exceptions.error_403 import NotRights
from api.exceptions.error_404 import UserNotFound
from django.conf import settings
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from fastapi import Depends
from jwt.exceptions import InvalidTokenError
from tokens.models import BlackListAccessToken
from users.models import User
from api.auth import oauth2_scheme


def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise NotAuth()
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY_JWT,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise NotValidToken()
    except InvalidTokenError:
        raise NotValidToken()
    if BlackListAccessToken.objects.filter(token=token).exists():
        raise NotValidToken()

    try:
        user = get_object_or_404(User, email=email)
    except Http404:
        raise UserNotFound()

    return user


def get_current_user_is_director_or_admin(
        current_user: User = Depends(get_current_user)
):
    if current_user.is_director or current_user.is_staff:
        return current_user
    raise NotRights()
