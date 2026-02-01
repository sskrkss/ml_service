from typing import List

from fastapi import APIRouter, Depends, status

from auth.authenticator import auth_admin
from database.database import get_session
from dto.request.admin_request_dto import AdminRequestDto
from dto.response.user_response_dto import UserResponseDto
from models import User
from services.user_service import UserService

admin_user_route = APIRouter()


@admin_user_route.get(
    "/",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=List[UserResponseDto],
    status_code=status.HTTP_200_OK,
    summary="Get all users info",
    response_description="List of all users info"
)
async def get_all_users(
    admin: User = Depends(auth_admin),
    session=Depends(get_session)
) -> List[UserResponseDto]:
    user_service = UserService(session)

    return [
        UserResponseDto.model_validate(user)
        for user in user_service.get_users()
    ]


@admin_user_route.put(
    "/add-admin-role",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=UserResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Add admin role to user",
    response_description="New admin user info"
)
async def add_admin_role(
    request_dto: AdminRequestDto,
    admin: User = Depends(auth_admin),
    session=Depends(get_session)
) -> UserResponseDto:
    user_service = UserService(session)
    target_user = user_service.get_user_by_id(str(request_dto.target_user_id))
    target_user = user_service.add_admin_role(target_user)

    return UserResponseDto.model_validate(target_user)


@admin_user_route.put(
    "/remove-admin-role",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=UserResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Remove admin role from user",
    response_description="User info"
)
async def remove_admin_role(
    request_dto: AdminRequestDto,
    admin: User = Depends(auth_admin),
    session=Depends(get_session)
) -> UserResponseDto:
    user_service = UserService(session)
    target_user = user_service.get_user_by_id(str(request_dto.target_user_id))
    target_user = user_service.remove_admin_role(target_user)

    return UserResponseDto.model_validate(target_user)
