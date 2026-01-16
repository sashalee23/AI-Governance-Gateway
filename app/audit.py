import json
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .db import get_conn

# hash the input text for the log!
def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def save_audit_record(
    *,
    request_id: str,
    text: str,
    audience: str,
    data_classification: str,
    pii_detected: bool,
    policy_decision: str,
    policy_reasons: List[str],
    risk_flags: List[str],
    summary: str,
) -> None:
    created_at = datetime.now(timezone.utc).isoformat()
    input_hash = sha256_text(text)

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO audit_log (
                request_id, created_at, audience, data_classification,
                input_hash, pii_detected, policy_decision, policy_reasons,
                risk_flags, summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                created_at,
                audience,
                data_classification,
                input_hash,
                1 if pii_detected else 0,
                policy_decision,
                json.dumps(policy_reasons),
                json.dumps(risk_flags),
                summary,
            ),
        )
        conn.commit()

def get_audit_record(request_id: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM audit_log WHERE request_id = ?",
            (request_id,),
        ).fetchone()

    if row is None:
        return None

    return {
        "request_id": row["request_id"],
        "created_at": row["created_at"],
        "audience": row["audience"],
        "data_classification": row["data_classification"],
        "input_hash": row["input_hash"],
        "pii_detected": bool(row["pii_detected"]),
        "policy_decision": row["policy_decision"],
        "policy_reasons": json.loads(row["policy_reasons"]),
        "risk_flags": json.loads(row["risk_flags"]),
        "summary": row["summary"],
    }
