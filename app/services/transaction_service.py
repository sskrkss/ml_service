from app.models.enums import TransactionType
from app.models.transaction import Transaction
from app.models.user import User


# TODO: Добавить запись в бд, сделать красивые импорты (__init__.py)
class TransactionService:
    # TODO: Добавить логику, если баланс отрицательный, плюс продумать логику для админа
    def make_transaction(self, user: User, amount: float, transaction_type: TransactionType) -> Transaction:
        transaction = Transaction(transaction_type, amount)

        user.add_transaction(transaction)

        if transaction_type == transaction_type.DEPOSIT:
            user.increase_balance(amount)
        elif transaction_type == transaction_type.WITHDRAW:
            user.decrease_balance(amount)

        return transaction
