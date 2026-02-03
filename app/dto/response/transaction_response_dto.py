from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from models.enums import TransactionType


class TransactionResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    amount: float
    transaction_type: TransactionType
