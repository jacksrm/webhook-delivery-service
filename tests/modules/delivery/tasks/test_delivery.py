import httpx
import pytest

from unittest.mock import patch


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

        result = process_delivery.run(str(delivery.id))

        assert result == {
            "delivery_id": str(delivery.id),
            "webhook_url": "https://example.com/webhook",
            "event_type": "user.created",
            "payload": {"user_id": "123"},
        }


def test_process_delivery_retries_on_connection_error() -> None:
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

        with patch(
            "webhook_delivery_service.modules.delivery.tasks.delivery.DeliveryClient"
        ) as client_class:
            client = client_class.return_value
            client.post.side_effect = httpx.ConnectError(
                "Connection failed"
            )

            with patch.object(
                process_delivery,
                "retry",
                side_effect=RuntimeError("retry"),
            ) as retry:
                with pytest.raises(RuntimeError, match="retry"):
                    process_delivery.run(str(delivery.id))

                retry.assert_called_once()


def test_process_delivery_has_exponential_backoff() -> None:
    assert process_delivery.retry_backoff is True


def test_process_delivery_has_max_retries() -> None:
    assert process_delivery.max_retries == 4


def test_process_delivery_does_not_retry_successful_delivery() -> (
    None
):
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
        delivery.status = "success"

        db.add(delivery)
        db.commit()

        with patch(
            "webhook_delivery_service.modules.delivery.tasks.delivery.DeliveryClient"
        ) as client_class:
            process_delivery.run(str(delivery.id))

            client_class.return_value.post.assert_not_called()
