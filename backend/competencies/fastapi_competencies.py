from fastapi import FastAPI
from api.routers.matrix import router_matrix, router_skills

fastapi_competencies = FastAPI()
fastapi_competencies.include_router(router_matrix)
fastapi_competencies.include_router(router_skills)


@fastapi_competencies.get("/")
def hello():
    return {"hello": "hi, i`m fastapi"}
