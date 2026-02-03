from datetime import datetime
from typing import Dict, Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from models.enums import TaskStatus


class MlTaskResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    task_status: TaskStatus
    created_at: datetime
    finished_at: Optional[datetime] = None
    prediction: Optional[Dict[str, Any]] = None
