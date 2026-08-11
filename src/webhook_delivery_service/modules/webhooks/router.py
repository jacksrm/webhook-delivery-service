from typing import Annotated, cast
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from webhook_delivery_service.infrastructure.dependencies import (
    get_db,
)
from webhook_delivery_service.modules.webhooks.models import (
    Webhook,
    webhook_event_types,
)


from .schemas import (
    WebhookCreate,
    WebhookResponse,
)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post(
    "/",
    response_model=WebhookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_webhook(
    data: WebhookCreate,
    db: Annotated[Session, Depends(get_db)],
) -> WebhookResponse:
    webhook = Webhook(
        url=str(data.url),
        secret=data.secret,
    )

    db.add(webhook)
    db.flush()

    db.execute(
        webhook_event_types.insert(),
        [
            {"webhook_id": webhook.id, "event_type": event_type}
            for event_type in data.event_types
        ],
    )

    db.commit()
    db.refresh(webhook)

    event_types = cast(
        list[str],
        db.execute(
            select(webhook_event_types.c.event_type).where(
                webhook_event_types.c.webhook_id == webhook.id
            )
        )
        .scalars()
        .all(),
    )

    return WebhookResponse(
        id=webhook.id,
        url=webhook.url,
        event_types=event_types,
        is_active=webhook.is_active,
        created_at=webhook.created_at,
        updated_at=webhook.updated_at,
    )


@router.get("/", response_model=list[WebhookResponse])
def list_webhooks(
    db: Annotated[Session, Depends(get_db)],
) -> list[WebhookResponse]:
    webhooks = db.scalars(select(Webhook)).all()

    event_types = db.execute(
        select(
            webhook_event_types.c.webhook_id,
            webhook_event_types.c.event_type,
        ).where(
            webhook_event_types.c.webhook_id.in_(
                [webhook.id for webhook in webhooks]
            )
        )
    ).all()

    event_types_by_webhook: dict[UUID, list[str]] = {}

    for webhook_id, event_type in event_types:
        event_types_by_webhook.setdefault(
            webhook_id,
            [],
        ).append(event_type)

    return [
        WebhookResponse(
            id=webhook.id,
            url=webhook.url,
            event_types=event_types_by_webhook.get(webhook.id, []),
            is_active=webhook.is_active,
            created_at=webhook.created_at,
            updated_at=webhook.updated_at,
        )
        for webhook in webhooks
    ]
