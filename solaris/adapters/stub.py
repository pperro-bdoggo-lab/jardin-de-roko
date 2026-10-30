"""Generador determinista para el walking skeleton. No es un LLM."""

from __future__ import annotations

import re
from dataclasses import dataclass

from solaris.schemas import Generation, ModelRoute, SamplingParams, SteeringSpec

_TOPIC_RE = re.compile(r"Tema:\s*(.+)", re.IGNORECASE)


def _topic(prompt: str) -> str:
    match = _TOPIC_RE.search(prompt)
    if match:
        return match.group(1).strip().splitlines()[0]
    return prompt.strip().splitlines()[0] if prompt.strip() else "el problema planteado"


@dataclass
class StubAdapter:
    model: str = "stub-deterministic"

    def generate(
        self, prompt: str, steering: SteeringSpec, params: SamplingParams
    ) -> Generation:
        topic = _topic(prompt)
        mode = steering.direction or "thesis"
        if mode == "null_negation":
            text = (
                f"Suspensión de la afirmación inicial sobre «{topic}»: antes de "
                "decidir, conviene explicitar supuestos, afectados y límites "
                "ecológicos, sin imponer una única cosmovisión."
            )
        elif mode == "synthesis":
            text = (
                f"Síntesis federada sobre «{topic}»: combinar cuidado material, "
                "cooperación voluntaria, verificación auditable y límites "
                "ecológicos, manteniendo revisión humana y reversibilidad."
            )
        else:
            text = (
                f"Propuesta inicial sobre «{topic}»: definir objetivos comunes, "
                "repartir autonomía local y medir bienestar, desigualdad y huella "
                "ecológica antes de escalar la medida."
            )
        return Generation(
            text=text,
            route=ModelRoute.STUB,
            model=self.model,
            latency_ms=0.0,
            raw={
                "mode": mode,
                "temperature": params.temperature,
                "top_p": params.top_p,
                "seed": params.seed,
                "strength": steering.strength,
            },
        )
