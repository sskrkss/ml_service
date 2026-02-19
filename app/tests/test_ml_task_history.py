from fastapi.testclient import TestClient
from jose import jwt

from auth.s2s_authenticator import S2S_SECRET_KEY


def test_ml_task_history(client: TestClient):
    response1 = client.post(
        "/api/ml-tasks/run",
        json={"input_text": "This was awesome day"},
    )

    assert response1.status_code == 200

    response2 = client.get("/api/ml-tasks")

    assert response2.status_code == 200
    assert len(response2.json()) == 1
    assert response2.json()[0] == response1.json()

    s2s_test_token = jwt.encode(
        claims={
            "iss": "ml_worker",
            "sub": "app",
        },
        key=S2S_SECRET_KEY,
        algorithm="HS256",
    )
    response3 = client.post(
        "/api/ml-tasks/save-prediction",
        json={
            "task_id": response1.json()["id"],
            "task_status": "completed",
            "prediction": ["ok"],
            "worker_id": "test-worker",
        },
        headers={"Authorization": f"Bearer {s2s_test_token}"},
    )
    assert response3.status_code == 200

    response4 = client.get("/api/ml-tasks")

    assert response4.status_code == 200
    assert len(response4.json()) == 1
    assert response4.json()[0]["id"] == response1.json()["id"]
    assert response4.json()[0]["task_status"] == "completed"
    assert response4.json()[0]["prediction"] == ["ok"]
    assert response4.json()[0]["worker_id"] == "test-worker"
