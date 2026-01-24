from .base_entity import BaseEntity
from enums import TransactionType


class Transaction(BaseEntity):
    def __init__(self, type: TransactionType, amount: float):
        super().__init__()

        self._type = type
        self._amount = amount

    @property
    def type(self) -> TransactionType:
        return self._type

    @property
    def amount(self) -> float:
        return self._amount
