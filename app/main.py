import hmac
import hashlib
import time
from fastapi import FastAPI, Request, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

from app.config import validate_config, WEBHOOK_SECRET
from app.models import init_db, get_connection
from app.storage import insert_message, list_messages, get_stats
from app.logging_utils import log_request

app = FastAPI()


@app.on_event("startup")
def startup_event():
    validate_config()
    init_db()


class WebhookMessage(BaseModel):
    message_id: str = Field(..., min_length=1)
    from_: str = Field(..., alias="from", regex=r"^\+\d+$")
    to: str = Field(..., regex=r"^\+\d+$")
    ts: str
    text: Optional[str] = Field(None, max_length=4096)


def verify_signature(secret: str, body: bytes, signature: str) -> bool:
    computed = hmac.new(
        secret.encode("utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, signature)

@app.post("/webhook")
async def webhook(request: Request):
    start_time = time.time()
    raw_body = await request.body()
    signature = request.headers.get("X-Signature")

    # Signature validation
    if not signature or not verify_signature(WEBHOOK_SECRET, raw_body, signature):
        log_request(
            method="POST",
            path="/webhook",
            status=401,
            latency_ms=0,
            result="invalid_signature"
        )
        raise HTTPException(status_code=401, detail="invalid signature")

    # Payload validation
    try:
        payload = await request.json()
        msg = WebhookMessage(**payload)
    except Exception:
        log_request(
            method="POST",
            path="/webhook",
            status=422,
            latency_ms=0,
            result="validation_error"
        )
        raise

    # Insert into DB (idempotent)
    result = insert_message({
        "message_id": msg.message_id,
        "from": msg.from_,
        "to": msg.to,
        "ts": msg.ts,
        "text": msg.text
    })

    latency_ms = int((time.time() - start_time) * 1000)

    log_request(
        method="POST",
        path="/webhook",
        status=200,
        latency_ms=latency_ms,
        message_id=msg.message_id,
        dup=(result == "duplicate"),
        result=result
    )

    return {"status": "ok"}




@app.get("/messages")
def get_messages(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_: Optional[str] = Query(None, alias="from"),
    since: Optional[str] = None,
    q: Optional[str] = None,
):
    data, total = list_messages(limit, offset, from_, since, q)

    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset,
    }



@app.get("/stats")
def stats():
    return get_stats()



@app.get("/health/live")
def health_live():
    return {"status": "alive"}


@app.get("/health/ready")
def health_ready():
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="not ready")
