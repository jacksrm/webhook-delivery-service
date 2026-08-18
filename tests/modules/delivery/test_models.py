from uuid import uuid4

from webhook_delivery_service.modules.delivery.models import Delivery


def test_delivery_model() -> None:
    event_id = uuid4()
    webhook_id = uuid4()

    delivery = Delivery(
        event_id=event_id,
        webhook_id=webhook_id,
    )

    assert delivery.event_id == event_id
    assert delivery.webhook_id == webhook_id
    assert delivery.status == "pending"
    assert delivery.attempts == 0


def test_delivery_generates_unique_ids() -> None:

    event_id = uuid4()
    webhook_id = uuid4()

    delivery_a = Delivery(
        event_id=event_id,
        webhook_id=webhook_id,
    )

    delivery_b = Delivery(
        event_id=event_id,
        webhook_id=webhook_id,
    )

    assert delivery_a.id != delivery_b.id


def test_delivery_can_have_dead_status() -> None:
    delivery = Delivery(
        event_id=uuid4(),
        webhook_id=uuid4(),
    )

    delivery.status = "dead"

    assert delivery.status == "dead"
