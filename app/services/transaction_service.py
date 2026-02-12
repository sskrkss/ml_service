from fastapi import HTTPException, status
from sqlmodel import Session, Sequence

from models.enums import TransactionType
from models.user import User
from models.user_transaction import UserTransaction
from repositories.transaction_repository import TransactionRepository
from repositories.user_repository import UserRepository


class TransactionService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)
        self.transaction_repository = TransactionRepository(session)

    def make_transaction(self, user: User, amount: float, transaction_type: TransactionType) -> UserTransaction:
        transaction = UserTransaction(
            transaction_type=transaction_type,
            amount=amount
        )

        user.add_transaction(transaction)

        if transaction_type == transaction_type.DEPOSIT:
            user.balance.deposit(amount)
        elif transaction_type == transaction_type.WITHDRAW:
            user.balance.withdraw(amount)

        self.user_repository.save(user)

        return transaction

    def check_balance_before_withdraw(self, user: User, amount: float) -> None:
        if amount > user.balance.amount:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Transaction declined: insufficient account balance"
            )

    def get_transactions_by_user(self, user: User) -> Sequence[UserTransaction]:
        return self.transaction_repository.get_by_user(user)
