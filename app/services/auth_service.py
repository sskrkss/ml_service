from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from auth.hash_password_util import HashPassword
from models import User, Balance
from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    def sign_up(self, email: str, username: str, plain_password: str) -> User:
        if self.user_repository.get_by_email(email) or self.user_repository.get_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email or username already exists"
            )

        hash_password = HashPassword()
        hashed_password = hash_password.create_hash(plain_password)

        user = User(
            email=email,
            username=username,
            password_hash=hashed_password
        )

        user.balance = Balance(
            amount=0.0,
            user_id=user.id
        )

        return self.user_repository.save(user)

    def sign_in(self, email_or_username: str, plain_password: str) -> User:
        user = self.user_repository.get_by_email(email_or_username)

        if user is None:
            user = self.user_repository.get_by_username(email_or_username)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        hash_password = HashPassword()
        is_password_valid = hash_password.verify_hash(plain_password, user.password_hash)

        if not is_password_valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return user
