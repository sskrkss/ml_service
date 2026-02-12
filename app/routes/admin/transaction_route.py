from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from auth.authenticator import auth_admin
from database.database import get_session
from dto.request.admin.transaction_request_dto import TransactionRequestDto
from dto.response.transaction_response_dto import TransactionResponseDto
from models import User
from models.enums import TransactionType
from services.transaction_service import TransactionService
from services.user_service import UserService

admin_transaction_route = APIRouter()


@admin_transaction_route.put(
    "/deposit",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=TransactionResponseDto,
    summary="Deposit money to user balance by admin",
    status_code=status.HTTP_200_OK
)
async def deposit(
    request_dto: TransactionRequestDto,
    admin: User = Depends(auth_admin),
    session=Depends(get_session)
) -> TransactionResponseDto:
    user_service = UserService(session)
    target_user = user_service.get_user_by_id(request_dto.target_user_id)

    transaction_service = TransactionService(session)
    transaction = transaction_service.make_transaction(
        target_user,
        request_dto.amount,
        TransactionType.DEPOSIT
    )

    return TransactionResponseDto.model_validate(transaction)


@admin_transaction_route.get(
    "/",
    openapi_extra={
        "security": [{"BearerAuth": []}],
    },
    response_model=List[TransactionResponseDto],
    summary="Get transactions of user by admin",
    status_code=status.HTTP_200_OK
)
async def get_transactions(
    target_user_id: UUID,
    admin: User = Depends(auth_admin),
    session=Depends(get_session)
) -> List[TransactionResponseDto]:
    user_service = UserService(session)
    target_user = user_service.get_user_by_id(target_user_id)

    transaction_service = TransactionService(session)

    return [
        TransactionResponseDto.model_validate(transaction)
        for transaction in transaction_service.get_transactions_by_user(target_user)
    ]
