from sqlalchemy import text

from webhook_delivery_service.infrastructure.database import engine


def test_database_connection() -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        assert result.scalar() == 1
