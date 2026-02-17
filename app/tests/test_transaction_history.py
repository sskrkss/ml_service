from fastapi.testclient import TestClient
from jose import jwt

from auth.s2s_authenticator import S2S_SECRET_KEY
from models.enums import TransactionType
from services.ml_task_service import RUN_TASK_PRICE


def test_transaction_history(client: TestClient):
    response1 = client.get("/api/transactions")
    assert response1.status_code == 200
    assert response1.json() == []

    response2 = client.put(
        "/api/transactions/deposit",
        json={"amount": 123},
    )
    assert response2.status_code == 200

    response3 = client.get("/api/transactions")

    assert response3.status_code == 200
    assert len(response3.json()) == 1
    assert response3.json()[0] == response2.json()

    response4 = client.post(
        "/api/ml-tasks/run",
        json={"input_text": "This was awesome day"},
    )

    assert response4.status_code == 200

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
            "task_id": response4.json()["id"],
            "task_status": "completed",
            "prediction": ["ok"],
            "worker_id": "test-worker",
        },
        headers={"Authorization": f"Bearer {s2s_test_token}"},
    )
    assert response5.status_code == 200

    response6 = client.get("/api/transactions")

    assert response6.status_code == 200
    assert len(response6.json()) == 2
    assert response6.json()[1] == response2.json()
    assert response6.json()[0]["transaction_type"] == TransactionType.WITHDRAW
    assert response6.json()[0]["amount"] == RUN_TASK_PRICE
