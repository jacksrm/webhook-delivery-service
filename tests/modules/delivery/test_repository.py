from sqlalchemy import insert

from webhook_delivery_service.infrastructure.database import (
    SessionLocal,
)
from webhook_delivery_service.modules.delivery.repository import (
    create_deliveries_for_event,
)
from webhook_delivery_service.modules.events.models import Event
from webhook_delivery_service.modules.webhooks.models import (
    Webhook,
    webhook_event_types,
)


def test_create_deliveries_for_event() -> None:
    with SessionLocal() as db:
        event = Event(
            type="user.created",
            payload={"user_id": 123},
        )

        webhook_1 = Webhook(
            url="https://example.com/webhook-1",
            secret="secret-1",
        )
        webhook_2 = Webhook(
            url="https://example.com/webhook-2",
            secret="secret-2",
        )

        db.add_all([event, webhook_1, webhook_2])
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
            ],
        )

        db.commit()

        deliveries = create_deliveries_for_event(db, event)

        assert len(deliveries) == 2

        assert {delivery.webhook_id for delivery in deliveries} == {
            webhook_1.id,
            webhook_2.id,
        }

        assert all(
            delivery.event_id == event.id for delivery in deliveries
        )

        assert all(
            delivery.status == "pending" for delivery in deliveries
        )

        assert all(delivery.attempts == 0 for delivery in deliveries)


def test_create_deliveries_for_eent_returns_empty_list() -> None:
    with SessionLocal() as db:
        event = Event(
            type="user.created",
            payload={"user_id": 123},
        )

        db.add(event)
        db.commit()

        deliveries = create_deliveries_for_event(db, event)

        assert deliveries == []


def test_create_deliveries_for_event_no_unsubscribed_webhooks() -> (
    None
):
    with SessionLocal() as db:
        event = Event(
            type="user.created",
            payload={"user_id": 123},
        )

        webhook = Webhook(
            url="https://example.com/webhook",
            secret="secret",
        )

        db.add_all([event, webhook])
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

        deliveries = create_deliveries_for_event(db, event)

        assert deliveries == []
