from fastapi.security.utils import get_authorization_scheme_param
from fastapi.testclient import TestClient
from sqlmodel import select, Session

from auth.cookie_util import AUTH_COOKIE_NAME
from auth.jwt_handler import verify_access_token
from models import User


def test_sign_in_by_email(client: TestClient, session: Session):
    client.post(
        "/api/sign-up",
        json={
            "email": "user@test.com",
            "username": "test_user",
            "plain_password": "qwerty123$",
        }
    )

    response = client.post(
        "/api/sign-in",
        json={
            "email_or_username": "user@test.com",
            "plain_password": "qwerty123$",
        }
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

    statement = select(User).where(User.email == "user@test.com")
    found_user = session.exec(statement).first()

    cookie_value = response.cookies.get(AUTH_COOKIE_NAME)
    scheme, token = get_authorization_scheme_param(cookie_value)
    token = token.strip('"')
    payload = verify_access_token(token)

    assert payload["user_id"] == str(found_user.id)


def test_sign_in_by_username(client: TestClient, session: Session):
    client.post(
        "/api/sign-up",
        json={
            "email": "user1@test.com",
            "username": "test_user1",
            "plain_password": "qwerty123$",
        }
    )

    response = client.post(
        "/api/sign-in",
        json={
            "email_or_username": "test_user1",
            "plain_password": "qwerty123$",
        }
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

    statement = select(User).where(User.username == "test_user1")
    found_user = session.exec(statement).first()

    cookie_value = response.cookies.get(AUTH_COOKIE_NAME)
    scheme, token = get_authorization_scheme_param(cookie_value)
    token = token.strip('"')
    payload = verify_access_token(token)

    assert payload["user_id"] == str(found_user.id)


def test_sign_in_not_found(client: TestClient, session: Session):
    response = client.post(
        "/api/sign-in",
        json={
            "email_or_username": "test_user2",
            "plain_password": "qwerty123$",
        }
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

    cookie_value = response.cookies.get(AUTH_COOKIE_NAME)

    assert cookie_value is None


def test_sign_in_wrong_password(client: TestClient, session: Session):
    client.post(
        "/api/sign-up",
        json={
            "email": "user3@test.com",
            "username": "test_user3",
            "plain_password": "qwerty123$",
        }
    )

    response = client.post(
        "/api/sign-in",
        json={
            "email_or_username": "test_user3",
            "plain_password": "qwerty123",
        }
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

    cookie_value = response.cookies.get(AUTH_COOKIE_NAME)

    assert cookie_value is None
