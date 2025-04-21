from fastapi import HTTPException


class NotValidNewPassword(HTTPException):
    def __init__(self, error=None):
        if not error:
            super().__init__(
                status_code=400,
                detail="Пароли совпадают"
            )
        else:
            super().__init__(
                status_code=400,
                detail=str(error)
            )
