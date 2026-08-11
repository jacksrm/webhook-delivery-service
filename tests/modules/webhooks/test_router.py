from fastapi.testclient import TestClient

from webhook_delivery_service.main import app

client = TestClient(app)


def test_create_webhook() -> None:
    url = "https://example.com/webhook"
    secret = "super-secret"
    event_types = ["user.created", "order.created"]

    response = client.post(
        "/webhooks/",
        json={
            "url": url,
            "secret": secret,
            "event_types": event_types,
        },
    )
    print(response.json())

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["url"] == url
    assert data["is_active"] is True
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
    assert set(data["event_types"]) == set(event_types)

    assert "secret" not in data
