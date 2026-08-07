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
```

## Features

- Webhook endpoint registration
- Event creation and dispatch
- Event filtering by type
- Asynchronous webhook delivery
- Retry with exponential backoff
- Maximum retry attempts
- Idempotent event processing
- HMAC webhook signatures
- Delivery status tracking
- Delivery history
- PostgreSQL persistence
- Redis-based asynchronous processing
- Request validation with Pydantic
- API documentation with OpenAPI
- Automated tests with Pytest
- Static analysis and formatting with Ruff
- Type checking with mypy
- Docker-based local development
- Health checks
- Structured logging

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

### Database

- PostgreSQL

### Asynchronous processing

- Redis
- CeleryFeatures

### Quality

- Pytest
- Ruff
- mypy

### Infrastructure

- Docker
- Docker Compose

## Architecture

The initial version follows a modular monolith architecture.

```text
app/
├── main.py
│
├── modules/
│   ├── webhooks/
│   ├── events/
│   └── deliveries/
│
├── infrastructure/
│   ├── database.py
│   ├── redis.py
│   └── celery.py
│
└── config.py
```

The goal is to maintain strong module boundaries while avoiding the operational
complexity of microservices before it is actually necessary.

## Core Concepts

### Webhook

A webhook is an HTTP callback triggered by an event.

For example:

```http
POST /webhooks
```

```json
{
  "url": "https://example.com/webhook",
  "events": ["user.created", "order.created"]
}
```

When an event occurs:

```http
POST /events
```

```json
{
  "type": "user.created",
  "data": {
    "id": 123,
    "name": "John"
  }
}
```

The service identifies the registered endpoints interested in that event and creates delivery jobs.

### Asynchronous delivery

The API should not wait for external webhook endpoints to respond.

Instead:

```text
Client
  │
  │ POST /events
  ▼
FastAPI
  │
  │ enqueue
  ▼
Redis
  │
  ▼
Celery Worker
  │
  ▼
External Webhook
```

The API can therefore respond quickly while the delivery happens in the
background.

### Retry

External systems may be temporarily unavailable.

A failed delivery can be retried using exponential backoff:

```text
Attempt 1 → 5s
Attempt 2 → 10s
Attempt 3 → 20s
Attempt 4 → 40s
Attempt 5 → 80s
```

After the maximum number of attempts, the delivery is marked as permanently
failed.

### Idempotency

The same event may be delivered more than once.

Each event therefore receives a unique identifier.

```text
{
  "id": "evt_01J...",
  "type": "payment.approved"
}
```

The system must prevent duplicate processing where possible.

### HMAC signatures

Webhook payloads are signed using a secret shared between the service and
the webhook consumer.

```text
signature = HMAC-SHA256(secret, payload)
```

The signature is sent through an HTTP header:

```http
X-Webhook-Signature: ...
```

The consumer can independently verify the authenticity of the request.

## API

Initial endpoints:

### Webhooks

```http
POST /webhooks
GET /webhooks
GET /webhooks/{id}
PATCH /webhooks/{id}
DELETE /webhooks/{id}
```

### Events

```http
POST /events
GET /events/{id}
```

### Deliveries

```http
GET /deliveries
GET /deliveries/{id}
POST /deliveries/{id}/retry
```

### Health

```http

```

```http
GET /health
```

### Example

Register a webhook:

```http
POST /webhooks
```

```json
Content-Type: application/json
{
  "url": "https://example.com/webhooks",
  "events": [
    "user.created"
  ]
}

```

Create an event:

```http
POST /events
```

```json
Content-Type: application/json
{
  "type": "user.created",
  "data": {
    "id": 123,
    "name": "John"
  }
}
```

The system asynchronously delivers:

```http
POST https://example.com/webhooks
Content-Type: application/json
X-Webhook-Id: wh_123
X-Event-Id: evt_123
X-Webhook-Signature: ...
```

```json
{
  "id": "evt_123",
  "type": "user.created",
  "data": {
    "id": 123,
    "name": "John"
  }
}
```

## Development Principles

The project follows a few architectural principles:

- High cohesion
- Low coupling
- Explicit module boundaries
- Dependency inversion where useful
- Explicit domain models
- Asynchronous processing for external deliveries
- Idempotent operations
- Observable failures
- Automated testing

The architecture should remain as simple as possible while satisfying the
actual requirements.

## Future Improvements

Potential future iterations include:

- Rate limiting
- Dead-letter queue
- Webhook replay
- Event versioning
- API authentication
- Multi-tenant support
- Delivery metrics
- Prometheus integration
- Distributed tracing
- Horizontal worker scaling
- Webhook endpoint health monitoring
- Dashboard for delivery history
