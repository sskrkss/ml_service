from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from models.enums import TaskStatus


class MlTaskResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    input_text: str
    task_status: TaskStatus
    created_at: datetime
    finished_at: Optional[datetime] = None
    prediction: Optional[List[str]] = None
    worker_id: Optional[str] = None
