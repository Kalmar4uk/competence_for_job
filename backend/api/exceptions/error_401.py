from fastapi import HTTPException


class NotValidToken(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Невалидный токен"
        )


class NotValidEmailOrPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Некорректный Email и/или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )


class NotAuth(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Необходимо авторизоваться",
            headers={"WWW-Authenticate": "Bearer"},
        )


class NotValidPassowod(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Введен некорректный текущий пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
