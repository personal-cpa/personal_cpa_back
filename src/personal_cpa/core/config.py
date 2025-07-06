# pyright: reportCallIssue=false,reportOptionalCall=false,reportAssignmentType=false
"""
This module provides configuration settings for the Personal CPA application.
"""

from functools import lru_cache
import os
from pathlib import Path
import urllib.parse

from dynaconf import Dynaconf
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CONFIG_PATH = os.getenv("SETTINGS_FILE", str(PROJECT_ROOT / "config.yml"))

config = Dynaconf(
    settings_files=[CONFIG_PATH], environments=True, env_switcher="PERSONAL_CPA_ENV", default_env="local", env="local"
)


class AppSettings(BaseSettings):
    """
    This class defines the application settings for the Personal CPA application.

    It provides the following:
    - Application name
    - Application version
    - Environment
    """

    APP_NAME: str = "Personal CPA"
    APP_VERSION: str = "25.3.1"
    ENVIRONMENT: str = config.current_env

    LOG_LEVEL: str = config.get("LOG_LEVEL")
    LOG_FILE: str = str(PROJECT_ROOT / config.get("LOG_FILE"))
    DB_TYPE: str = config.get("DB_TYPE")
    DB_HOST: str = config.get("DB_HOST")
    DB_PORT: int = config.get("DB_PORT")
    DB_DATABASE: str = config.get("DB_DATABASE")
    DB_USERNAME: str = config.get("DB_USERNAME")
    DB_PASSWORD: str = config.get("DB_PASSWORD")
    DB_ROOT_PASSWORD: str = config.get("DB_ROOT_PASSWORD")
    DB_POOL_CONNECTION_LIMIT: int = config.get("DB_POOL_CONNECTION_LIMIT")
    DB_POOL_MAX_IDLE: int = config.get("DB_POOL_MAX_IDLE")
    DB_POOL_IDLE_TIMEOUT: int = config.get("DB_POOL_IDLE_TIMEOUT")

    @property
    def database_url(self) -> str:
        """
        Returns:
            str: database url
        """
        password = urllib.parse.quote(self.DB_PASSWORD)
        return (
            f"{self.DB_TYPE}+pymysql://{self.DB_USERNAME}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"
        )


@lru_cache
def get_settings() -> AppSettings:
    """
    Returns the application settings.

    Returns:
        AppSettings: The application settings instance.
    """
    return AppSettings()
