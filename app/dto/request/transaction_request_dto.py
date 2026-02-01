from pydantic import BaseModel, field_validator


class TransactionRequestDto(BaseModel):
    amount: float

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value: float) -> float:
        if value <= 0:
            raise ValueError('Amount must be greater than 0')
        return round(value, 2)
