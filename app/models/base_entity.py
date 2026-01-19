from abc import ABC
from datetime import datetime
from uuid import uuid4, UUID


class BaseEntity(ABC):
    def __init__(self):
        self._id = uuid4()
        self._created_at = datetime.now()

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at
