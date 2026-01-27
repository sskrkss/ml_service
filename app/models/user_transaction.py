from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, Relationship

from models.base_entity import BaseEntity
from models.enums import TransactionType

if TYPE_CHECKING:
    from models.user import User


class UserTransaction(BaseEntity, table=True):
    amount: float = Field(nullable=False)
    transaction_type: TransactionType = Field(nullable=False)
    user_id: UUID = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="transactions")
