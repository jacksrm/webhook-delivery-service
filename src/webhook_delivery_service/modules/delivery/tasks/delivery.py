from typing import Any
from uuid import UUID

from webhook_delivery_service.modules.delivery.models import Delivery
from webhook_delivery_service.modules.events.models import Event
from webhook_delivery_service.modules.webhooks.models import Webhook

from ....infrastructure.database import SessionLocal

from ....infrastructure.celery import celery_app


@celery_app.task  # type: ignore[untyped-decorator]
def process_delivery(delivery_id: str) -> dict[str, Any]:
    with SessionLocal() as db:
        delivery = db.get(Delivery, UUID(delivery_id))

        if delivery is None:
            raise ValueError(f"Delivery {delivery_id} not found")

        event = db.get(Event, delivery.event_id)
        webhook = db.get(Webhook, delivery.webhook_id)

        if event is None:
            raise ValueError(f"Event {delivery.event_id} not found")

        if webhook is None:
            raise ValueError(
                f"Webhook {delivery.webhook_id} not found"
            )

        return {
            "delivery_id": str(delivery.id),
            "webhook_url": webhook.url,
            "event_type": event.type,
            "payload": event.payload,
        }
