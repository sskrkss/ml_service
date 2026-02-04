from pydantic import BaseModel


class SaveMlTaskPredictionDto(BaseModel):
    task_id: str
    prediction: list
