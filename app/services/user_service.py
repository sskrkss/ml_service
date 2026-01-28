from typing import List

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

        # try:
        #     if UserService.get_user_by_email(data.email, session):
        #         logger.warning(f"Signup attempt with existing email: {data.email}")
        #         raise HTTPException(
        #             status_code=status.HTTP_409_CONFLICT,
        #             detail="User with this email already exists"
        #         )
        #
        #     user = User(
        #         email=data.email,
        #         password=data.password)
        #     UserService.create_user(user, session)
        #     logger.info(f"New user registered: {data.email}")
        #     return {"message": "User successfully registered"}
        #
        # except Exception as e:
        #     logger.error(f"Error during signup: {str(e)}")
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail="Error creating user"
        #     )

        return self.user_repository.save(user)

    def get_users(self) -> List[User]:
        return self.user_repository.get_all()
