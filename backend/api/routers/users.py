from datetime import timedelta

from api.auth import (get_access_and_refresh_tekens, get_current_user,
                      oauth2_scheme)
from api.models_for_api.base_model import ApiUser, Token, UserLogin, UserRegistration
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from fastapi import APIRouter, Depends, HTTPException, status
from tokens.models import (BlackListAccessToken, BlackListRefreshToken,
                           RefreshToken)


router_login = APIRouter(prefix="/login", tags=["login"])
router_logout = APIRouter(prefix="/logout", tags=["logout"])
router_users = APIRouter(prefix="/users", tags=["users"])
router_register = APIRouter(prefix="/registration", tags=["registration"])

User = get_user_model()


@router_register.post("/users", response_model=ApiUser)
def registration_user(from_data: UserRegistration):
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


@router_login.post("/", response_model=Token)
def login_for_access_token(form_data: UserLogin):
    user = authenticate(email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
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


@router_logout.post("/", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(
    current_user: ApiUser = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
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


@router_users.get("/me", response_model=ApiUser)
def read_users_me(current_user: ApiUser = Depends(get_current_user)):
    return current_user
