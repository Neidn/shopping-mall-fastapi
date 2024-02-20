# pylint: disable=no-self-argument
"""
configuration
"""
import os
from functools import lru_cache
from typing import List, Union, Optional

from pydantic import HttpUrl, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource


class SQLAlchemySettings(BaseSettings):
    database: str = Field(alias="DATABASE")

    sqlalchemy_pool_size: int = Field(alias="POOL_SIZE")
    sqlalchemy_pool_timeout: int = Field(alias="POOL_TIMEOUT")
    sqlalchemy_pool_recycle: int = Field(alias="POOL_RECYCLE")
    sqlalchemy_echo: bool = Field(alias="ECHO")
    sqlalchemy_database_url: str = Field(alias="DATABASE_URL")

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=os.path.join(os.getcwd(), "..", ".env"),
    )


class Settings(BaseSettings):
    """
    application settings
    """

    api_version_prefix: str = Field(alias="API_VERSION_PREFIX")
    jwt_algorithm: str = Field(alias="JWT_ALGORITHM")

    access_token_expire_seconds: int = Field(alias="ACCESS_TOKEN_EXPIRE_SECONDS")
    user_repository_path: str = Field(alias="USER_REPOSITORY_PATH")

    private_key: str = Field(alias="PRIVATE_KEY")
    public_key: str = Field(alias="PUBLIC_KEY")
    cors_allows: List[HttpUrl] = []

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.getcwd(), "..", ".env"),
        extra="ignore",
    )

    @field_validator("cors_allows")
    def __set_cors_allows(cls, v: Union[str, List[str]]) -> List[str]:  # noqa
        if isinstance(v, str) and not v.startswith("["):
            result = [i.strip() for i in v.split(",")]
        elif isinstance(v, List):
            result = v
        else:
            raise ValueError(v)
        return result

    @field_validator("private_key")
    def __set_private_key(cls, path: str) -> str:  # noqa
        private_key = open(path).read()
        return private_key

    @field_validator("public_key")
    def __set_public_key(cls, path: str) -> str:  # noqa
        public_key = open(path).read()
        return public_key


class LoadSettings:
    """
    load settings
    """

    def __init__(self):
        self.settings = Settings()
        self.sqlalchemy_settings = SQLAlchemySettings()

    @lru_cache()
    def get_settings(self):
        return self.settings, self.sqlalchemy_settings


load_settings = LoadSettings()

settings, sqlalchemy_settings = load_settings.get_settings()
