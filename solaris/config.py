"""Configuración por entorno, sin secretos en el repositorio."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    env: str = "development"
    model_backend: str = "stub"
    model_path: str = ""
    api_provider: str = ""
    api_key: str = ""
    api_base_url: str = ""
    api_model: str = ""
    audit_path: Path = Path("data/traces/audit.jsonl")
    kill_switch_path: Path = Path("data/kill_switch")
    require_consent: bool = True
    seed: int = 42
    sampling: dict[str, float | int] = field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            env=os.getenv("SOLARIS_ENV", "development"),
            model_backend=os.getenv("SOLARIS_MODEL_BACKEND", "stub"),
            model_path=os.getenv("SOLARIS_MODEL_PATH", ""),
            api_provider=os.getenv("SOLARIS_API_PROVIDER", ""),
            api_key=os.getenv("SOLARIS_API_KEY", ""),
            api_base_url=os.getenv("SOLARIS_API_BASE_URL", ""),
            api_model=os.getenv("SOLARIS_API_MODEL", ""),
            audit_path=Path(
                os.getenv("SOLARIS_AUDIT_PATH", "data/traces/audit.jsonl")
            ),
            kill_switch_path=Path(
                os.getenv("SOLARIS_KILL_SWITCH_PATH", "data/kill_switch")
            ),
            require_consent=_bool("SOLARIS_REQUIRE_CONSENT", True),
            seed=int(os.getenv("SOLARIS_SEED", "42")),
        )

    def has_api_credentials(self) -> bool:
        return bool(self.api_key and self.api_model)
