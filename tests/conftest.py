import os

from fastapi.testclient import TestClient

from webhook_delivery_service import env  # noqa: F401

import pytest
from sqlalchemy import text

from webhook_delivery_service.main import app
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


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"X-API-Key": os.environ["API_KEY"]}
