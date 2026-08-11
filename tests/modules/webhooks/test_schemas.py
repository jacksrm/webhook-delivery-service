from webhook_delivery_service.modules.webhooks.schemas import (
    WebhookCreate,
)


def test_webhook_create_schema() -> None:
    webhook = WebhookCreate(
        url="https://example.com/webhook",
        secret="my-secret",
        event_types=["user.created", "order.created"],
    )

    assert webhook.url == "https://example.com/webhook"
    assert webhook.secret == "my-secret"
    assert webhook.event_types == ["user.created", "order.created"]
