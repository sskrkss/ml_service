from pydantic import BaseModel, ConfigDict


class BalanceResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    amount: float
    currency: str
