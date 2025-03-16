import os
from dotenv import load_dotenv
from fastapi import FastAPI
from api.routers.matrix import router_matrix, router_skills, router_grade
from api.routers.users import router_auth, router_users

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
