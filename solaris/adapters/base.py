"""Contrato común de adaptadores de modelo."""

from __future__ import annotations

from typing import Protocol

from solaris.schemas import Generation, SamplingParams, SteeringSpec


class ModelAdapter(Protocol):
    def generate(
        self, prompt: str, steering: SteeringSpec, params: SamplingParams
    ) -> Generation:
        ...
