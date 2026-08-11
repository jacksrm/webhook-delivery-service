from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from webhook_delivery_service.infrastructure.database import Base

webhook_event_types = Table(
    "webhook_event_types",
    Base.metadata,
    Column(
        "webhook_id",
        ForeignKey("webhooks.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "event_type",
        String(255),
        primary_key=True,
    ),
)


class Webhook(Base):
    __tablename__ = "webhooks"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
    )

    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    secret: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __init__(
        self,
        url: str,
        secret: str,
        is_active: bool = True,
    ) -> None:
        self.id = uuid4()
        self.url = url
        self.secret = secret
        self.is_active = is_active
