from uuid import UUID

from pydantic import BaseModel


class AdminRequestDto(BaseModel):
    target_user_id: UUID
