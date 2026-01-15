from pydantic import BaseModel
from typing import Literal, List

Audience = Literal["internal", "external"]
Classification = Literal["public", "internal", "confidential", "unknown"]

class SummarizeRequest(BaseModel):
    text: str
    audience: Audience
    data_classification: Classification