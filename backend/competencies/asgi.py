# uvicorn competencies.asgi:application --reload
import os
import django
from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'competencies.settings')
django.setup()

from .fastapi_competencies import fastapi_competencies
django_application = get_wsgi_application()

application = FastAPI()

application.mount(
    "/static",
    StaticFiles(directory="collected_static"),
    name="static"
)

application.mount("/api", fastapi_competencies)
application.mount("/", WSGIMiddleware(django_application))
