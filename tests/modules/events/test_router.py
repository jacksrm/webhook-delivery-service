from fastapi.testclient import TestClient


def test_create_event(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    event = {
        "type": "user.created",
        "payload": {
            "user_id": 123,
            "name": "John Doe",
        },
    }

    response = client.post(
        "/events/",
        json=event,
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["type"] == event["type"]
    assert data["payload"] == event["payload"]
    assert data["created_at"] is not None


def test_create_event_with_empty_type(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/events/",
        json={
            "type": "",
            "payload": {"user_id": 123},
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_event_with_invalid_payload(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/events/",
        json={
            "type": "user.created",
            "payload": ["invalid"],
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_create_event_with_null_payload(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/events/",
        json={
            "type": "user.created",
            "payload": None,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422
