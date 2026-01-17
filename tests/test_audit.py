import os
from pathlib import Path

from app.db import init_db
from app.audit import save_audit_record, get_audit_record

def test_audit_round_trip(tmp_path):
    # Use a temporary sqlite database file for this test
    test_db_path = tmp_path / "test_audit.db"
    os.environ["AUDIT_DB_PATH"] = str(test_db_path)

    # Create the schema in the test db
    init_db()

    request_id = "test-request-123"

    save_audit_record(
        request_id=request_id,
        text="hello world",
        audience="internal",
        data_classification="public",
        pii_detected=False,
        policy_decision="ALLOW",
        policy_reasons=["ok"],
        risk_flags=["NONE"],
        summary="fake summary",
        prompt_version="summarize_v1",
        prompt_hash="dummyhash",
    )

    record = get_audit_record(request_id)
    assert record is not None
    assert record["request_id"] == request_id
    assert record["audience"] == "internal"
    assert record["data_classification"] == "public"
    assert record["policy_decision"] == "ALLOW"
    assert record["policy_reasons"] == ["ok"]
    assert record["risk_flags"] == ["NONE"]
    assert record["summary"] == "fake summary"
    assert record["input_hash"]  # should exist and be non-empty
