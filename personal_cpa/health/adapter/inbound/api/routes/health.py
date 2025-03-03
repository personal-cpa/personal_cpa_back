"""
This module defines the health check endpoint for the Personal CPA application.
"""

from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: A dictionary containing the status of the service.

    Raises:
        HTTPException: If the service is unhealthy.
    """
    try:
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "unhealthy", "error": str(e), "message": "Service is unavailable"},
        ) from e
