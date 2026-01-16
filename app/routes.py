from fastapi import APIRouter
from uuid import uuid4
from .schemas import SummarizeRequest, SummarizeResponse
from .classification import detect_pii
from .policy import evaluate_policy
from .audit import save_audit_record

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/v1/tasks/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    request_id = str(uuid4())

    pii_detected = detect_pii(req.text)

    policy = evaluate_policy(
        audience = req.audience,
        data_classification = req.data_classification,
        pii_detected = pii_detected
    )

    if policy.decision == "DENY":
        resp = SummarizeResponse(
            request_id=request_id,
            summary="Request denied by policy.",
            risk_flags=policy.flags,
            policy_decision="DENY",
            policy_reasons=policy.reasons
        )
        save_audit_record(
            request_id=request_id,
            text=req.text,
            audience=req.audience,
            data_classification=req.data_classification,
            pii_detected=pii_detected,
            policy_decision=resp.policy_decision,
            policy_reasons=resp.policy_reasons,
            risk_flags=resp.risk_flags,
            summary=resp.summary,
        )
        return resp

    resp = SummarizeResponse(
        request_id=request_id,
        summary=f"(Fake for now) Summary of {len(req.text)} characters. Blah.",
        risk_flags=policy.flags,
        policy_decision="ALLOW",
        policy_reasons=policy.reasons
    )

    save_audit_record(
        request_id=request_id,
        text=req.text,
        audience=req.audience,
        data_classification=req.data_classification,
        pii_detected=pii_detected,
        policy_decision=resp.policy_decision,
        policy_reasons=resp.policy_reasons,
        risk_flags=resp.risk_flags,
        summary=resp.summary,
    )

    return resp