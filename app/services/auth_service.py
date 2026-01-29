import logging

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from models import User, Balance
from repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    def sign_up(self, email: str, username: str, password: str) -> User:
        if self.user_repository.get_by_email(email):
            logger.error(f"Signup attempt with existing email: {email}")

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        if self.user_repository.get_by_username(username):
            logger.error(f"Signup attempt with existing username: {username}")

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists"
            )

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

    def sign_in(self, emailOrUsername: str, password: str):
        pass

    def sign_out(self):
        pass

    def refresh_token(self):
        pass
