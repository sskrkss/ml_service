from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BalanceResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amount: float
    currency: str
