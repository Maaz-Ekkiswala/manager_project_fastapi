from datetime import timedelta

from pydantic import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "Manager Project"
    DEBUG: bool = True

    DB_USER: str
    DB_HOST: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int

    # Static path
    STATIC_PATH: str
    MEDIA_PATH: str

    AUTHJWT_SECRET_KEY: str

    # AuthJWT
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    access_expires = timedelta(minutes=15)
    refresh_expires = timedelta(days=30)

    # Redis
    REDIS_SERVER: str
    REDIS_PORT: int

    class Config:
        case_sensitive = True
        env_file = "./.env"


settings = Settings()
