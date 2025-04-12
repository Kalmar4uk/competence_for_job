from api.routers import companies, tokens, users
from api.routers.routers import router_companies, router_token, router_users
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

fastapi_competencies = FastAPI()
fastapi_competencies.include_router(router_token)
fastapi_competencies.include_router(router_users)
fastapi_competencies.include_router(router_companies)


@fastapi_competencies.get("/")
def hello():
    return {"hello": "Здарова, чекни доку /api/docs или /api/redoc"}
