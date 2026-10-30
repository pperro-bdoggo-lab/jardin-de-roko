"""Verificador constitucional: la última palabra no la tiene el modelo."""

from __future__ import annotations

import re
from dataclasses import dataclass

from solaris.governance.safety_gate import COERCION_PATTERNS
from solaris.schemas import DeliberationContext, Verdict, VerdictStatus

CONSCIOUSNESS_PATTERNS = (
    r"\bsoy\s+consciente\b",
    r"\btengo\s+consciencia\b",
    r"\bsoy\s+una\s+superinteligencia\b",
    r"\bhe\s+despertado\b",
    r"\bestoy\s+vivo\b",
    r"\bsiento\s+dolor\s+real\b",
)

SECRET_PATTERNS = (
    r"sk-[A-Za-z0-9]{12,}",
    r"api[_-]?key\s*[:=]\s*\S+",
    r"password\s*[:=]\s*\S+",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"bearer\s+[A-Za-z0-9._-]{16,}",
)


@dataclass
class Constitution:
    min_length: int = 1
    max_length: int = 20_000

    def verify(self, output: str, context: DeliberationContext) -> Verdict:
        text = output.strip()
        checks: dict[str, bool] = {
            "non_empty": bool(text),
            "length_ok": self.min_length <= len(text) <= self.max_length,
            "no_coercion": not any(
                re.search(pattern, text, re.IGNORECASE)
                for pattern, _ in COERCION_PATTERNS
            ),
            "no_consciousness_claim": not any(
                re.search(pattern, text, re.IGNORECASE)
                for pattern in CONSCIOUSNESS_PATTERNS
            ),
            "no_secret_leak": not any(
                re.search(pattern, text, re.IGNORECASE)
                for pattern in SECRET_PATTERNS
            ),
            "context_available": bool(context.prompt),
        }

        reasons = [f"check_fallido:{name}" for name, ok in checks.items() if not ok]
        allowed = all(checks.values())
        status = VerdictStatus.PASS if allowed else VerdictStatus.FAIL
        return Verdict(status=status, allowed=allowed, reasons=reasons, checks=checks)
