from sqlalchemy import insert

from webhook_delivery_service.infrastructure.database import (
    SessionLocal,
)
from webhook_delivery_service.modules.webhooks.models import (
    Webhook,
    webhook_event_types,
)
from webhook_delivery_service.modules.webhooks.repository import (
    find_webhooks_by_event_type,
)


def test_find_webhooks_by_event_type() -> None:
    with SessionLocal() as db:
        webhook_1 = Webhook(
            url="https://example.com/webhook-1",
            secret="secret-1",
        )
        webhook_2 = Webhook(
            url="https://example.com/webhook-2",
            secret="secret-2",
        )
        webhook_3 = Webhook(
            url="https://example.com/webhook-3",
            secret="secret-3",
        )

        db.add_all([webhook_1, webhook_2, webhook_3])
        db.flush()

        db.execute(
            insert(webhook_event_types),
            [
                {
                    "webhook_id": webhook_1.id,
                    "event_type": "user.created",
                },
                {
                    "webhook_id": webhook_2.id,
                    "event_type": "user.created",
                },
                {
                    "webhook_id": webhook_3.id,
                    "event_type": "order.created",
                },
            ],
        )

        db.commit()

        result = find_webhooks_by_event_type(db, "user.created")

        assert {webhook.id for webhook in result} == {
            webhook_1.id,
            webhook_2.id,
        }


def test_find_webhooks_by_event_type_returns_empty_list() -> None:
    with SessionLocal() as db:
        result = find_webhooks_by_event_type(
            db,
            "user.created",
        )

        assert result == []


def test_find_webhooks_by_event_type_no_unsubscribed_webhooks() -> (
    None
):
    with SessionLocal() as db:
        webhook = Webhook(
            url="https://example.com/webhook",
            secret="secret",
        )

        db.add(webhook)
        db.flush()

        db.execute(
            insert(webhook_event_types),
            [
                {
                    "webhook_id": webhook.id,
                    "event_type": "order.created",
                },
            ],
        )

        db.commit()

        result = find_webhooks_by_event_type(
            db,
            "user.created",
        )

        assert result == []
