from sqlmodel import select

from repositories.base_repository import BaseRepository
from models.user import User


class UserRepository(BaseRepository[User]):
    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        return self._session.exec(statement).first()
