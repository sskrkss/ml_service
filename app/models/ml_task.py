import json
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship

from models.base_entity import BaseEntity
from models.enums import TaskStatus

if TYPE_CHECKING:
    from models.user import User


class MlTask(BaseEntity, table=True):
    input_text: str = Field(
        min_length=10,
        max_length=2000,
        nullable=False
    )
    prediction_json: Optional[str] = Field(
        default=None,
        sa_column=Column("prediction", JSON, nullable=True)
    )
    worker_id: Optional[str] = Field(
        default=None,
        nullable=True
    )
    task_status: TaskStatus = Field(
        default=TaskStatus.PROCESSING,
        nullable=False
    )
    finished_at: Optional[datetime] = Field(
        default=None,
        nullable=True
    )
    user_id: UUID = Field(
        foreign_key="user.id",
        nullable=False
    )
    user: "User" = Relationship(back_populates="ml_tasks")

    @property
    def prediction(self) -> Optional[List[str]]:
        if self.prediction_json:
            return json.loads(self.prediction_json)
        return None

    @prediction.setter
    def prediction(self, value: Optional[List[str]]):
        if value:
            self.prediction_json = json.dumps(value)
        else:
            self.prediction_json = None
