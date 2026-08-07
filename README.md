# Webhook Delivery Service

A reliable and scalable webhook delivery service built with Python and FastAPI.

The service allows applications to register webhook endpoints and asynchronously
deliver events to them with retry mechanisms, idempotency, HMAC signatures and
delivery tracking.

## Overview

Webhooks allow systems to communicate through events without requiring
continuous polling.

Instead of a consumer repeatedly asking:

"Has something happened?"

the producer sends an HTTP request when an event occurs.

This project provides the infrastructure required to reliably deliver those
events.

```text
                    ┌─────────────────┐
                    │   Client/API    │
                    └────────┬────────┘
                             │
                         POST /events
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │      API        │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │      Redis      │
                    │      Queue      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Celery Workers  │
                    └────────┬────────┘
                             │
                ┌────────────┼────────────┐
                ▼            ▼            ▼
           Webhook #1   Webhook #2   Webhook #3
