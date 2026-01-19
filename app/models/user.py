from typing import List
from base_entity import BaseEntity
from enums import UserRole
from transaction import Transaction
from prediction import Prediction


class User(BaseEntity):
    def __init__(self, email: str, username: str, password_hash: str):
        super().__init__()

        self._email = email
        self._username = username
        self._password_hash = password_hash
        self._balance: float = 0
        self._roles: List[UserRole] = [UserRole.USER]
        self._transactions: List[Transaction] = []
        self._predictions: List[Prediction] = []

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
    def predictions(self) -> List[Prediction]:
        return self._predictions

    def add_role(self, role: UserRole) -> None:
        if role not in self._roles:
            self._roles.append(role)
