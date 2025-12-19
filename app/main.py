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

app = FastAPI()

@app.on_event("startup")
def startup():
    validate_config()
    init_db()
