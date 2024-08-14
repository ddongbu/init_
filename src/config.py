import os
from typing import Any

from dotenv import load_dotenv
from pydantic import MySQLDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        # env_file=("../.env", '../.env.prod'),
        env_file_encoding="utf-8",
    )
    FLIP_DB: MySQLDsn
    RESUME_DB: MySQLDsn
    RECRUIT_DB: MySQLDsn
    MONGO_DB: str
    SYSTEM_DB: str

    REDIS_URL_T: RedisDsn
    REDIS_URL_C: RedisDsn
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    # cors
    # CORS_ORIGINS: list[str]
    # CORS_ORIGIN_REGEX: str | None = None
    # CORS_HEADERS: list[str]

    # jwt
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 60 * 60 * 24 * 7

    # token
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # googleAPI
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    APP_VERSION: str = "1"


class TestConfig(Config):
    ...


class LocalConfig(Config):
    FLIP_DB: MySQLDsn
    RESUME_DB: MySQLDsn
    RECRUIT_DB: MySQLDsn
    SYSTEM_DB: str
    MONGO_DB: str

    @field_validator("FLIP_DB", "RESUME_DB", "RECRUIT_DB", "SYSTEM_DB", "MONGO_DB")
    def test(v, f):
        return os.getenv(f"{f.field_name}_DEV", v)


class ProductionConfig(Config):
    ...


def get_config():
    env = os.getenv("API_ENV", 'local')
    config = {
        "test": TestConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config[env]


settings: Config = get_config()

app_configs: dict[str, Any] = {
    "title": "FastAPI TITLE",
    "version": settings.APP_VERSION,
    "root_path": "/api",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "openapi_url": "/openapi",
}
