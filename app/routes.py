from fastapi import APIRouter
from uuid import uuid4
from .schemas import SummarizeRequest, SummarizeResponse

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/v1/tasks/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    # THis is a placeholder: I got no policies & no AI yet
    return SummarizeResponse(
        request_id=str(uuid4()),
        summary=f"(Fake for now) Summary of {len(req.text)} characters. Blah.",
        risk_flags=[],
        policy_decision="ALLOW",
        policy_reasons=["PLACEHOLDER: no policy checks in this project yet."]
    )