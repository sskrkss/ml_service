from fastapi import APIRouter

from routes.health_check_route import health_check_route
from routes.auth_route import auth_route
from routes.user_route import user_route
from routes.admin.user_route import admin_user_route
from routes.transaction_route import transaction_route
from routes.ml_task_route import ml_task_route


def get_app_router() -> APIRouter:
    router = APIRouter()

    router.include_router(health_check_route, tags=['Health check'])
    router.include_router(auth_route, prefix='/api', tags=['Auth'])
    router.include_router(user_route, prefix='/api/users', tags=['User'])
    router.include_router(admin_user_route, prefix='/api/admin/users', tags=['Admin'])
    router.include_router(transaction_route, prefix='/api/transactions', tags=['Transaction'])
    router.include_router(ml_task_route, prefix='/api/ml-tasks', tags=['Ml task'])

    return router
