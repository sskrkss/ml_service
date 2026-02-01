from pydantic import field_validator

from dto.request.admin.admin_request_dto import AdminRequestDto


class TransactionRequestDto(AdminRequestDto):
    amount: float

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, value: float) -> float:
        if value <= 0:
            raise ValueError('Amount must be greater than 0')
        return round(value, 2)
