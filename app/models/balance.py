from uuid import UUID
from sqlmodel import Field

from models.base_entity import BaseEntity


class Balance(BaseEntity, table=True):
    amount: float = Field(
        default=0.0,
        nullable=False
    )
    user_id: UUID = Field(
        foreign_key="user.id",
        unique=True,
        nullable=True
    )

    def deposit(self, amount: float) -> None:
        self.amount += amount

    def withdraw(self, amount: float) -> None:
        self.amount -= amount
