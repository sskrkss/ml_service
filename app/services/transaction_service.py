from sqlmodel import Session

from models.enums import TransactionType
from models.user_transaction import UserTransaction
from models.user import User
from repositories.user_repository import UserRepository


class TransactionService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    # TODO: Добавить логику, если баланс отрицательный, плюс продумать логику для админа
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
