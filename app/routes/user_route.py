from fastapi import APIRouter, status, Depends
from database.database import get_session
from models import User
from services.user_service import UserService
from typing import Dict
import logging

logger = logging.getLogger(__name__)

user_route = APIRouter()


# TODO: возможно выдавать токены сразу
@user_route.post(
    '/sign-up',
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="User registration",
    description="Register a new user with email and password")
async def sign_up(email: str, username: str, password: str, session=Depends(get_session)) -> Dict[str, str]:
    user_service = UserService(session)
    user_service.sign_up(email=email, username=username, password=password)

    return {
        "message": "User successfully registered"
    }


# TODO: мб понадобится мб нет, доставать id из access_token текущей сессии
@user_route.get(
    "/current",
    response_model=User,
    summary="Get current user info",
    response_description="Current user info"
)
async def get_current_user(session=Depends(get_session)) -> User:
    user_service = UserService(session)

    return user_service.get_user_by_id('id from token')
