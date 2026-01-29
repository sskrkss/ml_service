from typing import Dict

from fastapi import APIRouter, Depends, status

from database.database import get_session
from services.user_service import UserService

user_route = APIRouter()


# TODO: сам id экстрактить из access_token
# TODO: выдавать dto
@user_route.get(
    "/current",
    status_code=status.HTTP_200_OK,
    summary="Get current user info",
    response_description="Current user info including balance"
)
async def get_current_user(id: str, session=Depends(get_session)) -> Dict:
    user_service = UserService(session)
    user = user_service.get_user_by_id(id)

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "roles": user.roles,
        "balance": user.balance.amount
    }
