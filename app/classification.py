import re

EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,4}\)?[\s-]?)?\d{3,4}[\s-]?\d{4}\b")

def detect_pii(text: str) -> bool:
    return bool(EMAIL_RE.search(text) or PHONE_RE.search(text))