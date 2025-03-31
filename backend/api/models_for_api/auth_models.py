from pydantic import BaseModel


class Token(BaseModel):
    """Модель токенов"""
    access_token: str
    refresh_token: str
    token_type: str


class UserLogin(BaseModel):
    """Модель для получения токена"""
    email: str
    password: str
