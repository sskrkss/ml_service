from fastapi import APIRouter, status, Depends
from database.database import get_session
from models import User
from services.user_service import UserService
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

user_route = APIRouter()


@user_route.post(
    '/sign-up',
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="User registration",
    description="Register a new user with email and password")
async def sign_up(email: str, username: str, password: str, session=Depends(get_session)) -> Dict[str, str]:
    """
    Create new user account.

    Args:
        email: Email address
        username: Username
        password: Password
        session: Database session

    Returns:
        dict: Success message

    Raises:
        HTTPException: If user already exists
    """
    user_service = UserService(session)
    user_service.sign_up(email=email, username=username, password=password)

    return {
        "message": "User successfully registered"
    }


@user_route.get(
    "/",
    response_model=List[User],
    summary="Get all users",
    response_description="List of all users"
)
async def get_all_users(session=Depends(get_session)) -> List[User]:
    """
    Get list of all users.

    Args:
        session: Database session

    Returns:
        List[UserResponse]: List of users
    """

    user_service = UserService(session)

    return user_service.get_users()
