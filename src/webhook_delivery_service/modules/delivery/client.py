from typing import Any

import httpx


class DeliveryClient:
    def __init__(
        self,
        http_client: httpx.Client,
        timeout: float,
    ) -> None:
        self.http_client = http_client
        self.timeout = timeout

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
            timeout=self.timeout,
        )
