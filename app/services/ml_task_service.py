import pandas as pd

from app.models.ml_task import MlTask
from app.models.user import User


# TODO: Добавить запись в бд, сделать красивые импорты (__init__.py)
class MlService:
    def prepare_dataset(self, dataset: str) -> pd.Dataset:
        pass

    # TODO: Как будто планируется асинхронка,
    #  пока все очень примерно, потом понадобится доп логика для обработки сообщений брокера разного статуса
    def run_task(self, user: User, dataset: str) -> MlTask:
        ml_task = MlTask(dataset)

        user.add_ml_task(ml_task)

        # TODO: где-то тут отправляем сообщение брокеру на запуск модели

        return ml_task
