import hashlib
import hmac


def generate_signature(payload: bytes, secret: str) -> str:
    return hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
