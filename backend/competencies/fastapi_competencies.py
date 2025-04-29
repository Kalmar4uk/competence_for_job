from api.routers import companies, matrix, template_matrix, tokens, users, skills, grade
from api.routers.routers import (router_companies, router_matrix,
                                 router_template_matrix, router_token,
                                 router_users, tags_metadata, router_skills, router_grades)
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

description = """
## The best project for finding employees based on their competencies
Самый лучший проект для поиска сотрудников по их компетенциям
"""

fastapi_competencies = FastAPI(
    openapi_tags=tags_metadata,
    title="CompetenceAPI",
    description=description,
    version="1.0.хуй пойми уже какая"
)
fastapi_competencies.include_router(router_token)
fastapi_competencies.include_router(router_users)
fastapi_competencies.include_router(router_companies)
fastapi_competencies.include_router(router_template_matrix)
fastapi_competencies.include_router(router_matrix)
fastapi_competencies.include_router(router_skills)
fastapi_competencies.include_router(router_grades)


@fastapi_competencies.get("/")
def hello():
    return {"hello": "Здарова, чекни доку /api/docs или /api/redoc"}
