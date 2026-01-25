from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
