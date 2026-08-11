from fastapi import FastAPI

from .modules.webhooks.router import router as webhook_router

app = FastAPI()

app.include_router(webhook_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
