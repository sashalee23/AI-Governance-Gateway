import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "audit.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_log (
                request_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                audience TEXT NOT NULL,
                data_classification TEXT NOT NULL,
                input_hash TEXT NOT NULL,
                pii_detected INTEGER NOT NULL,
                policy_decision TEXT NOT NULL,
                policy_reasons TEXT NOT NULL,
                risk_flags TEXT NOT NULL,
                summary TEXT NOT NULL
            )
            """
        )
        conn.commit()
