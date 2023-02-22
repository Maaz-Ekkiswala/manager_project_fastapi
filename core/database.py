from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from core.config import settings

DB_URL = f"postgres://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
print(DB_URL)


def init(app: FastAPI):
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": [
                 "apps.users.models", "aerich.models"
            ]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


TORTOISE_ORM = {
    "connections": {
        "default": f'{DB_URL}',
    },
    "apps": {
        "user": {
            "models": [
                 "apps.users.models", "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}