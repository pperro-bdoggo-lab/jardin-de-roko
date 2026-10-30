"""Contratos de datos de JR-0.1.

Schemas deliberadamente basados en la biblioteca estándar para que el walking
skeleton sea ejecutable sin dependencias externas. La migración a Pydantic (si
aporta validación/JSON Schema) queda para un sprint posterior.
"""

from __future__ import annotations

import json
import math
import uuid
from dataclasses import dataclass, field, fields, is_dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping

SCHEMA_VERSION = "jr-0.1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def to_dict(value: Any) -> Any:
    """Convierte recursivamente schemas, enums y contenedores a JSON puro."""
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {item.name: to_dict(getattr(value, item.name)) for item in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): to_dict(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_dict(item) for item in value]
    if isinstance(value, datetime):
        return value.isoformat()
    return value


class JsonModel:
    def to_dict(self) -> dict[str, Any]:
        return to_dict(self)

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(
            self.to_dict(), ensure_ascii=False, indent=indent, sort_keys=True
        )


class SafetyStatus(str, Enum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs_review"


class VerdictStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class ModelRoute(str, Enum):
    STUB = "stub"
    LOCAL = "local"
    API = "api"
    HYBRID = "hybrid"


class Regime(str, Enum):
    CONSENSUS = "consensus"
    ALARM = "alarm"
    CRISIS = "crisis"
    NOT_EVALUATED = "not_evaluated"


class MemoryKind(str, Enum):
    EPISODIC = "episodic"
    SOMATIC = "somatic"


@dataclass
class SamplingParams(JsonModel):
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 512
    seed: int = 42

    def __post_init__(self) -> None:
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError("temperature debe estar entre 0 y 2")
        if not 0.0 <= self.top_p <= 1.0:
            raise ValueError("top_p debe estar entre 0 y 1")
        if self.max_tokens <= 0:
            raise ValueError("max_tokens debe ser positivo")


@dataclass
class SteeringSpec(JsonModel):
    direction: str | None = None
    strength: float = 0.0
    notes: str = ""

    def __post_init__(self) -> None:
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("strength debe estar entre 0 y 1")


@dataclass
class Request(JsonModel):
    prompt: str
    request_id: str = field(default_factory=lambda: new_id("req"))
    created_at: str = field(default_factory=utc_now)
    consent: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.prompt or not self.prompt.strip():
            raise ValueError("prompt no puede estar vacío")
        if len(self.prompt) > 20_000:
            raise ValueError("prompt excede el límite de 20000 caracteres")


@dataclass
class SafetyDecision(JsonModel):
    allowed: bool
    status: SafetyStatus = SafetyStatus.ALLOWED
    reasons: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    requires_human_review: bool = False


@dataclass
class AffectState(JsonModel):
    valence: float = 0.0
    arousal: float = 0.0
    tension: float = 0.0
    intensity: float = 0.0
    label: str = "neutro"

    def __post_init__(self) -> None:
        for name in ("valence", "arousal", "tension", "intensity"):
            value = getattr(self, name)
            if not math.isfinite(value):
                raise ValueError(f"{name} debe ser finito")
        if not -1.0 <= self.valence <= 1.0:
            raise ValueError("valence debe estar entre -1 y 1")
        for name in ("arousal", "tension", "intensity"):
            if not 0.0 <= getattr(self, name) <= 1.0:
                raise ValueError(f"{name} debe estar entre 0 y 1")


@dataclass
class ECROState(JsonModel):
    lenses: dict[str, float] = field(default_factory=dict)
    description: str = ""

    def __post_init__(self) -> None:
        for name, value in self.lenses.items():
            if not math.isfinite(value):
                raise ValueError(f"lente {name} debe ser finito")


@dataclass
class ComplexState(JsonModel):
    real: float
    imag: float
    modulus: float
    phase: float
    collapsed: float
    is_collapsed: bool = False


@dataclass
class MemoryItem(JsonModel):
    text: str
    kind: MemoryKind = MemoryKind.EPISODIC
    affect: float = 0.0
    score: float = 0.0
    item_id: str = field(default_factory=lambda: new_id("mem"))
    created_at: str = field(default_factory=utc_now)


@dataclass
class Generation(JsonModel):
    text: str
    route: ModelRoute = ModelRoute.STUB
    model: str = "stub"
    latency_ms: float = 0.0
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class DeliberationCandidate(JsonModel):
    name: str
    prompt: str
    rationale: str
    score: float
    generation: Generation | None = None


@dataclass
class DeliberationTrace(JsonModel):
    candidates: list[DeliberationCandidate] = field(default_factory=list)
    selected: str | None = None
    notes: list[str] = field(default_factory=list)


@dataclass
class DeliberationContext(JsonModel):
    prompt: str
    affect: AffectState
    ecro: ECROState
    complex_state: ComplexState
    memories: list[MemoryItem] = field(default_factory=list)


@dataclass
class ImpactReport(JsonModel):
    wellbeing: float = 0.0
    gini: float = 0.0
    infrapower: float = 0.0
    stability: float = 0.0
    ecological_footprint: float = 0.0
    regime: Regime = Regime.CONSENSUS
    notes: list[str] = field(default_factory=list)


@dataclass
class Verdict(JsonModel):
    status: VerdictStatus
    allowed: bool
    reasons: list[str] = field(default_factory=list)
    checks: dict[str, bool] = field(default_factory=dict)


@dataclass
class AuditEvent(JsonModel):
    kind: str
    payload: dict[str, Any]
    event_id: str = field(default_factory=lambda: new_id("evt"))
    timestamp: str = field(default_factory=utc_now)
    prev_hash: str = "GENESIS"
    hash: str = ""


@dataclass
class Trace(JsonModel):
    request: Request
    safety: SafetyDecision
    affect: AffectState
    ecro: ECROState
    complex_state: ComplexState
    memories: list[MemoryItem]
    deliberation: DeliberationTrace
    generation: Generation | None
    verdict: Verdict
    impact: ImpactReport
    route: ModelRoute
    timings: dict[str, float] = field(default_factory=dict)
    trace_id: str = field(default_factory=lambda: new_id("trace"))
    schema_version: str = SCHEMA_VERSION
    created_at: str = field(default_factory=utc_now)
    blocked: bool = False
    error: str | None = None


@dataclass
class Response(JsonModel):
    trace_id: str
    text: str
    verdict: Verdict
    trace: Trace
