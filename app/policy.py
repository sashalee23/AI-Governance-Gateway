"""
Policy evaluation logic for AI request governance.

This module contains explicit, deterministic rules that decide whether
a request is allowed to proceed to AI processing.

Design principles:
- Policies are explainable (return human-readable reasons)
- Policies are deterministic (no AI involvement)
- Policies fail closed for clearly unsafe combinations
"""

from dataclasses import dataclass
from typing import List, Literal

Decision = Literal["ALLOW", "DENY"]

@dataclass
class PolicyResult:
     """
    Result of evaluating a governance policy decision.

    Attributes:
        decision: Final allow/deny decision.
        reasons: Human-readable explanations for the decision.
        flags: Machine-readable risk flags for monitoring and audit.
    """
    decision: Decision
    reasons: List[str]
    flags: List[str]

def evaluate_policy(audience: str, data_classification: str, pii_detected: bool) -> PolicyResult:
    """
    Evaluate governance policies for an incoming summarize request.

    Governance notes:
        - Confidential data is never allowed to be processed for an external audience.
        - PII detection currently results in a risk flag, not a hard denial.
        - All decisions are deterministic and explainable.
    """
    
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