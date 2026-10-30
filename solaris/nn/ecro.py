"""ECRO: lentes que deforman la percepción latente."""

from __future__ import annotations

from dataclasses import dataclass

from solaris.schemas import AffectState, ECROState


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


@dataclass
class ECRO:
    def encode(self, affect: AffectState) -> ECROState:
        lenses = {
            "apertura": _clamp01(0.5 + 0.3 * affect.valence + 0.2 * affect.arousal),
            "rigor": _clamp01(0.5 + 0.3 * affect.tension),
            "cuidado": _clamp01(0.5 + 0.4 * affect.valence - 0.2 * affect.tension),
            "exploracion": _clamp01(0.5 + 0.4 * affect.arousal),
            "defensa": _clamp01(0.3 + 0.6 * affect.tension),
        }
        dominant = max(lenses, key=lenses.__getitem__)
        return ECROState(
            lenses={name: round(value, 3) for name, value in lenses.items()},
            description=f"Lente dominante: {dominant}",
        )
