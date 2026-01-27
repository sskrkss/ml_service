from typing import List, TYPE_CHECKING
from sqlalchemy import Column, JSON
from sqlalchemy.ext.mutable import MutableList
from sqlmodel import Field, Relationship

from models.balance import Balance
from models.base_entity import BaseEntity
from models.enums import UserRole

if TYPE_CHECKING:
    from models.ml_task import MlTask
    from models.user_transaction import UserTransaction


class User(BaseEntity, table=True):
    email: str = Field(
        unique=True,
        index=True,
        min_length=5,
        max_length=255,
        nullable=False
    )
    username: str = Field(
        unique=True,
        index=True,
        min_length=5,
        max_length=255,
        nullable=False
    )
    password_hash: str = Field(
        max_length=255,
        min_length=5,
        nullable=False
    )
    roles: List[UserRole] = Field(
        default_factory=lambda: [UserRole.USER],
        sa_column=Column(
            MutableList.as_mutable(JSON),
            nullable=False
        )
    )
    balance: Balance = Relationship(
        sa_relationship_kwargs={
            "uselist": False,
            "cascade": "all, delete-orphan",
            "single_parent": True,
            "lazy": "selectin"
        }
    )
    transactions: List["UserTransaction"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        }
    )
    ml_tasks: List["MlTask"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        }
    )

    def add_role(self, role: UserRole) -> None:
        if role not in self.roles:
            self.roles.append(role)

    def has_role(self, role: UserRole) -> bool:
        return role in self.roles

    def add_transaction(self, transaction: "UserTransaction") -> None:
        transaction.user_id = self.id
        self.transactions.append(transaction)

    def add_ml_task(self, ml_task: "MlTask") -> None:
        ml_task.user_id = self.id
        self.ml_tasks.append(ml_task)
