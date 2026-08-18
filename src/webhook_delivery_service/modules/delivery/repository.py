from uuid import UUID

from sqlalchemy.orm import Session

from ...modules.events.models import Event
from ...modules.webhooks.repository import (
    find_webhooks_by_event_type,
)
from .models import Delivery


def create_deliveries_for_event(
    db: Session,
    event: Event,
) -> list[Delivery]:
    webhooks = find_webhooks_by_event_type(db, event.type)

    deliveries = [
        Delivery(event_id=event.id, webhook_id=webhook.id)
        for webhook in webhooks
    ]

    db.add_all(deliveries)

    return deliveries


def update_delivery_status(
    db: Session,
    delivery_id: UUID,
    status: str,
) -> None:
    delivery = db.get(Delivery, delivery_id)

    if delivery is None:
        raise ValueError("Delivery not found")

    delivery.status = status
    db.commit()
