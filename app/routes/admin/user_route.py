from fastapi import APIRouter, Depends
from database.database import get_session
from models import User
from services.user_service import UserService
from typing import List
import logging

logger = logging.getLogger(__name__)

admin_user_route = APIRouter()


# TODO: понадобится, чтобы выдавать админские права, ну и плюс для отладки, добавить isGranted
@admin_user_route.get(
    "/",
    response_model=List[User],
    summary="Get all users",
    response_description="List of all users"
)
async def get_all_users(session=Depends(get_session)) -> List[User]:
    user_service = UserService(session)

    return user_service.get_users()


# TODO: добавить isGranted
@admin_user_route.put(
    "/",
    response_model=User,
    summary="Add admin role to user",
    response_description="Granted user"
)
async def add_admin_role_to_user(id: str, session=Depends(get_session)) -> User:
    user_service = UserService(session)
    user = user_service.get_user_by_id(id)

    return user_service.add_admin_role(user)
