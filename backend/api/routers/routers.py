from fastapi import APIRouter

router_token = APIRouter(prefix="/token", tags=["Токены"])
router_users = APIRouter(prefix="/users", tags=["Пользователь"])
router_companies = APIRouter(prefix="/companies", tags=["Компания"])
router_template_matrix = APIRouter(
    prefix="/matrix_template",
    tags=["Шаблон матрицы"]
)
router_matrix = APIRouter(prefix="/matrix", tags=["Матрица"])


tags_metadata = [
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
    }
]
