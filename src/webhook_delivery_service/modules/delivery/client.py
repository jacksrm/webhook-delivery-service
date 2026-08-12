from typing import Any

import httpx


class DeliveryClient:
    def __init__(self, http_client: httpx.Client) -> None:
        self.http_client = http_client

    def post(
        self,
        url: str,
        payload: dict[str, Any],
        headers: dict[str, str],
    ) -> httpx.Response:
        return self.http_client.post(
            url,
            json=payload,
            headers=headers,
        )
