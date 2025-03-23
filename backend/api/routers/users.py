from datetime import timedelta

from api.auth import (authenticate_user, get_access_and_refresh_tekens,
                      get_current_active_user)
from api.models_for_api.base_model import ApiUser, Token, UserLogin
from django.conf import settings
from django.contrib.auth import authenticate
from fastapi import APIRouter, Depends, HTTPException, status
from users.models import RefreshToken

router_auth = APIRouter(prefix="/token", tags=["auth"])
router_users = APIRouter(prefix="/users", tags=["users"])


@router_auth.post("/", response_model=Token)
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

    RefreshToken.objects.create(
        user=user,
        refresh_token=refresh_token
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )


@router_users.get("/me", response_model=ApiUser)
def read_users_me(current_user: ApiUser = Depends(get_current_active_user)):
    return current_user
