from typing import List

from fastapi import APIRouter, Depends, status

from auth.authenticator import auth_user
from database.database import get_session
from dto.request.transaction_request_dto import TransactionRequestDto
from dto.response.transaction_response_dto import TransactionResponseDto
from models import User
from models.enums import TransactionType
from services.transaction_service import TransactionService

transaction_route = APIRouter()


@transaction_route.put(
    "/deposit",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=TransactionResponseDto,
    summary="Deposit money to user balance",
    status_code=status.HTTP_200_OK
)
async def deposit(
    request_dto: TransactionRequestDto,
    user: User = Depends(auth_user),
    session=Depends(get_session)
) -> TransactionResponseDto:
    transaction_service = TransactionService(session)
    transaction = transaction_service.make_transaction(
        user=user,
        amount=request_dto.amount,
        transaction_type=TransactionType.DEPOSIT
    )

    return TransactionResponseDto.model_validate(transaction)


@transaction_route.get(
    "/",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=List[TransactionResponseDto],
    summary="Get transactions of current user",
    status_code=status.HTTP_200_OK
)
async def get_transactions(
    user: User = Depends(auth_user),
    session=Depends(get_session)
) -> List[TransactionResponseDto]:
    transaction_service = TransactionService(session)

    return [
        TransactionResponseDto.model_validate(transaction)
        for transaction in transaction_service.get_transactions_by_user(user)
    ]
