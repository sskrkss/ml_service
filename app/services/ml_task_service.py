from sqlmodel import Session

from models.ml_task import MlTask
from models.user import User
from repositories.user_repository import UserRepository


# TODO: Добавить запись в бд, сделать красивые импорты (__init__.py)
class MlTaskService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    # TODO: Как будто планируется асинхронка,
    #  пока все очень примерно, потом понадобится доп логика для обработки сообщений брокера разного статуса
    def run_ml_task(self, user: User, raw_dataset: dict) -> MlTask:
        ml_task = MlTask(
            dataset=raw_dataset
        )

        user.add_ml_task(ml_task)
        self.user_repository.save(user)

        # TODO: где-то тут отправляем сообщение брокеру на запуск модели и подготовки датасета (если нужно)

        return ml_task
