from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import select, Session

from auth.s2s_authenticator import S2S_SECRET_KEY
from models import User, Balance
from services.ml_task_service import RUN_TASK_PRICE


def test_ml_task_run(client: TestClient):
    response1 = client.get("/api/users/current")

    assert response1.status_code == 200
    assert response1.json()['balance']['amount'] == 1.0

    response2 = client.post(
        "/api/ml-tasks/run",
        json={"input_text": "This was awesome day"},
    )

    assert response2.status_code == 200

    response3 = client.get(f"/api/ml-tasks/{response2.json()['id']}")

    assert response2.status_code == 200
    assert response3.json() == response2.json()

    response4 = client.get("/api/users/current")

    assert response4.status_code == 200
    assert response4.json()['balance']['amount'] == 1.0

    s2s_test_token = jwt.encode(
        claims={
            "iss": "ml_worker",
            "sub": "app",
        },
        key=S2S_SECRET_KEY,
        algorithm="HS256",
    )
    response5 = client.post(
        "/api/ml-tasks/save-prediction",
        json={
            "task_id": response2.json()["id"],
            "task_status": "completed",
            "prediction": ["ok"],
            "worker_id": "test-worker",
        },
        headers={"Authorization": f"Bearer {s2s_test_token}"},
    )
    assert response5.status_code == 200

    response6 = client.get("/api/users/current")

    assert response6.status_code == 200
    assert response6.json()['balance']['amount'] == 1.0 - RUN_TASK_PRICE

    response7 = client.get(f"/api/ml-tasks/{response2.json()['id']}")

    assert response7.status_code == 200
    assert response7.json()["id"] == response2.json()["id"]
    assert response7.json()["task_status"] == "completed"
    assert response7.json()["prediction"] == ["ok"]
    assert response7.json()["worker_id"] == "test-worker"


def test_ml_task_run_short_input_text(client: TestClient, session: Session):
    response = client.post(
        "/api/ml-tasks/run",
        json={"input_text": "This"},
    )

    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"] ==
            "String should have at least 5 characters")


def test_ml_task_run_long_input_text(client: TestClient, session: Session):
    response = client.post(
        "/api/ml-tasks/run",
        json={"input_text": """
            This was awesome day
            This was awesome day
            This was awesome day
            This was awesome day
            This was awesome day
            This was awesome day
            This was awesome day
        """},
    )

    assert response.status_code == 422
    assert (response.json()["detail"][0]["msg"] ==
            "String should have at most 200 characters")


def test_ml_task_run_insufficient_balance(client: TestClient, session: Session):
    statement = select(User).where(User.username == "test_auth_user")
    authorized_user = session.exec(statement).first()

    authorized_user.balance.amount = 0
    session.commit()

    response1 = client.get("/api/users/current")

    assert response1.status_code == 200
    assert response1.json()['balance']['amount'] == 0

    response2 = client.post(
        "/api/ml-tasks/run",
        json={"input_text": "This was awesome day"},
    )

    assert response2.status_code == 409
    assert response2.json() == {"detail": "Transaction declined: insufficient account balance"}
