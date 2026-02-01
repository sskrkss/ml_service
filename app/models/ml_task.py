from datetime import datetime
from typing import Dict, Any, Optional, TYPE_CHECKING
from uuid import UUID
from sqlalchemy import Column, JSON
from sqlalchemy.ext.mutable import MutableDict
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
    prediction: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(
            MutableDict.as_mutable(JSON),
            nullable=True
        )
    )
    task_status: TaskStatus = Field(
        default=TaskStatus.PENDING,
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
