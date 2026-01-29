from typing import Dict

from fastapi import APIRouter, status

health_check_route = APIRouter()


@health_check_route.get(
    "/health-check",
    status_code=status.HTTP_200_OK,
    summary="App's health check"
)
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
