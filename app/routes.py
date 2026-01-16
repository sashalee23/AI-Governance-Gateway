from fastapi import APIRouter
from uuid import uuid4
from .schemas import SummarizeRequest, SummarizeResponse
from .classification import detect_pii
from .policy import evaluate_policy

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

    # If the policy is Deny then we need to return a safe response (No AI call)
    if policy.decision == "DENY":
        return SummarizeResponse(
            request_id=request_id,
            summary=f"(Fake for now) Summary of {len(req.text)} characters. Blah.",
            risk_flags=policy.flags,
            policy_decision="DENY",
            policy_reasons=policy.reasons
        )

    return SummarizeResponse(
        request_id=request_id,
        summary=f"(Fake for now) Summary of {len(req.text)} characters. Blah.",
        risk_flags=policy.flags,
        policy_decision="ALLOW",
        policy_reasons=policy.reasons
    )