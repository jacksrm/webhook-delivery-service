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


def test_create_event_with_empty_type() -> None:
    response = client.post(
        "/events/",
        json={
            "type": "",
            "payload": {"user_id": 123},
        },
    )

    assert response.status_code == 422


def test_create_event_with_invalid_payload() -> None:
    response = client.post(
        "/events/",
        json={
            "type": "user.created",
            "payload": ["invalid"],
        },
    )

    assert response.status_code == 422


def test_create_event_with_null_payload() -> None:
    response = client.post(
        "/events/",
        json={
            "type": "user.created",
            "payload": None,
        },
    )

    assert response.status_code == 422
