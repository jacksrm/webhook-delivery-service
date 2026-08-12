from unittest.mock import Mock

from webhook_delivery_service.modules.delivery.client import (
    DeliveryClient,
)


def test_delivery_client_sends_post_request() -> None:
    http_client = Mock()
    http_client.post.return_value.status_code = 200

    client = DeliveryClient(http_client, timeout=10.0)

    response = client.post(
        url="https://example.com/webhook",
        payload={"user_id": "123"},
        headers={"X-Webhook-Signature": "signature"},
    )

    http_client.post.assert_called_once_with(
        "https://example.com/webhook",
        json={"user_id": "123"},
        headers={"X-Webhook-Signature": "signature"},
        timeout=10.0,
    )

    assert response.status_code == 200


def test_delivery_client_uses_timeout() -> None:
    http_client = Mock()
    http_client.post.return_value.status_code = 200

    client = DeliveryClient(
        http_client,
        timeout=10.0,
    )

    client.post(
        url="https://example.com/webhook",
        payload={"user_id": "123"},
        headers={},
    )

    http_client.post.assert_called_once_with(
        "https://example.com/webhook",
        json={"user_id": "123"},
        headers={},
        timeout=10.0,
    )
