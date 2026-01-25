from sqlmodel import Session

from models.balance import Balance
from models.enums import UserRole
from models.user import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    def add_admin_role(self, user: User) -> User:
        user.add_role(UserRole.ADMIN)

        return self.user_repository.save(user)

    def sign_up(self, email: str, username: str, password: str) -> User:
        # TODO: Добавить хэширование для пароля
        password_hash = password

        user = User(
            email=email,
            username=username,
            password_hash=password_hash
        )

        user.balance = Balance(
            amount=0.0,
            user_id=user.id
        )

        return self.user_repository.save(user)
