from fastapi import APIRouter


router_token = APIRouter(prefix="/token", tags=["Токены"])
router_users = APIRouter(prefix="/users", tags=["Пользователь"])
router_companies = APIRouter(prefix="/companies", tags=["Компания"])
router_matrix = APIRouter(prefix="/matrix", tags=["Матрица"])
router_skills = APIRouter(prefix="/skills", tags=["Навык"])
router_grade = APIRouter(prefix="/grade", tags=["Оценка"])
