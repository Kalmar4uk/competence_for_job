from fastapi import APIRouter

router_token = APIRouter(prefix="/token", tags=["Токены"])
router_users = APIRouter(prefix="/users", tags=["Пользователь"])
router_companies = APIRouter(prefix="/companies", tags=["Компания"])
router_template_matrix = APIRouter(
    prefix="/template_matrix",
    tags=["Шаблон матрицы"]
)
router_matrix = APIRouter(prefix="/matrix", tags=["Матрица"])
router_skills = APIRouter(prefix="/skills", tags=["Навык"])
router_grades = APIRouter(prefix="/grades", tags=["Оценка"])


tags_metadata: list[dict[str, str]] = [
    {
        "name": "Пользователь",
        "description": "Эндпоинты для работы с пользователями",
    },
    {
        "name": "Токены",
        "description": "Эндпоинты для работы с токенами"
    },
    {
        "name": "Компания",
        "description": "Эндпоинты для работы с компаниями"
    },
    {
        "name": "Шаблон матрицы",
        "description": "Эндпоинты для работы с шаблонами матриц"
    },
    {
        "name": "Матрица",
        "description": "Эндпоинты для работы с матрицами"
    },
    {
        "name": "Навык",
        "description": "Эндпоинты для работы с навыками"
    },
    {
        "name": "Оценка",
        "description": "Эндпоинты для работы с оценками"
    }
]
