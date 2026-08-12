from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Webhook, webhook_event_types


def find_webhooks_by_event_type(
    db: Session, event_type: str
) -> list[Webhook]:
    statement = (
        select(Webhook)
        .join(
            webhook_event_types,
            webhook_event_types.c.webhook_id == Webhook.id,
        )
        .where(
            webhook_event_types.c.event_type == event_type,
        )
    )

    return list(db.scalars(statement).all())
