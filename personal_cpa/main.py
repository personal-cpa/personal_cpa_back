"""
This module defines the FastAPI application.
"""

from fastapi import FastAPI

from personal_cpa.core.config import get_settings
from personal_cpa.health.adapter.inbound.api.routes import health

settings = get_settings()
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(health.router, prefix="/api/v1")
