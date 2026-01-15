from pydantic import BaseModel
from typing import Literal, List

Audience = Literal["internal", "external"]
Classification = Literal["public", "internal", "confidential", "unknown"]

class SummarizeRequest(BaseModel):
    text: str
    audience: Audience
    data_classification: Classification

class SummarizeResponse(BaseModel):
    request_id: str
    summary: str
    risk_flags: List[str]
    policy_decision: Literal["ALLOW", "DENY"]
    policy_reasons: List[str]
