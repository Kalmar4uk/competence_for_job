from fastapi import HTTPException


class NotRights(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Недостаточно прав"
        )
