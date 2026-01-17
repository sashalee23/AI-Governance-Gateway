import os
import sqlite3
from pathlib import Path

def get_db_path() -> Path:
    default = Path(__file__).resolve().parent.parent / "audit.db"
    return Path(os.environ.get("AUDIT_DB_PATH", str(default)))

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
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
                summary TEXT NOT NULL,
                prompt_version TEXT NOT NULL,
                prompt_hash TEXT NOT NULL
            )
            """
        )
        conn.commit()
