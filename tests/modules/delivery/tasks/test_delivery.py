from sqlalchemy import insert

from webhook_delivery_service.infrastructure.database import (
    SessionLocal,
)
from webhook_delivery_service.modules.delivery.models import Delivery
from webhook_delivery_service.modules.delivery.tasks.delivery import (
    process_delivery,
)
from webhook_delivery_service.modules.events.models import Event
from webhook_delivery_service.modules.webhooks.models import (
    Webhook,
    webhook_event_types,
)


def test_process_delivery() -> None:
    with SessionLocal() as db:
        webhook = Webhook(
            url="https://example.com/webhook",
            secret="secret",
        )

        event = Event(
            type="user.created",
            payload={"user_id": "123"},
        )

        db.add_all([webhook, event])
        db.flush()

        db.execute(
            insert(webhook_event_types),
            {
                "webhook_id": webhook.id,
                "event_type": event.type,
            },
        )

        delivery = Delivery(
            event_id=event.id,
            webhook_id=webhook.id,
        )

        db.add(delivery)
        db.commit()

        result = process_delivery(str(delivery.id))

        assert result == {
            "delivery_id": str(delivery.id),
            "webhook_url": "https://example.com/webhook",
            "event_type": "user.created",
            "payload": {"user_id": "123"},
        }
