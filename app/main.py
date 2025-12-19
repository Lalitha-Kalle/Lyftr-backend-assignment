# app/main.py
import hmac
import hashlib
import time
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from app.config import validate_config, WEBHOOK_SECRET
from app.models import init_db, get_connection
from app.storage import insert_message
from app.logging_utils import log_request
from fastapi import Query
from app.storage import list_messages

app = FastAPI()

@app.on_event("startup")
def startup():
    validate_config()
    init_db()


@app.get("/messages")
def get_messages(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_: str | None = Query(None, alias="from"),
    since: str | None = None,
    q: str | None = None,
):
    data, total = list_messages(limit, offset, from_, since, q)

    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


