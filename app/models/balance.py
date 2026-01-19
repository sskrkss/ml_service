from base_entity import BaseEntity


class Balance(BaseEntity):
    def __init__(self):
        super().__init__()

        self._amount: float = 0

    @property
    def amount(self) -> float:
        return self._amount

    def deposit(self, deposit_amount: float) -> None:
        self._amount += deposit_amount

    def withdraw(self, withdraw_amount: float) -> None:
        self._amount -= withdraw_amount
