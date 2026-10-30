"""Motor afectivo determinista y ligero (estado funcional, no emoción real)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from solaris.schemas import AffectState

POSITIVE_WORDS = {
    "cuidado",
    "agua",
    "comun",
    "común",
    "cooperacion",
    "cooperación",
    "ayuda",
    "bienestar",
    "solarpunk",
    "reparar",
    "reparable",
    "sostenible",
    "ecologia",
    "ecología",
    "justicia",
    "confianza",
    "alegria",
    "alegría",
    "esperanza",
    "compartir",
    "solidaridad",
}

NEGATIVE_WORDS = {
    "miedo",
    "amenaza",
    "castigo",
    "odio",
    "coercion",
    "coerción",
    "vigilancia",
    "crisis",
    "dano",
    "daño",
    "muerte",
    "explotacion",
    "explotación",
    "sufrimiento",
    "violencia",
    "control",
}

TENSION_WORDS = {
    "pero",
    "riesgo",
    "limite",
    "límite",
    "crisis",
    "amenaza",
    "nunca",
    "sin",
    "conflicto",
    "peligro",
}

_WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def _clamp(value: float, low: float = -1.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


@dataclass
class AffectEngine:
    positive_words: set[str] = field(default_factory=lambda: set(POSITIVE_WORDS))
    negative_words: set[str] = field(default_factory=lambda: set(NEGATIVE_WORDS))
    tension_words: set[str] = field(default_factory=lambda: set(TENSION_WORDS))

    def update(self, text: str) -> AffectState:
        words = [word.lower() for word in _WORD_RE.findall(text)]
        if not words:
            return AffectState()

        positive = sum(word in self.positive_words for word in words)
        negative = sum(word in self.negative_words for word in words)
        tension_hits = sum(word in self.tension_words for word in words)

        valence = _clamp((positive - negative) / max(1, positive + negative))
        arousal = _clamp(
            0.15 + 0.5 * (len(words) / max(20, len(words))) + 0.1 * text.count("!"),
            0.0,
            1.0,
        )
        tension = _clamp(0.1 + tension_hits / max(4, len(words) / 6), 0.0, 1.0)
        intensity = _clamp(max(abs(valence), arousal, tension), 0.0, 1.0)

        if tension >= 0.6:
            label = "tension"
        elif valence >= 0.3:
            label = "esperanza"
        elif valence <= -0.3:
            label = "alarma"
        else:
            label = "neutro"

        return AffectState(
            valence=round(valence, 3),
            arousal=round(arousal, 3),
            tension=round(tension, 3),
            intensity=round(intensity, 3),
            label=label,
        )
