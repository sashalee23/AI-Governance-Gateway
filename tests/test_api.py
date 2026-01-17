import os
from app.main import app
from app.db import init_db
from fastapi.testclient import TestClient

def test_summarize_allow(tmp_path):
    os.environ["AUDIT_DB_PATH"] = str(tmp_path / "api_allow.db")
    init_db()

    client = TestClient(app)
    resp = client.post(
        "/v1/tasks/summarize",
        json={
            "text": "hello world",
            "audience": "internal",
            "data_classification": "public",
        },
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["policy_decision"] == "ALLOW"
    assert "request_id" in body

def test_summarize_deny_confidential_external(tmp_path):
    os.environ["AUDIT_DB_PATH"] = str(tmp_path / "api_deny.db")
    init_db()

    client = TestClient(app)
    resp = client.post(
        "/v1/tasks/summarize",
        json={
            "text": "secret roadmap",
            "audience": "external",
            "data_classification": "confidential",
        },
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["policy_decision"] == "DENY"
    assert body["summary"] == "Request denied by policy."
    assert "Confidential data cannot be processed" in body["policy_reasons"][0]
