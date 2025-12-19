# app/storage.py
from datetime import datetime
import sqlite3
from app.models import get_connection

def insert_message(message):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO messages (message_id, from_msisdn, to_msisdn, ts, text, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            message["message_id"],
            message["from"],
            message["to"],
            message["ts"],
            message.get("text"),
            datetime.utcnow().isoformat() + "Z"
        ))
        conn.commit()
        return "created"
    except sqlite3.IntegrityError:
        return "duplicate"
    finally:
        conn.close()
