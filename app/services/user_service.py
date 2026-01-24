from sqlmodel import Session

from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository


# TODO: Добавить запись в бд, сделать красивые импорты (__init__.py)
class UserService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    def add_admin_role(self, user: User) -> User:
        user.add_role(UserRole.ADMIN)

        return user

    def sign_up(self, email: str, username: str, password: str) -> User:
        # TODO: Добавить хэширование для пароля
        user = User(email=email,
                    username=username,
                    password_hash=password)

        user = self.user_repository.create(user)

        return user
