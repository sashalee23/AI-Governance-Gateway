import json
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Literal, Sequence, TypedDict

from .db import get_conn

def sha256_text(text: str) -> str:
    """
    Return a SHA-256 hash of the given text.

    Governance note:
        - We store the hash (fingerprint) instead of raw text to avoid logging
          potentially sensitive input while still supporting audit/replay checks.
    """
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
    prompt_version: str,
    prompt_hash: str,
) -> None:

    """
    Persist an audit record for a summarize request.

    Args:
        request_id: Unique identifier for this request (UUID string).
        text: Raw input text. This function will hash it; it is not stored.
        audience: 'internal' or 'external'.
        data_classification: 'public' | 'internal' | 'confidential' | 'unknown'.
        pii_detected: Whether simple PII detection flagged the text.
        policy_decision: 'ALLOW' or 'DENY'.
        policy_reasons: Human-readable reasons explaining the decision.
        risk_flags: Machine-readable flags for dashboards/metrics.
        summary: The returned summary (or denial message).
        prompt_version: The version of the prompt file used.
        prompt_hash: Hash of the prompt text used for this request.

    Security/Governance:
        - Stores only input_hash, not raw text.
        - Stores reasons + flags so decisions are explainable later.
    """

    created_at = datetime.now(timezone.utc).isoformat()
    input_hash = sha256_text(text)

    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO audit_log (
                request_id, created_at, audience, data_classification,
                input_hash, pii_detected, policy_decision, policy_reasons,
                risk_flags, summary, prompt_version, prompt_hash
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                prompt_version,
                prompt_hash,
            ),
        )
        conn.commit()

def get_audit_record(request_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a stored audit record by request_id.

    Returns:
        The audit record dict if found, otherwise None.
    """
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
        "prompt_version": row["prompt_version"],
        "prompt_hash": row["prompt_hash"],
    }
