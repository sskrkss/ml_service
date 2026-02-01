from sqlalchemy.engine.base import Engine
from sqlmodel import SQLModel, create_engine, Session

from database.config import get_settings
from services.auth_service import AuthService
from services.user_service import UserService

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

    return _engine


def init_db(drop_all: bool = False, with_test_data: bool = False) -> None:
    """
    Initialize database schema and create test data.
    
    Args:
        drop_all: If True, drops all tables before creation
        with_test_data: If True, creates test data
    
    Raises:
        Exception: Any database-related exception
    """
    engine = get_database_engine()
    if drop_all:
        SQLModel.metadata.drop_all(engine)

    SQLModel.metadata.create_all(engine)

    if with_test_data:
        generate_test_data(engine)


def close_db():
    """
    Close connection and delete engine.
    """
    global _engine
    if _engine:
        _engine.dispose()
        _engine = None


def get_session():
    """
    Get session for engine.
    """
    engine = get_database_engine()

    with Session(engine) as session:
        yield session


def generate_test_data(engine: Engine) -> None:
    with Session(engine) as session:
        auth_service = AuthService(session)

        test_user = auth_service.sign_up(
            email=f"sskrk@gmail.com",
            username=f"sskrk",
            plain_password=f"12345678"
        )

        user_service = UserService(session)
        user_service.add_admin_role(test_user)
