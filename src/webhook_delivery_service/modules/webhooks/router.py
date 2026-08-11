from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from webhook_delivery_service.infrastructure.dependencies import (
    get_db,
)
from webhook_delivery_service.modules.webhooks.models import Webhook

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
    webhook: WebhookCreate,
    db: Annotated[Session, Depends(get_db)],
) -> Webhook:
    db_webhook = Webhook(
        url=str(webhook.url),
        secret=webhook.secret,
    )

    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)

    return db_webhook
