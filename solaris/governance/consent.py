"""Consentimiento opt-in y reversible."""

from __future__ import annotations

from dataclasses import dataclass

from solaris.schemas import Request


@dataclass
class ConsentPolicy:
    require_consent: bool = True

    def check(self, request: Request) -> tuple[bool, str | None]:
        if not self.require_consent:
            return True, None
        if request.consent:
            return True, None
        return False, "La participación requiere consentimiento explícito (opt-in)."
