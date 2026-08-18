from typing import Any
from uuid import UUID

from celery.exceptions import MaxRetriesExceededError
import httpx
from celery import Task

from ....infrastructure.celery import celery_app
from ....infrastructure.database import SessionLocal
from ....modules.delivery.models import Delivery
from ....modules.events.models import Event
from ....modules.webhooks.models import Webhook
from ...delivery.client import DeliveryClient


@celery_app.task(
    bind=True,
    retry_backoff=True,
    max_retries=4,
)  # type: ignore[untyped-decorator]
def process_delivery(self: Task, delivery_id: str) -> dict[str, Any]:
    with SessionLocal() as db:
        delivery = db.get(Delivery, UUID(delivery_id))

        if delivery is None:
            raise ValueError(f"Delivery {delivery_id} not found")

        if delivery.status == "success":
            return {
                "delivery_id": str(delivery.id),
                "status": delivery.status,
            }

        if delivery.status == "dead":
            return {
                "delivery_id": str(delivery.id),
                "status": delivery.status,
            }

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
            try:
                raise self.retry(exc=exc) from exc
            except MaxRetriesExceededError:
                delivery.status = "dead"
                db.commit()
                raise
