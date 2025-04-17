import os

import django
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'competencies.settings')
django.setup()

from .fastapi_competencies import fastapi_competencies


origins = [
    "http://localhost",
    "http://localhost:8000",
]

django_application = get_asgi_application()

application = FastAPI()

application.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
 )

application.mount(
    "/static",
    StaticFiles(directory="collected_static"),
    name="static"
)

application.mount("/api", fastapi_competencies)
application.mount("/", django_application)
