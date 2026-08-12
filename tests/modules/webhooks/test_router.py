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


def test_get_webhook() -> None:
    webhook = {
        "url": "https://example.com/webhook",
        "secret": "super-secret",
        "event_types": ["user.created", "order.created"],
    }

    create_response = client.post("/webhooks/", json=webhook)

    assert create_response.status_code == 201

    created_data = create_response.json()
    webhook_id = created_data["id"]

    response = client.get(f"/webhooks/{webhook_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == webhook_id
    assert data["url"] == webhook["url"]
    assert set(data["event_types"]) == set(webhook["event_types"])
    assert data["is_active"] is True
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
    assert "secret" not in data


def test_get_webhook_not_found() -> None:
    response = client.get(
        "/webhooks/00000000-0000-0000-0000-000000000000"
    )

    assert response.status_code == 404


def test_update_webhook() -> None:
    webhook = {
        "url": "https://example.com/webhook",
        "secret": "super-secret",
        "event_types": ["user.created", "order.created"],
    }

    create_response = client.post("/webhooks/", json=webhook)

    assert create_response.status_code == 201

    webhook_id = create_response.json()["id"]

    response = client.patch(
        f"/webhooks/{webhook_id}",
        json={
            "url": "https://example.com/updated-webhook",
            "event_types": ["order.created", "order.updated"],
            "is_active": False,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == webhook_id
    assert data["url"] == "https://example.com/updated-webhook"
    assert set(data["event_types"]) == {
        "order.created",
        "order.updated",
    }
    assert data["is_active"] is False
    assert "secret" not in data


def test_update_webhook_partial() -> None:
    webhook = {
        "url": "https://example.com/webhook",
        "secret": "super-secret",
        "event_types": ["user.created", "order.created"],
    }

    create_response = client.post("/webhooks/", json=webhook)

    assert create_response.status_code == 201

    webhook_id = create_response.json()["id"]

    response = client.patch(
        f"/webhooks/{webhook_id}",
        json={"is_active": False},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["url"] == webhook["url"]
    assert set(data["event_types"]) == set(webhook["event_types"])
    assert data["is_active"] is False


def test_update_webhook_not_found() -> None:
    response = client.patch(
        "/webhooks/00000000-0000-0000-0000-000000000000",
        json={"is_active": False},
    )

    assert response.status_code == 404


def test_delete_webhook() -> None:
    webhook = {
        "url": "https://example.com/webhook",
        "secret": "super-secret",
        "event_types": ["user.created", "order.created"],
    }

    create_response = client.post("/webhooks/", json=webhook)

    assert create_response.status_code == 201

    webhook_id = create_response.json()["id"]

    response = client.delete(f"/webhooks/{webhook_id}")

    assert response.status_code == 204

    get_response = client.get(f"/webhooks/{webhook_id}")

    assert get_response.status_code == 404


def test_delete_webhook_not_found() -> None:
    response = client.delete(
        "/webhooks/00000000-0000-0000-0000-000000000000",
    )

    assert response.status_code == 404
