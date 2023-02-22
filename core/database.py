from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from core.config import settings

DB_URL = f"postgres://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
print(DB_URL)


def init(app: FastAPI):
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": [
            "apps.users.models",
            "aerich.models",
            "apps.master.models",
            "apps.projects.models",
            "apps.issues.models",
            "apps.comments.models",
        ]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
    Tortoise.init_models([
        "apps.users.models",
        "apps.master.models",
        "apps.projects.models",
        "apps.issues.models",
        "apps.comments.models",
    ], "models")


TORTOISE_ORM = {
    "connections": {
        "default": f'{DB_URL}',
    },
    "apps": {
        "models": {
            "models": [
                "apps.users.models",
                "apps.master.models",
                "apps.projects.models",
                "apps.issues.models",
                "apps.comments.models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}