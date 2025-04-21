from pydantic import BaseModel, Field


class Token(BaseModel):
    """Модель токенов"""
    access_token: str = Field(examples=["dfsadfasfsdfsdfsd.ewqeqwe1213"])
    refresh_token: str = Field(examples=["ipoieopwqensbadsad.sdawe123"])
    token_type: str = Field(examples=["Bearer"])


class UserLogin(BaseModel):
    """Модель для получения токена"""
    email: str = Field(examples=["olezha.korotky@mail.ru"])
    password: str = Field(examples=["Aotydfsabfdsjk145"])
