from typing import Dict
from fastapi import APIRouter

health_check_route = APIRouter()


@health_check_route.get("/health-check")
async def health_check() -> Dict[str, str]:
    """
    Эндпоинт проверки работоспособности для мониторинга.

    Returns:
        Dict[str, str]: Сообщение о статусе
    """
    return {"status": "healthy"}
