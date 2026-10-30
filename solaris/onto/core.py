"""Núcleo ontológico mínimo sobre C (proyección determinista para JR-0.1).

La ontología algebraica completa (afirmación, negación nula, doble negación y
colapso) llega en la Semana 2. Aquí el estado se deriva del hash del contexto
para que el walking skeleton sea reproducible y auditable.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass

from solaris.schemas import ComplexState


@dataclass
class OntologyCore:
    def project(self, context: str) -> ComplexState:
        digest = hashlib.sha256(context.encode("utf-8")).digest()
        unit = lambda chunk: int.from_bytes(chunk, "big") / 2**32  # noqa: E731
        modulus = 0.5 + 1.5 * unit(digest[:4])
        phase = -math.pi + 2 * math.pi * unit(digest[4:8])
        real = modulus * math.cos(phase)
        imag = modulus * math.sin(phase)
        return ComplexState(
            real=round(real, 6),
            imag=round(imag, 6),
            modulus=round(modulus, 6),
            phase=round(phase, 6),
            collapsed=round(modulus**2, 6),
            is_collapsed=False,
        )
