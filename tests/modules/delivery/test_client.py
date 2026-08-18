import json
from unittest.mock import Mock

from webhook_delivery_service.modules.delivery.client import (
    DeliveryClient,
)


def test_delivery_client_sends_post_request() -> None:
    http_client = Mock()
    http_client.post.return_value.status_code = 200

    client = DeliveryClient(http_client, timeout=10.0)

    payload = json.dumps(
        {"user_id": "123"},
        separators=(",", ":"),
    ).encode()

    response = client.post(
        url="https://example.com/webhook",
        payload=payload,
        headers={"X-Webhook-Signature": "signature"},
    )

    http_client.post.assert_called_once_with(
        "https://example.com/webhook",
        content=payload,
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

    payload = json.dumps(
        {"user_id": "123"},
        separators=(",", ":"),
    ).encode()

    client.post(
        url="https://example.com/webhook",
        payload=payload,
        headers={},
    )

    http_client.post.assert_called_once_with(
        "https://example.com/webhook",
        content=payload,
        headers={},
        timeout=10.0,
    )
