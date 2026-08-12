from fastapi.testclient import TestClient

from webhook_delivery_service.main import app

client = TestClient(app)


def test_create_event() -> None:
    event = {
        "type": "user.created",
        "payload": {
            "user_id": 123,
            "name": "John Doe",
        },
    }

    response = client.post("/events/", json=event)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["type"] == event["type"]
    assert data["payload"] == event["payload"]
    assert data["created_at"] is not None
