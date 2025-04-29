from fastapi import HTTPException


class EmployeeDir(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Сотрудник уже является директором компании"
        )


class EmployeeInCompany(HTTPException):
    def __init__(self, user_id):
        super().__init__(
            status_code=422,
            detail=f"Сотрудник с id {user_id} уже находится в компании"
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


class DoesNotMatchCountSkill(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=422,
            detail="Кол-во навыков не совпадает с исходным кол-вом"
        )


class BadSkillInRequest(HTTPException):
    def __init__(self, skills: list[str]):
        super().__init__(
            status_code=422,
            detail=(
                f"Были обнаружены навыки которые "
                f"отсутствовали в исходной матрице {skills}"
            )
        )


class SkillAlreadyExists(HTTPException):
    def __init__(self, name: str):
        super().__init__(
            status_code=422,
            detail=f"Навык '{name}' уже есть"
        )
