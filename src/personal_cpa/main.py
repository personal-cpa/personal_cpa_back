"""
This module defines the FastAPI application.
"""

import logging
import time

from fastapi import FastAPI, Request
from starlette.middleware.base import RequestResponseEndpoint

from core.logger import setup_logging
from personal_cpa.adapter.inbound.api import error_handler
from personal_cpa.adapter.inbound.api.routes import chart_of_account, health
from personal_cpa.config import get_settings
from personal_cpa.container import Container
from personal_cpa.exceptions import PersonalCPAError

settings = get_settings()
setup_logging(settings)

logger = logging.getLogger(settings.APP_NAME)

container = Container()
container.wire(packages=[".adapter"])


async def logging_middleware(request: Request, call_next: RequestResponseEndpoint):
    """
    Log the request and response.

    Args:
        request: The request object.
        call_next: The next middleware or endpoint to call.

    Returns:
        The response object.

    Raises:
        PersonalCPAError: 사용자 정의 예외 발생 시 발생
    """
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Response status code: {response.status_code}, Process time: {process_time}")
    except PersonalCPAError:
        process_time = time.time() - start_time
        logger.exception(f"Request Failed: {request.method} {request.url} Process time: {process_time}")
        raise
    else:
        return response


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.container = container  # pyright: ignore reportAttributeAccessIssue

app.middleware("http")(logging_middleware)
error_handler.add_error_handlers(app)

app.include_router(health.router, prefix="/api/v1")
app.include_router(chart_of_account.router, prefix="/api/v1")
