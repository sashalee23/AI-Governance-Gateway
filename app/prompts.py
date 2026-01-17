"""
Prompt loading utilities.

Prompts are treated as versioned system artifacts. We load them from files
to support change review, auditability, and future regression testing.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

@dataclass(frozen=True)
class PromptArtifact:
    """A loaded prompt plus metadata suitable for audit logging."""
    version: str
    text: str
    sha256: str

def load_prompt(version: str) -> PromptArtifact:
    """
    Load a prompt file by version name (e.g. "summarize_v1").

    Expects a file at: prompts/{version}.txt
    """
    path = PROMPTS_DIR / f"{version}.txt"
    text = path.read_text(encoding="utf-8")
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return PromptArtifact(version=version, text=text, sha256=sha)
