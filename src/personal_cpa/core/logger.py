"""
This module configures the logger for the application using dictConfig.
"""

import logging.config
from pathlib import Path
import sys

from personal_cpa.core.config import AppSettings


def setup_logging(settings: AppSettings) -> None:
    """
    Set up logging configuration for the application.

    Args:
        settings: The application settings.
    """
    log_dir = Path(settings.LOG_FILE).parent
    if not Path.exists(log_dir):
        Path.mkdir(log_dir)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}},
        "handlers": {
            "console": {"class": "logging.StreamHandler", "stream": sys.stdout, "formatter": "default"},
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": settings.LOG_FILE,
                "maxBytes": 1024 * 1024 * 5,  # 5 MB
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "loggers": {
            settings.APP_NAME: {"handlers": ["console", "file"], "level": settings.LOG_LEVEL, "propagate": False}
        },
        "root": {"handlers": ["console", "file"], "level": settings.LOG_LEVEL},
    }
    logging.config.dictConfig(logging_config)
