from fastapi.security.utils import get_authorization_scheme_param
from fastapi.testclient import TestClient
from sqlmodel import select, Session

from auth.cookie_util import AUTH_COOKIE_NAME
from auth.hash_password_util import HashPassword
from auth.jwt_handler import verify_access_token
from models import User


def test_sign_up(client: TestClient, session: Session):
    response = client.post(
        "/api/sign-up",
        json={
            "email": "user@test.com",
            "username": "test_user",
            "plain_password": "qwerty123$",
        }
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Registration successful"}

    statement = select(User).where(User.email == "user@test.com")
    found_user = session.exec(statement).first()

    assert found_user.email == "user@test.com"
    assert found_user.username == "test_user"
    assert found_user.balance.amount == 0
    assert len(found_user.transactions) == 0
    assert len(found_user.ml_tasks) == 0
    assert HashPassword().verify_hash("qwerty123$", found_user.password_hash)

    cookie_value = response.cookies.get(AUTH_COOKIE_NAME)
    scheme, token = get_authorization_scheme_param(cookie_value)
    token = token.strip('"')
    payload = verify_access_token(token)

    assert payload["user_id"] == str(found_user.id)


def test_sign_up_not_unique_username(client: TestClient):
    client.post(
        "/api/sign-up",
        json={
            "email": "user1@test.com",
            "username": "test_user1",
            "plain_password": "qwerty123$",
        }
    )

    response = client.post(
        "/api/sign-up",
        json={
            "email": "user2@test.com",
            "username": "test_user1",
            "plain_password": "qwerty123$",
        }
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email or username already exists"}


def test_sign_up_not_unique_email(client: TestClient):
    client.post(
        "/api/sign-up",
        json={
            "email": "user3@test.com",
            "username": "test_user3",
            "plain_password": "qwerty123$",
        }
    )

    response = client.post(
        "/api/sign-up",
        json={
            "email": "user3@test.com",
            "username": "test_user4",
            "plain_password": "qwerty123$",
        }
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email or username already exists"}


def test_sign_up_not_valid_email_format(client: TestClient):
    response = client.post(
        "/api/sign-up",
        json={
            "email": "usertest.com",
            "username": "test_user5",
            "plain_password": "qwerty123$",
        }
    )

    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"] ==
            "value is not a valid email address: An email address must have an @-sign.")


def test_sign_up_short_username(client: TestClient):
    response = client.post(
        "/api/sign-up",
        json={
            "email": "user6@test.com",
            "username": "test",
            "plain_password": "qwerty123$",
        }
    )

    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"] ==
            "Value error, Username must be at least 5 characters")


def test_sign_up_long_username(client: TestClient):
    response = client.post(
        "/api/sign-up",
        json={
            "email": "user7@test.com",
            "username": "test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test_test",
            "plain_password": "qwerty123$",
        }
    )

    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"] ==
            "Value error, Username must not exceed 50 characters")


def test_sign_up_short_password(client: TestClient):
    response = client.post(
        "/api/sign-up",
        json={
            "email": "user8@test.com",
            "username": "test_user8",
            "plain_password": "qwerty",
        }
    )

    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"] ==
            "Value error, Password must be at least 8 characters")
