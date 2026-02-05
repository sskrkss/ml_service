from typing import List

from pydantic import BaseModel, ConfigDict

from dto.response.balance_response_dto import BalanceResponseDto


class UserResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    username: str
    roles: List[str]
    balance: BalanceResponseDto
