import os

from api.routers.matrix import router_grade, router_matrix, router_skills
from api.routers.users import router_auth, router_users
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

fastapi_competencies = FastAPI()
fastapi_competencies.include_router(router_matrix)
fastapi_competencies.include_router(router_skills)
fastapi_competencies.include_router(router_grade)
fastapi_competencies.include_router(router_auth)
fastapi_competencies.include_router(router_users)

@fastapi_competencies.get("/")
def hello():
    return {"hello": "Здарова, чекни доку /api/docs или /api/redoc"}
