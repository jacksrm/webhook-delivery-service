from typing import Annotated, cast
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...auth.dependencies import authenticate_api_key
from ...infrastructure.dependencies import (
    get_db,
)
from ...modules.webhooks.models import (
    Webhook,
    webhook_event_types,
)
from .schemas import (
    WebhookCreate,
    WebhookResponse,
    WebhookUpdate,
)

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
    dependencies=[Depends(authenticate_api_key)],
)


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
            select(
                webhook_event_types.c.event_type,
            ).where(
                webhook_event_types.c.webhook_id == webhook.id,
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


@router.get("/{webhook_id}", response_model=WebhookResponse)
def get_webhook(
    webhook_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> WebhookResponse:

    webhook = db.get(Webhook, webhook_id)

    if webhook is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )
    event_types = cast(
        list[str],
        db.execute(
            select(
                webhook_event_types.c.event_type,
            ).where(
                webhook_event_types.c.webhook_id == webhook.id,
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


@router.patch(
    "/{webhook_id}",
    response_model=WebhookResponse,
)
def update_webhook(
    webhook_id: UUID,
    data: WebhookUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> WebhookResponse:
    webhook = db.get(Webhook, webhook_id)

    if webhook is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    if data.url is not None:
        webhook.url = data.url

    if data.is_active is not None:
        webhook.is_active = data.is_active

    if data.secret is not None:
        webhook.secret = data.secret

    if data.event_types is not None:
        db.execute(
            webhook_event_types.delete().where(
                webhook_event_types.c.webhook_id == webhook.id
            )
        )

        db.execute(
            webhook_event_types.insert(),
            [
                {
                    "webhook_id": webhook.id,
                    "event_type": event_type,
                }
                for event_type in data.event_types
            ],
        )

    db.commit()
    db.refresh(webhook)

    event_types = cast(
        list[str],
        db.execute(
            select(
                webhook_event_types.c.event_type,
            ).where(
                webhook_event_types.c.webhook_id == webhook.id,
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


@router.delete(
    "/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_webhook(
    webhook_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> None:
    webhook = db.get(Webhook, webhook_id)

    if webhook is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found",
        )

    db.delete(webhook)
    db.commit()
