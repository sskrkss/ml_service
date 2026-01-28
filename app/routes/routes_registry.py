from fastapi import APIRouter

from routes.health_check import health_check_route
from routes.user import user_route


def get_app_router() -> APIRouter:
    router = APIRouter()

    router.include_router(health_check_route, tags=['Health check'])
    router.include_router(user_route, prefix='/api/users', tags=['Users'])

    return router
