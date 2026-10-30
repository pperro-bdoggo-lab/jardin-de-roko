"""Adaptador local (Semana 3). Hoy solo valida configuración."""

from __future__ import annotations

from dataclasses import dataclass

from solaris.errors import AdapterNotConfigured
from solaris.schemas import Generation, SamplingParams, SteeringSpec


@dataclass
class LocalAdapter:
    model_path: str = ""
    model_name: str = "local"

    def generate(
        self, prompt: str, steering: SteeringSpec, params: SamplingParams
    ) -> Generation:
        if not self.model_path:
            raise AdapterNotConfigured(
                "LocalAdapter requiere SOLARIS_MODEL_PATH o un modelo open-weight."
            )
        raise AdapterNotConfigured(
            "LocalAdapter aún no implementado; previsto para la Semana 3."
        )
