from enum import Enum


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"


class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionType(Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
