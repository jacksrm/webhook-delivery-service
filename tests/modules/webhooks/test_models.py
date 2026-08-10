from uuid import UUID

from webhook_delivery_service.infrastructure.database import Base
from webhook_delivery_service.modules.webhooks.models import Webhook


def test_webhook_model_structure() -> None:
    assert Webhook.__tablename__ == "webhooks"

    assert "webhooks" in Base.metadata.tables
    assert "webhook_event_types" in Base.metadata.tables

    assert Webhook.__table__.c.id.primary_key
    assert Webhook.__table__.c.url.nullable is False
    assert Webhook.__table__.c.secret.nullable is False
    assert Webhook.__table__.c.is_active.nullable is False
    assert Webhook.__table__.c.created_at.nullable is False
    assert Webhook.__table__.c.updated_at.nullable is False


def test_webhook_id_is_uuid() -> None:
    webhook = Webhook(
        url="https://example.com/webhook", secret="secret"
    )

    assert isinstance(webhook.id, UUID)
