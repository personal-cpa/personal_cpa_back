"""
This module defines the FastAPI application.
"""

import logging

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from personal_cpa.adapter.inbound.api import error_handler
from personal_cpa.adapter.inbound.api.routes import health
from personal_cpa.core.config import get_settings
from personal_cpa.core.logger import setup_logging

settings = get_settings()
setup_logging(settings)

logger = logging.getLogger(settings.APP_NAME)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log requests and responses.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        """
        Log the request and response.

        Args:
            request: The request object.
            call_next: The next middleware or endpoint to call.

        Returns:
            The response object.
        """
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response status code: {response.status_code}")
        return response


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(LoggingMiddleware)
error_handler.add_error_handlers(app)

app.include_router(health.router, prefix="/api/v1")
