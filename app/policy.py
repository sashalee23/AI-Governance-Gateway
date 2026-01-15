from dataclasses import dataclass
from typing import List, Literal

Decision = Literal["ALLOW", "DENY"]

@dataclass
class PolicyResult:
    decision: Decision
    reasons: List[str]
    flags: List[str]
    