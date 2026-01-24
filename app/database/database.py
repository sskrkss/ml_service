import atexit
from sqlalchemy.engine.base import Engine
from sqlmodel import SQLModel, create_engine, Session

from .config import get_settings
from ..services.user_service import UserService

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
                user_service.sign_up(email="test@mail.ru",
                                     username="test_user",
                                     password="test_password")

                session.commit()
    except Exception as e:
        raise
