from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    type: str
    payload: dict[str, Any]


class EventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    type: str
    payload: dict[str, Any]
    created_at: datetime
