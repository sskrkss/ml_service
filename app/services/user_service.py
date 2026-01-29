import logging
from typing import List

from fastapi import HTTPException, status
from sqlmodel import Session

from models.enums import UserRole
from models.user import User
from repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)

    def get_users(self) -> List[User]:
        return self.user_repository.get_all()

    def get_user_by_id(self, id: str) -> User:
        user = self.user_repository.get_by_id(id)

        if user is None:
            logger.error(f"User with id:{id} not found")

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id:{id} not found"
            )

        return user

    def add_admin_role(self, user: User) -> User:
        user.add_role(UserRole.ADMIN)

        return self.user_repository.save(user)
