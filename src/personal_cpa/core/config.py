"""
This module provides configuration settings for the Personal CPA application.
"""

from functools import lru_cache
import os
from pathlib import Path

from dynaconf import Dynaconf
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).parent.parent
SETTINGS_FILE = os.getenv("SETTINGS_FILE", str(PROJECT_ROOT / "settings.yaml"))

settings = Dynaconf(
    settings_files=[SETTINGS_FILE], environments=True, env_switcher="PERSONAL_CPA_ENV", default_env="local"
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
    ENVIRONMENT: str = str(settings.ENVIRONMENT)


@lru_cache
def get_settings() -> AppSettings:
    """
    Returns the application settings.

    Returns:
        AppSettings: The application settings instance.
    """
    return AppSettings()
