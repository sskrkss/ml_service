from app.models.enums import UserRole
from app.models.user import User


# TODO: Добавить запись в бд
class UserService:
    def add_admin_role(self, user: User) -> User:
        user.add_role(UserRole.ADMIN)

        return user

    def sign_up(self, username: str, email: str, password: str) -> User:
        # TODO: Добавить хэширование для пароля
        user = User(username, email, password)

        return user
