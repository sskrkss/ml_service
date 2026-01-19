from typing import List

from base_entity import BaseEntity
from enums import UserRole
from ml_task import MlTask
from transaction import Transaction


class User(BaseEntity):
    def __init__(self, email: str, username: str, password_hash: str):
        super().__init__()

        self._email = email
        self._username = username
        self._password_hash = password_hash
        self._balance: float = 0
        self._roles: List[UserRole] = [UserRole.USER]
        self._transactions: List[Transaction] = []
        self._ml_tasks: List[MlTask] = []

    @property
    def email(self) -> str:
        return self._email

    @property
    def username(self) -> str:
        return self._username

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def roles(self) -> List[UserRole]:
        return self._roles

    @property
    def transactions(self) -> List[Transaction]:
        return self._transactions

    @property
    def ml_tasks(self) -> List[MlTask]:
        return self._ml_tasks

    def add_role(self, role: UserRole) -> None:
        if role not in self._roles:
            self._roles.append(role)

    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def add_ml_task(self, ml_task: MlTask) -> None:
        self._ml_tasks.append(ml_task)

    def increase_balance(self, amount: float) -> None:
        self._balance += amount

    def decrease_balance(self, amount: float) -> None:
        self._balance -= amount
