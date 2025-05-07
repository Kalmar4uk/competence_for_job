from fastapi import FastAPI
from database.settings import init_tortoise


app = FastAPI()
init_tortoise(app)
