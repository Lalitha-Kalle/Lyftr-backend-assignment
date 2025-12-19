# Lyftr AI – Backend Assignment

## Overview

This project is a **FastAPI-based backend service** that ingests WhatsApp-like webhook messages exactly once, stores them in SQLite, and exposes APIs for listing messages, analytics, and health checks.

The service focuses on:
- Secure webhook ingestion using HMAC
- Idempotent message storage
- Pagination and filtering
- Simple analytics
- Production-style validation and logging

---

## Tech Stack

- **Language:** Python 3
- **Framework:** FastAPI
- **Database:** SQLite
- **Validation:** Pydantic

---

## Project Structure

```
app/
├── main.py            # FastAPI app and routes
├── config.py          # Environment variable loading
├── models.py          # Database initialization
├── storage.py         # Database operations
└── logging_utils.py   # Structured JSON logging
```

---

## Environment Variables

The following environment variables must be set before running the app:

| Variable | Description |
|--------|------------|
| `DATABASE_URL` | SQLite DB path (e.g. `sqlite:///./app.db`) |
| `WEBHOOK_SECRET` | Secret used to verify webhook signatures |
| `LOG_LEVEL` | Logging level (INFO / DEBUG), optional |

Example:
```bash
export DATABASE_URL="sqlite:///./app.db"
export WEBHOOK_SECRET="testsecret"
```

---

## How to Run Locally


### 1. Start the server
```bash
uvicorn app.main:app --reload
```

Server runs at:
```
http://localhost:8000
```

---

## API Endpoints

### POST `/webhook`

Ingest inbound messages exactly once.

### GET `/messages`

List stored messages with pagination and filters.

### GET `/stats`

Provide message-level analytics.

### GET `/health/live`

Liveness probe.

### GET `/health/ready`

Readiness probe.

---

## Design Decisions

- **Idempotency:** Enforced using a PRIMARY KEY on `message_id`
- **Security:** HMAC SHA256 signature verification on raw request body
- **Validation:** Strict request validation using Pydantic
- **Persistence:** SQLite chosen for simplicity and portability
- **Logging:** One structured JSON log per request

---

## Setup Used

VS Code + manual implementation
