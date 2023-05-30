import logging
import os
from copy import deepcopy
from functools import lru_cache
from typing import Union, Any, Optional

from pydantic import BaseSettings, validator
from pydantic.networks import PostgresDsn
from uvicorn.config import LOGGING_CONFIG as UVICORN_LOGGING_CONFIG


class Settings(BaseSettings):
    HOST: str = '127.0.0.1'
    PORT: int = 5000
    WORKERS: int = 1
    LOG_LEVEL: Union[int, str] = logging.INFO
    LOGGING_CONFIG: dict[str, Any] = UVICORN_LOGGING_CONFIG
    DEBUG: bool = False
    AUTH: str = ''
    DATABASE_HOST: str = 'postgres_db'
    DATABASE_PORT: str = '5433'
    DATABASE_USER: str = 'postgres'
    DATABASE_PASSWORD: str = 'postgres'
    DATABASE_NAME: str = 'events_service'
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True, allow_reuse=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("DATABASE_HOST"),
            port=values.get("DATABASE_PORT"),
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            path=f"/{values.get('DATABASE_NAME', '')}",
        )

    class Config:
        env_file = "../.env"


@lru_cache()
def get_config():
    return Settings()


current_config = get_config()

for k, v in list(current_config):
    globals()[k] = v

    if k in ['SQLALCHEMY_DATABASE_URI']:
        os.environ[k] = str(v)
