from typing import List

from fastapi import APIRouter, Depends, status

from database.database import get_session
from models import MlTask, UserTransaction
from models.enums import TransactionType
from repositories.user_repository import UserRepository
from services.transaction_service import TransactionService

transaction_route = APIRouter()


@transaction_route.put(
    "/deposit",
    response_model=UserTransaction,
    summary="Deposit money to user balance",
    status_code=status.HTTP_200_OK
)
async def deposit(user_id: str, amount: float, session=Depends(get_session)) -> UserTransaction:
    # TODO: id пользователя экстрактим из access_token
    user_repository = UserRepository(session)
    user = user_repository.get_by_id(user_id)

    transaction_service = TransactionService(session)

    return transaction_service.make_transaction(user, amount, TransactionType.DEPOSIT)


@transaction_route.put(
    "/withdraw",
    response_model=UserTransaction,
    summary="Withdraw money from user balance",
    status_code=status.HTTP_200_OK
)
async def deposit(user_id: str, amount: float, session=Depends(get_session)) -> UserTransaction:
    # TODO: id пользователя экстрактим из access_token
    user_repository = UserRepository(session)
    user = user_repository.get_by_id(user_id)

    transaction_service = TransactionService(session)

    return transaction_service.make_transaction(user, amount, TransactionType.WITHDRAW)


@transaction_route.get(
    "/",
    response_model=List[UserTransaction],
    summary="Get transactions of current user",
    status_code=status.HTTP_200_OK
)
async def get_transactions(user_id: str, session=Depends(get_session)) -> List[UserTransaction]:
    # TODO: id пользователя экстрактим из access_token
    user_repository = UserRepository(session)
    user = user_repository.get_by_id(user_id)

    # TODO: скорее всего сортировка нужна будет
    return user.transactions
