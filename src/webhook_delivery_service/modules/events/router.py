from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from webhook_delivery_service.infrastructure.dependencies import (
    get_db,
)
from .schemas import EventCreate, EventResponse
from .models import Event

router = APIRouter(prefix="/events", tags=["events"])


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    data: EventCreate,
    db: Annotated[Session, Depends(get_db)],
) -> EventResponse:
    event = Event(
        type=data.type,
        payload=data.payload,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return EventResponse(
        id=event.id,
        type=event.type,
        payload=event.payload,
        created_at=event.created_at,
    )
