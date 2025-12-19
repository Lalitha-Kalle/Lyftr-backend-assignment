# app/config.py
import os

DATABASE_URL = os.getenv("DATABASE_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def validate_config():
    if not WEBHOOK_SECRET:
        raise RuntimeError("WEBHOOK_SECRET is not set")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
