from sqlmodel import select, desc, Sequence

from models import User
from models.user_transaction import UserTransaction
from repositories.base_repository import BaseRepository


class TransactionRepository(BaseRepository[UserTransaction]):
    def get_by_user(self, user: User) -> Sequence[UserTransaction]:
        statement = (
            select(UserTransaction)
            .where(UserTransaction.user_id == user.id)
            .order_by(desc(UserTransaction.created_at))
        )

        return self._session.exec(statement).all()
