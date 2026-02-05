from pydantic import BaseModel


class AdminRequestDto(BaseModel):
    target_user_id: str
