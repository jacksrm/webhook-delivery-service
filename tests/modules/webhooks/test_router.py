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


def test_list_webhooks() -> None:
    webhooks = [
        {
            "url": "https://example.com/webhook-1",
            "secret": "secret-1",
            "event_types": ["user.created"],
        },
        {
            "url": "https://example.com/webhook-2",
            "secret": "secret-2",
            "event_types": ["order.created", "order.updated"],
        },
    ]

    for webhook in webhooks:
        response = client.post("/webhooks/", json=webhook)
        assert response.status_code == 201

    response = client.get("/webhooks/")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert {item["url"] for item in data} == {
        "https://example.com/webhook-1",
        "https://example.com/webhook-2",
    }

    event_types_by_url = {
        item["url"]: set(item["event_types"]) for item in data
    }

    assert event_types_by_url["https://example.com/webhook-1"] == {
        "user.created"
    }

    assert event_types_by_url["https://example.com/webhook-2"] == {
        "order.created",
        "order.updated",
    }

    for item in data:
        assert "secret" not in item
