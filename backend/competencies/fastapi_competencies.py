from api.routers.companies import *
from api.routers.matrix import *
from api.routers.users import *
from api.routers.routers import router_companies, router_grade, router_token, router_matrix, router_skills, router_users
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

fastapi_competencies = FastAPI()
fastapi_competencies.include_router(router_token)
fastapi_competencies.include_router(router_users)
fastapi_competencies.include_router(router_companies)
fastapi_competencies.include_router(router_matrix)
fastapi_competencies.include_router(router_skills)
fastapi_competencies.include_router(router_grade)


@fastapi_competencies.get("/")
def hello():
    return {"hello": "Здарова, чекни доку /api/docs или /api/redoc"}
