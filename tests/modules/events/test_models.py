from uuid import UUID

from webhook_delivery_service.modules.events.models import Event


def test_event_model() -> None:
    event = Event(
        type="user.created",
        data={
            "id": 123,
            "user": {"name": "John", "roles": ["admin", "user"]},
        },
    )

    assert isinstance(event.id, UUID)
    assert event.type == "user.created"
    assert event.data == {
        "id": 123,
        "user": {"name": "John", "roles": ["admin", "user"]},
    }


def test_event_generates_unique_ids() -> None:
    event_a = Event(type="user.created", data={"id": 1})

    event_b = Event(type="user.created", data={"id": 2})

    assert event_a.id != event_b.id
