from fastapi import HTTPException


class CompanyNotFound(HTTPException):
    def __init__(self, company_id):
        super().__init__(
            status_code=404,
            detail=f"Компания с id {company_id} не найдена"
        )


class UserNotFound(HTTPException):
    def __init__(self, user_id=None, email=None):
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
    def __init__(self, template_id):
        super().__init__(
            status_code=404,
            detail=f"Шаблон матрицы с id {template_id} не найден"
        )


class MatrixNotFound(HTTPException):
    def __init__(self, matrix_id):
        super().__init__(
            status_code=404,
            detail=f"Матрица с id {matrix_id} не найден"
        )
