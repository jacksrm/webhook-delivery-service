from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WebhookCreate(BaseModel):
    url: str
    secret: str
    event_types: list[str]


class WebhookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
