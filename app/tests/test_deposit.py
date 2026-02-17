from datetime import datetime

from fastapi.testclient import TestClient


def test_deposit(client: TestClient):
    response1 = client.get("/api/users/current")

    assert response1.status_code == 200
    assert response1.json()['balance']['amount'] == 1.0

    response2 = client.put(
        "/api/transactions/deposit",
        json={
            "amount": 0.1
        }
    )

    assert response2.status_code == 200
    assert response2.json()['amount'] == 0.1
    assert response2.json()['transaction_type'] == "deposit"
    assert datetime.fromisoformat(response2.json()['created_at']).date() == datetime.now().date()

    response3 = client.get("/api/users/current")

    assert response3.status_code == 200
    assert response3.json()['balance']['amount'] == 1.1
