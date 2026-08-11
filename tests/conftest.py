import pytest
from sqlalchemy import text

from webhook_delivery_service.infrastructure.database import (
    SessionLocal,
)


@pytest.fixture(autouse=True)
def clean_database() -> None:
    with SessionLocal() as db:
        db.execute(
            text(
                """ 
                TRUNCATE TABLE
                    deliveries,
                    events,
                    webhook_event_types,
                    webhooks
                RESTART IDENTITY CASCADE
                """
            )
        )

        db.commit()
