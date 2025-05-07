from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


TORTOISE_ORM = {
    "connections": {"default": "sqlite://new_db.sqlite3"},
    "apps": {
        "models": {
            "models": [
                "database.users.models",
                "database.companies.models",
                "database.matrix.models",
                "database.tokens.models",
                "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}


def init_tortoise(app: FastAPI):
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True
    )
