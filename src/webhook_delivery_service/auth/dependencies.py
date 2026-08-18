import os

from fastapi import Header, HTTPException, status


def authenticate_api_key(
    api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> None:
    expected_api_key = os.getenv("API_KEY")

    if not api_key or api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
