from fastapi import HTTPException


class EmployeeDir(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Сотрудник уже является директором компании"
        )


class EmployeeInCompany(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Сотрудник уже находится в компании"
        )


class UniqueNameCompany(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Такое название компании уже используется"
        )


class UniqueEmailEmployee(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Email уже используется"
        )


class NotValidEmail(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Некорректный Email"
        )
