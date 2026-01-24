from datetime import datetime

from .base_entity import BaseEntity
from enums import TaskStatus


# TODO: с форматом dataset и prediction нужно будет еще подумать, но скорее всего json
class MlTask(BaseEntity):
    def __init__(self, dataset: str):
        super().__init__()

        self._dataset = dataset
        self._prediction: str | None = None
        self._task_status: TaskStatus = TaskStatus.PENDING
        self._finished_at: datetime | None = None

    @property
    def dataset(self) -> str:
        return self._dataset

    # TODO: если предполагается кэширование, то можно prediction выделить в отдельную сущность
    #  и сохранять в бд вместе с dataset, чтобы переиспользовать результат
    @property
    def prediction(self) -> str | None:
        return self._prediction

    @property
    def task_status(self) -> TaskStatus:
        return self._task_status

    @property
    def finished_at(self) -> datetime:
        return self._created_at
