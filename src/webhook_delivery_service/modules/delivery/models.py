from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from webhook_delivery_service.infrastructure.database import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    event_id: Mapped[UUID] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )

    webhook_id: Mapped[UUID] = mapped_column(
        ForeignKey("webhooks.id"), nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default="pending"
    )

    attempts: Mapped[int] = mapped_column(nullable=False, default=0)

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

    def __init__(self, event_id: UUID, webhook_id: UUID):
        self.id = uuid4()
        self.event_id = event_id
        self.webhook_id = webhook_id
        self.status = "pending"
        self.attempts = 0
