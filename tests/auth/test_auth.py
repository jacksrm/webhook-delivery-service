from fastapi.testclient import TestClient


def test_request_without_api_key_returns_401(
    client: TestClient,
) -> None:

    response = client.get("/webhooks")

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API key"}


def test_request_with_invalid_api_key_returns_401(
    client: TestClient,
) -> None:

    response = client.get(
        "/webhooks",
        headers={"X-API-Key": "invalid-api-key"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API key"}


def test_request_with_valid_api_key_is_allowed(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:

    response = client.get(
        "/webhooks",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_events_request_without_api_key_returns_401(
    client: TestClient,
) -> None:
    response = client.post(
        "/events/",
        json={
            "type": "user.created",
            "payload": {"user_id": "123"},
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API key"}


def test_events_request_with_valid_api_key_is_allowed(
    client: TestClient,
    auth_headers: dict[str, str],
) -> None:
    response = client.post(
        "/events/",
        json={
            "type": "user.created",
            "payload": {"user_id": "123"},
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
