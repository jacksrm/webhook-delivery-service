from typing import Any
from uuid import UUID

import httpx
from celery import Task

from ....infrastructure.celery import celery_app
from ....infrastructure.database import SessionLocal
from ....modules.delivery.models import Delivery
from ....modules.events.models import Event
from ....modules.webhooks.models import Webhook
from ...delivery.client import DeliveryClient


@celery_app.task(bind=True)  # type: ignore[untyped-decorator]
def process_delivery(self: Task, delivery_id: str) -> dict[str, Any]:
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

        try:
            with httpx.Client() as http_client:
                client = DeliveryClient(
                    http_client=http_client,
                    timeout=10.0,
                )

                response = client.post(  # noqa: F841
                    url=webhook.url,
                    payload=event.payload,
                    headers={},
                )

            return {
                "delivery_id": str(delivery.id),
                "webhook_url": webhook.url,
                "event_type": event.type,
                "payload": event.payload,
            }
        except httpx.RequestError as exc:
            raise self.retry(exc=exc) from exc
