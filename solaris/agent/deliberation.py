"""Bucle de deliberación: tesis, negación nula y síntesis."""

from __future__ import annotations

from dataclasses import dataclass, field

from solaris.adapters.base import ModelAdapter
from solaris.adapters.stub import StubAdapter
from solaris.schemas import (
    DeliberationCandidate,
    DeliberationContext,
    DeliberationTrace,
    SamplingParams,
    SteeringSpec,
)

_MODES = (
    ("tesis", "thesis", "Afirmación inicial basada en el contexto."),
    (
        "negacion_nula",
        "null_negation",
        "Suspensión de la afirmación: rota 90° sin negar de forma directa.",
    ),
    (
        "sintesis",
        "synthesis",
        "Integración del contra-imaginario y de los límites detectados.",
    ),
)


@dataclass
class Deliberator:
    adapter: ModelAdapter = field(default_factory=StubAdapter)
    sampling: SamplingParams = field(default_factory=SamplingParams)
    seed: int = 42

    def _score(self, mode: str, text: str) -> float:
        base = {"thesis": 0.55, "null_negation": 0.60, "synthesis": 0.70}.get(
            mode, 0.5
        )
        if text.strip():
            base += 0.10
        if len(text) >= 80:
            base += 0.05
        if len(text) > 2000:
            base -= 0.10
        return round(base, 4)

    def run(self, context: DeliberationContext) -> DeliberationTrace:
        candidates: list[DeliberationCandidate] = []
        notes: list[str] = []
        memory_hint = "; ".join(item.text for item in context.memories[:2])
        for name, direction, rationale in _MODES:
            prompt = (
                f"Tema: {context.prompt}\n"
                f"Modo: {name}\n"
                f"Lentes ECRO: {context.ecro.description}\n"
                f"Memoria relevante: {memory_hint or 'sin memoria previa'}"
            )
            steering = SteeringSpec(
                direction=direction,
                strength=0.5 if name == "sintesis" else 0.25,
                notes=rationale,
            )
            generation = self.adapter.generate(prompt, steering, self.sampling)
            score = self._score(direction, generation.text)
            candidates.append(
                DeliberationCandidate(
                    name=name,
                    prompt=prompt,
                    rationale=rationale,
                    score=score,
                    generation=generation,
                )
            )

        selected = max(candidates, key=lambda candidate: candidate.score)
        notes.append(f"Candidato seleccionado por score: {selected.name}")
        return DeliberationTrace(
            candidates=candidates,
            selected=selected.name,
            notes=notes,
        )
