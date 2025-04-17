from fastapi import HTTPException


class CompanyNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Компания не найдена"
        )


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Сотрудник(-и) не найден(-ы)"
        )


class TemplateMatrixNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Шаблон матрицы не найден"
        )
