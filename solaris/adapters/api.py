"""Adaptador de API externa (Semana 3). El generador nunca es autoridad final."""

from __future__ import annotations

from dataclasses import dataclass

from solaris.errors import AdapterNotConfigured
from solaris.schemas import Generation, SamplingParams, SteeringSpec


@dataclass
class ApiAdapter:
    api_key: str = ""
    model: str = ""
    base_url: str = ""
    provider: str = ""

    def generate(
        self, prompt: str, steering: SteeringSpec, params: SamplingParams
    ) -> Generation:
        if not self.api_key or not self.model:
            raise AdapterNotConfigured(
                "ApiAdapter requiere API key y modelo configurados por entorno."
            )
        raise AdapterNotConfigured(
            "ApiAdapter aún no implementado; previsto para la Semana 3."
        )
