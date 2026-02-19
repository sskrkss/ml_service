import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from api import app
from auth.authenticator import auth_user
from auth.hash_password_util import HashPassword
from database.database import get_session
from models import User, Balance


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///testing.db", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    hash_password = HashPassword()
    hashed_password = hash_password.create_hash('qwerty123$')

    test_user = User(
        email='auth_user@test.ru',
        username='test_auth_user',
        password_hash=hashed_password
    )

    test_user.balance = Balance(
        amount=1.0,
        user_id=test_user.id
    )

    session.add(test_user)
    session.commit()

    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[auth_user] = lambda: test_user

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
