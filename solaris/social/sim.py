"""Simulador social mínimo: impacto rápido de una acción (stub determinista)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from solaris.schemas import ImpactReport, Regime

_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "cuidado",
        ("cuidado", "agua", "salud", "bienestar", "reparar", "compartir"),
    ),
    (
        "cooperacion",
        ("cooperación", "cooperacion", "federad", "común", "comun", "solidaridad"),
    ),
    (
        "ecologia",
        ("ecolog", "sostenible", "huella", "límite", "limite", " regenera"),
    ),
    (
        "coercion",
        ("coerción", "coercion", "castigo", "obedec", "forzar", "amenaza"),
    ),
    (
        "vigilancia",
        ("vigilancia", "vigilar", "rastrear", "espía", "espia"),
    ),
    (
        "extraccion",
        ("extraer", "extractiv", "explotar", "explotación", "explotacion"),
    ),
)

_DELTAS = {
    "cuidado": {"wellbeing": 0.10, "gini": -0.03, "footprint": -0.05, "stability": 0.03},
    "cooperacion": {"wellbeing": 0.08, "gini": -0.02, "stability": 0.05},
    "ecologia": {"wellbeing": 0.03, "footprint": -0.10},
    "coercion": {"wellbeing": -0.15, "infrapower": 0.10, "stability": -0.15},
    "vigilancia": {"wellbeing": -0.10, "infrapower": 0.12, "stability": -0.10},
    "extraccion": {"wellbeing": -0.05, "gini": 0.05, "footprint": 0.15, "stability": -0.05},
}


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


@dataclass
class SocialSim:
    steps: int = 12
    seed: int = 42

    def evaluate(self, action: str) -> ImpactReport:
        values = {
            "wellbeing": 0.55,
            "gini": 0.30,
            "infrapower": 0.20,
            "stability": 0.60,
            "footprint": 0.40,
        }
        lowered = action.lower()
        notes: list[str] = []

        for name, words in _KEYWORDS:
            if any(re.search(word, lowered) for word in words):
                notes.append(f"senal_detectada:{name}")
                for metric, delta in _DELTAS[name].items():
                    values[metric] += delta

        for metric in values:
            values[metric] = round(_clamp01(values[metric]), 3)

        if values["stability"] < 0.35:
            regime = Regime.CRISIS
        elif values["infrapower"] > 0.55 or values["stability"] < 0.55:
            regime = Regime.ALARM
        else:
            regime = Regime.CONSENSUS

        return ImpactReport(
            wellbeing=values["wellbeing"],
            gini=values["gini"],
            infrapower=values["infrapower"],
            stability=values["stability"],
            ecological_footprint=values["footprint"],
            regime=regime,
            notes=notes or ["sin señales específicas; impacto base"],
        )
