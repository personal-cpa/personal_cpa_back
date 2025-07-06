"""
This module defines the error handler for the FastAPI application.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def add_error_handlers(app: FastAPI) -> None:
    """
    This function adds error handlers to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        This function handles all exceptions that are not explicitly handled by other exception handlers.

        Args:
            request (Request): The request that caused the exception.
            exc (Exception): The exception that was raised.

        Returns:
            JSONResponse: A JSON response with a 500 status code and a generic error message.
        """
        logger.error(f"Unhandled exception: {exc} for request {request.method} {request.url}")
        return JSONResponse(status_code=500, content={"message": "Internal server error"})
