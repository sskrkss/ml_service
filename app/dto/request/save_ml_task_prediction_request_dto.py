from typing import Optional

from pydantic import BaseModel

from models.enums import TaskStatus


class SaveMlTaskPredictionDto(BaseModel):
    task_id: str
    task_status: TaskStatus
    prediction: Optional[list]
    worker_id: str
