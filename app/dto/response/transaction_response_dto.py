from datetime import datetime

from pydantic import BaseModel, ConfigDict

from models.enums import TransactionType


class TransactionResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    amount: float
    transaction_type: TransactionType
