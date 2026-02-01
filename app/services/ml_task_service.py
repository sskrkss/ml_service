from sqlmodel import Session, Sequence

from database.config import get_settings
from models.enums import TransactionType
from models.ml_task import MlTask
from models.user import User
from repositories.ml_task_repository import MlTaskRepository
from repositories.user_repository import UserRepository
from services.transaction_service import TransactionService

settings = get_settings()
RUN_TASK_PRICE = settings.RUN_TASK_PRICE


class MlTaskService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)
        self.ml_task_repository = MlTaskRepository(session)
        self.transaction_service = TransactionService(session)

    def run_ml_task(self, user: User, input_text: str) -> MlTask:
        ml_task = MlTask(
            input_text=input_text
        )

        self.transaction_service.make_transaction(user, RUN_TASK_PRICE, TransactionType.WITHDRAW)

        user.add_ml_task(ml_task)
        self.user_repository.save(user)

        # TODO: Урок 5. Где-то тут отправляем сообщение брокеру на запуск модели и подготовки датасета (если нужно)

        return ml_task

    def get_ml_tasks_by_user(self, user: User) -> Sequence[MlTask]:
        return self.ml_task_repository.get_by_user(user)
