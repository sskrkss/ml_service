from typing import Dict, List

from fastapi import APIRouter, Depends, status

from database.database import get_session
from models import MlTask
from repositories.user_repository import UserRepository
from services.ml_task_service import MlTaskService

ml_task_route = APIRouter()


@ml_task_route.post(
    "/run",
    response_model=MlTask,
    summary="Run ml task",
    status_code=status.HTTP_200_OK
)
async def run_ml_task(user_id: str, raw_dataset: Dict, session=Depends(get_session)) -> MlTask:
    # TODO: id пользователя экстрактим из access_token
    user_repository = UserRepository(session)
    user = user_repository.get_by_id(user_id)

    ml_task_service = MlTaskService(session)

    return ml_task_service.run_ml_task(user, raw_dataset)


@ml_task_route.get(
    "/",
    response_model=List[MlTask],
    summary="Get ml tasks of current user",
    status_code=status.HTTP_200_OK
)
async def get_ml_tasks(user_id: str, session=Depends(get_session)) -> List[MlTask]:
    # TODO: id пользователя экстрактим из access_token
    user_repository = UserRepository(session)
    user = user_repository.get_by_id(user_id)

    # TODO: скорее всего сортировка нужна будет
    return user.ml_tasks
