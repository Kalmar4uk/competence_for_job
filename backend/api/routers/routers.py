from fastapi import APIRouter

router_token = APIRouter(prefix="/token", tags=["Токены"])
router_users = APIRouter(prefix="/users", tags=["Пользователь"])
router_companies = APIRouter(prefix="/companies", tags=["Компания"])
