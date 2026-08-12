from webhook_delivery_service.infrastructure.celery import celery_app


def test_celery_configuration() -> None:
    celery_main = "webhook_delivery_service"
    broker_url = "redis://localhost:6379/0"
    result_backend = "redis://localhost:6379/1"

    assert celery_app.main == celery_main
    assert celery_app.conf.broker_url == broker_url
    assert celery_app.conf.result_backend == result_backend
