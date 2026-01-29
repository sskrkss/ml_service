from typing import List

from fastapi import APIRouter, Depends, status

from database.database import get_session
from models import User
from services.user_service import UserService

admin_user_route = APIRouter()


# TODO: понадобится, чтобы выдавать админские права, ну и плюс для отладки, добавить isGranted
@admin_user_route.get(
    "/",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    response_description="List of all users info"
)
async def get_all_users(session=Depends(get_session)) -> List[User]:
    user_service = UserService(session)

    return user_service.get_users()


# TODO: добавить isGranted
@admin_user_route.put(
    "/",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Add admin role to user",
    response_description="New admin user info"
)
async def add_admin_role(id: str, session=Depends(get_session)) -> User:
    user_service = UserService(session)
    user = user_service.get_user_by_id(id)

    return user_service.add_admin_role(user)
