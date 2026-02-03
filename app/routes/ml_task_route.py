from typing import List

from fastapi import APIRouter, Depends, status

from auth.authenticator import auth_user
from database.database import get_session
from dto.request.run_ml_task_request_dto import RunMlTaskRequestDto
from dto.response.ml_task_response_dto import MlTaskResponseDto
from models import User
from services.ml_task_service import MlTaskService

ml_task_route = APIRouter()


@ml_task_route.post(
    "/run",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=MlTaskResponseDto,
    summary="Run ml task",
    status_code=status.HTTP_200_OK
)
async def run_ml_task(
    request_dto: RunMlTaskRequestDto,
    user: User = Depends(auth_user),
    session=Depends(get_session)
) -> MlTaskResponseDto:
    ml_task_service = MlTaskService(session)
    ml_task = ml_task_service.run_ml_task(user, request_dto.input_text)

    return MlTaskResponseDto.model_validate(ml_task)


@ml_task_route.get(
    "/",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=List[MlTaskResponseDto],
    summary="Get ml tasks of current user",
    status_code=status.HTTP_200_OK
)
async def get_ml_tasks(
    user: User = Depends(auth_user),
    session=Depends(get_session)
) -> List[MlTaskResponseDto]:
    ml_task_service = MlTaskService(session)

    return [
        MlTaskResponseDto.model_validate(ml_task)
        for ml_task in ml_task_service.get_ml_tasks_by_user(user)
    ]
