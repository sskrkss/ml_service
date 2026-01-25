import atexit
from sqlalchemy.engine.base import Engine
from sqlmodel import SQLModel, create_engine, Session

from database.config import get_settings
from models.enums import TransactionType
from services.user_service import UserService
from services.transaction_service import TransactionService
from services.ml_task_service import MlTaskService
from repositories.user_repository import UserRepository

_engine: Engine | None = None


def get_database_engine() -> Engine:
    """
    Create and configure the SQLAlchemy engine.
    
    Returns:
        Engine: Configured SQLAlchemy engine
    """
    settings = get_settings()

    global _engine
    if _engine is None:
        _engine = create_engine(
            url=settings.DATABASE_URL_psycopg,
            echo=settings.DEBUG,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600
        )

        # TODO: временное решение, пока хз как правильно
        atexit.register(dispose_engine)
    return _engine


def dispose_engine():
    """
    Close connection and delete engine.
    """
    global _engine
    if _engine:
        _engine.dispose()
        _engine = None


def init_db(drop_all: bool = False, with_test_data: bool = False) -> None:
    """
    Initialize database schema and create test data.
    
    Args:
        drop_all: If True, drops all tables before creation
        with_test_data: If True, creates test data
    
    Raises:
        Exception: Any database-related exception
    """
    try:
        engine = get_database_engine()
        if drop_all:
            SQLModel.metadata.drop_all(engine)

        SQLModel.metadata.create_all(engine)

        if with_test_data:
            with Session(engine) as session:
                user_service = UserService(session)
                user = user_service.sign_up(
                    email="test@mail.ru",
                    username="test_user",
                    password="test_password"
                )

                session.commit()

                print("---------------------------DATABASE TEST STARTED---------------------------")

                user_repository = UserRepository(session)
                found_user = user_repository.get_by_email(user.email)

                print()
                print("User")
                print(found_user)

                print()
                print("User's balance")
                print(found_user.balance)

                admin = user_service.add_admin_role(found_user)
                session.commit()

                print()
                print("Add admin role")
                print(admin.roles)

                print()
                print("Deposit 20.5")
                transaction_service = TransactionService(session)
                transaction_service.make_transaction(
                    transaction_type=TransactionType.DEPOSIT,
                    amount=20.5,
                    user=found_user
                )
                session.commit()
                print(found_user.balance)

                print()
                print("Withdraw 10.2")
                transaction_service = TransactionService(session)
                transaction_service.make_transaction(
                    transaction_type=TransactionType.WITHDRAW,
                    amount=10.2,
                    user=found_user
                )
                session.commit()
                print(found_user.balance)

                print()
                print("All user's transactions")
                print(found_user.transactions)

                print()
                print("Add ml task")
                ml_task_service = MlTaskService(session)
                ml_task_service.run_task(
                    dataset={"dataset": "test_dataset"},
                    user=found_user
                )
                session.commit()
                print(found_user.ml_tasks)

                print()
                print("---------------------------DATABASE TEST FINISHED---------------------------")
    except Exception as e:
        raise
