from datetime import datetime

from sqlmodel import Session, Sequence

from database.config import get_settings
from models.enums import TaskStatus, TransactionType
from models.ml_task import MlTask
from models.user import User
from repositories.ml_task_repository import MlTaskRepository
from repositories.user_repository import UserRepository
from services.rmq.ml_task_publisher import send_task
from services.transaction_service import TransactionService

settings = get_settings()
RUN_TASK_PRICE = settings.RUN_TASK_PRICE


class MlTaskService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)
        self.ml_task_repository = MlTaskRepository(session)
        self.transaction_service = TransactionService(session)

    def run_ml_task(self, user: User, input_text: str) -> MlTask:
        self.transaction_service.check_balance_before_withdraw(user, RUN_TASK_PRICE)

        ml_task = MlTask(
            input_text=input_text
        )

        user.add_ml_task(ml_task)
        self.user_repository.save(user)

        send_task(ml_task.id_string, ml_task.input_text)

        return ml_task

    def save_ml_task_prediction(
        self,
        task_id: str,
        task_status: TaskStatus,
        prediction: list[dict],
        worker_id: str
    ) -> MlTask:
        ml_task = self.ml_task_repository.get_by_id(task_id)

        if task_status == TaskStatus.COMPLETED:
            ml_task.prediction = prediction
            ml_task.task_status = TaskStatus.COMPLETED

            self.transaction_service.make_transaction(
                user=ml_task.user,
                amount=RUN_TASK_PRICE,
                transaction_type=TransactionType.WITHDRAW
            )
        elif task_status == TaskStatus.FAILED:
            ml_task.task_status = TaskStatus.FAILED

        ml_task.finished_at = datetime.now()
        ml_task.worker_id = worker_id

        self.ml_task_repository.save(ml_task)

        return ml_task

    def get_ml_tasks_by_user(self, user: User) -> Sequence[MlTask]:
        return self.ml_task_repository.get_by_user(user)
