import hmac
import hashlib
from webhook_delivery_service.modules.delivery.signature import (
    generate_signature,
)


def test_generate_signature() -> None:
    payload = b'{"user_id":"123"}'
    secret = "super-secret"

    signature = generate_signature(payload, secret)

    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    assert signature == expected


def test_generate_signature_changes_with_secret() -> None:
    payload = b'{"user_id":"123"}'

    signature_1 = generate_signature(payload, "secret-1")
    signature_2 = generate_signature(payload, "secret-2")

    assert signature_1 != signature_2


def test_generate_signature_changes_with_payload() -> None:
    secret = "super-secret"

    signature_1 = generate_signature(
        b'{"user_id":"123"}',
        secret,
    )
    signature_2 = generate_signature(
        b'{"user_id":"456"}',
        secret,
    )

    assert signature_1 != signature_2
