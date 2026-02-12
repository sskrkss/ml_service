from typing import Sequence
from uuid import UUID

from sqlmodel import select, desc

from models import User, MlTask
from repositories.base_repository import BaseRepository


class MlTaskRepository(BaseRepository[MlTask]):
    def get_by_id(self, id: UUID) -> MlTask | None:
        statement = select(MlTask).where(MlTask.id == id)

        return self._session.exec(statement).first()

    def get_by_user(self, user: User) -> Sequence[MlTask]:
        statement = (
            select(MlTask)
            .where(MlTask.user_id == user.id)
            .order_by(desc(MlTask.created_at))
        )

        return self._session.exec(statement).all()
