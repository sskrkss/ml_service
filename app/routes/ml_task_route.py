from typing import List

from fastapi import APIRouter, Depends, status

from auth.authenticator import auth_user
from auth.s2s_authenticator import auth_ml_worker
from database.database import get_session
from dto.request.run_ml_task_request_dto import RunMlTaskRequestDto
from dto.request.save_ml_task_prediction_request_dto import SaveMlTaskPredictionDto
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


@ml_task_route.post(
    "/save-prediction",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=MlTaskResponseDto,
    summary="Save ml task prediction (only for s2s integration)",
    status_code=status.HTTP_200_OK
)
async def save_ml_task_prediction(
    request_dto: SaveMlTaskPredictionDto,
    s2s=Depends(auth_ml_worker),
    session=Depends(get_session)
) -> MlTaskResponseDto:
    ml_task_service = MlTaskService(session)
    ml_task = ml_task_service.save_ml_task_prediction(
        task_id=request_dto.task_id,
        task_status=request_dto.task_status,
        prediction=request_dto.prediction,
        worker_id=request_dto.worker_id
    )

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
