from fastapi import APIRouter

router_token = APIRouter(prefix="/token", tags=["Токены"])
router_users = APIRouter(prefix="/users", tags=["Пользователь"])
router_companies = APIRouter(prefix="/companies", tags=["Компания"])
router_template_matrix = APIRouter(
    prefix="/matrix_template",
    tags=["Шаблон матрицы"]
)
router_matrix = APIRouter(prefix="/matrix", tags=["Матрица"])
