"""Adapter híbrido: intenta local, luego API y, si no hay nada, fallback explícito."""

from __future__ import annotations

from dataclasses import dataclass

from solaris.adapters.base import ModelAdapter
from solaris.errors import AdapterError
from solaris.schemas import Generation, SamplingParams, SteeringSpec


@dataclass
class HybridAdapter:
    local: ModelAdapter | None = None
    api: ModelAdapter | None = None
    fallback: ModelAdapter | None = None

    def generate(
        self, prompt: str, steering: SteeringSpec, params: SamplingParams
    ) -> Generation:
        failures: list[str] = []
        for name, adapter in (("local", self.local), ("api", self.api)):
            if adapter is None:
                continue
            try:
                generation = adapter.generate(prompt, steering, params)
            except AdapterError as exc:
                failures.append(f"{name}: {exc}")
                continue
            generation.raw = {**generation.raw, "hybrid_failures": failures}
            return generation

        if self.fallback is not None:
            generation = self.fallback.generate(prompt, steering, params)
            generation.raw = {**generation.raw, "hybrid_failures": failures}
            return generation

        raise AdapterError("HybridAdapter sin adaptadores disponibles: " + "; ".join(failures))
