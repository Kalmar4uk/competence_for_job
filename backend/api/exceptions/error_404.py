from fastapi import HTTPException


class CompanyNotFound(HTTPException):
    def __init__(self, company_id: int):
        super().__init__(
            status_code=404,
            detail=f"Компания с id {company_id} не найдена"
        )


class UserNotFound(HTTPException):
    def __init__(self, user_id: int | None = None, email: str | None = None):
        if email:
            super().__init__(
                status_code=404,
                detail=f"Сотрудник с email {email} не найден"
            )
        else:
            super().__init__(
                status_code=404,
                detail=f"Сотрудник с id {user_id} не найден"
            )


class TemplateMatrixNotFound(HTTPException):
    def __init__(self, template_id: int):
        super().__init__(
            status_code=404,
            detail=f"Шаблон матрицы с id {template_id} не найден"
        )


class MatrixNotFound(HTTPException):
    def __init__(self, matrix_id: int):
        super().__init__(
            status_code=404,
            detail=f"Матрица с id {matrix_id} не найден"
        )
