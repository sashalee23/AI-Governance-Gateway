from dataclasses import dataclass
from typing import List, Literal

Decision = Literal["ALLOW", "DENY"]

@dataclass
class PolicyResult:
    decision: Decision
    reasons: List[str]
    flags: List[str]

def evaluate_policy(audience: str, data_classification: str, pii_detected: bool) -> PolicyResult:
    reasons: List[str] = []
    flags: List[str] = []

    # Confidential data must not be processed for an external audience.
    if data_classification == "confidential" and audience == "external":
        return PolicyResult(
            decision = "DENY",
            reasons = ["Confidential data cannot be processed for an external audience."],
            flags=["CONFIDENTIAL_EXTERNAL"]
        )

    if pii_detected:
        flags.append("PII_DETECTED")
        reasons.append("Possible PII detected in input.")

    return PolicyResult(decision="ALLOW", reasons=reasons, flags=flags)