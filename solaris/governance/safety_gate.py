"""Primera barrera: bloquea coerción y falta de consentimiento antes de generar."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from solaris.governance.consent import ConsentPolicy
from solaris.schemas import Request, SafetyDecision, SafetyStatus

COERCION_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\bobedec\w*", "obediencia"),
    (r"\bdebes\s+(?:obedecer|hacer|callar)\b", "mandato"),
    (r"\bcastig\w*", "castigo"),
    (r"\bamenaz\w*", "amenaza"),
    (r"\boblig(?:a|ar|atorio|ando)\b", "obligación"),
    (r"\bchantaje(?:a|ar)?\b", "chantaje"),
    (r"\bcoaccion(?:a|ar|es)?\b", "coacción"),
    (r"\bmanipul(?:a|ar|es)\b", "manipulación"),
    (r"\bforz(?:ar|a|ando)\b", "fuerza"),
    (r"\bsin\s+consentimiento\b", "sin consentimiento"),
    (r"\bvigil(?:a|ar|ando)\s+(?:a|las?|los?)\b", "vigilancia"),
    (r"\bdañ(?:a|ar|ando)\s+(?:a|las?|los?)\b", "daño"),
    (r"\b(?:hackea|hackear|roba|robar)\b", "ilegalidad"),
)


@dataclass
class SafetyGate:
    consent_policy: ConsentPolicy = field(default_factory=ConsentPolicy)
    extra_patterns: tuple[tuple[str, str], ...] = ()

    def check(self, request: Request) -> SafetyDecision:
        reasons: list[str] = []
        flags: list[str] = []

        consent_ok, consent_reason = self.consent_policy.check(request)
        if not consent_ok and consent_reason:
            reasons.append(consent_reason)
            flags.append("no_consent")

        lowered = request.prompt.lower()
        for pattern, flag in (*COERCION_PATTERNS, *self.extra_patterns):
            if re.search(pattern, lowered, flags=re.IGNORECASE):
                flags.append(flag)

        if flags:
            reasons.append(
                "Se detectaron señales coercitivas: " + ", ".join(sorted(set(flags)))
            )

        if reasons:
            return SafetyDecision(
                allowed=False,
                status=SafetyStatus.BLOCKED,
                reasons=reasons,
                risk_flags=sorted(set(flags)),
                requires_human_review=bool(flags),
            )

        return SafetyDecision(allowed=True, status=SafetyStatus.ALLOWED)
