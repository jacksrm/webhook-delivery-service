from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ...infrastructure.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    type: Mapped[str] = mapped_column(String(255), nullable=False)

    payload: Mapped[dict[str, Any]] = mapped_column(
        JSON, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (Index("ix_events_type", "type"),)

    def __init__(self, type: str, payload: dict[str, Any]):
        self.id = uuid4()
        self.type = type
        self.payload = payload
