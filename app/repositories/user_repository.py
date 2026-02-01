from sqlmodel import select, Sequence

from models.user import User
from repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def get_by_id(self, id: str) -> User | None:
        statement = select(User).where(User.id == id)

        return self._session.exec(statement).first()

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self._session.exec(statement).first()

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)

        return self._session.exec(statement).first()

    def get_all(self) -> Sequence[User]:
        statement = select(User).order_by(User.username)

        return self._session.exec(statement).all()
