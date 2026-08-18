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
        payload: bytes,
        headers: dict[str, str],
    ) -> httpx.Response:
        return self.http_client.post(
            url,
            content=payload,
            headers=headers,
            timeout=self.timeout,
        )
