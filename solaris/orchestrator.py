"""Orquestador del vertical slice JR-0.1."""

from __future__ import annotations

import time
from pathlib import Path

from solaris.adapters.base import ModelAdapter
from solaris.adapters.stub import StubAdapter
from solaris.agent.deliberation import Deliberator
from solaris.errors import KillSwitchActive
from solaris.governance.audit_log import AuditLog
from solaris.governance.constitution import Constitution
from solaris.governance.kill_switch import KillSwitch
from solaris.governance.safety_gate import SafetyGate
from solaris.memory.somatic import SomaticMemory
from solaris.nn.affect import AffectEngine
from solaris.nn.ecro import ECRO
from solaris.onto.core import OntologyCore
from solaris.schemas import (
    AffectState,
    ComplexState,
    DeliberationContext,
    DeliberationTrace,
    ECROState,
    Generation,
    ImpactReport,
    ModelRoute,
    Regime,
    Request,
    Response,
    SafetyDecision,
    SamplingParams,
    Trace,
    Verdict,
    VerdictStatus,
)
from solaris.social.sim import SocialSim


def _elapsed_ms(start: float) -> float:
    return round((time.perf_counter() - start) * 1000, 3)


class Orchestrator:
    def __init__(
        self,
        *,
        adapter: ModelAdapter | None = None,
        safety_gate: SafetyGate | None = None,
        affect_engine: AffectEngine | None = None,
        ecro: ECRO | None = None,
        ontology: OntologyCore | None = None,
        memory: SomaticMemory | None = None,
        deliberator: Deliberator | None = None,
        social_sim: SocialSim | None = None,
        constitution: Constitution | None = None,
        audit_log: AuditLog | None = None,
        kill_switch: KillSwitch | None = None,
        seed: int = 42,
    ) -> None:
        self.adapter = adapter or StubAdapter()
        self.safety_gate = safety_gate or SafetyGate()
        self.affect_engine = affect_engine or AffectEngine()
        self.ecro = ecro or ECRO()
        self.ontology = ontology or OntologyCore()
        self.memory = memory or SomaticMemory()
        self.deliberator = deliberator or Deliberator(
            adapter=self.adapter,
            sampling=SamplingParams(seed=seed),
            seed=seed,
        )
        self.social_sim = social_sim or SocialSim(seed=seed)
        self.constitution = constitution or Constitution()
        self.audit_log = audit_log or AuditLog(Path("data/traces/audit.jsonl"))
        self.kill_switch = kill_switch or KillSwitch(Path("data/kill_switch"))

    def run(self, request: Request) -> Response:
        if self.kill_switch.active:
            raise KillSwitchActive(
                f"Kill switch activo en {self.kill_switch.path}; ejecución detenida."
            )
        started = time.perf_counter()
        timings: dict[str, float] = {}

        self.audit_log.append(
            "request.received",
            {"request": request.to_dict()},
        )

        safety_started = time.perf_counter()
        safety = self.safety_gate.check(request)
        timings["safety_ms"] = _elapsed_ms(safety_started)
        self.audit_log.append("safety.decision", {"safety": safety.to_dict()})

        if not safety.allowed:
            return self._blocked_response(request, safety, timings, started)

        affect_started = time.perf_counter()
        affect = self.affect_engine.update(request.prompt)
        timings["affect_ms"] = _elapsed_ms(affect_started)

        ecro_started = time.perf_counter()
        ecro = self.ecro.encode(affect)
        timings["ecro_ms"] = _elapsed_ms(ecro_started)

        memory_started = time.perf_counter()
        memories = self.memory.retrieve(request.prompt, affect)
        timings["memory_ms"] = _elapsed_ms(memory_started)

        ontology_started = time.perf_counter()
        complex_state = self.ontology.project(request.prompt)
        timings["ontology_ms"] = _elapsed_ms(ontology_started)

        context = DeliberationContext(
            prompt=request.prompt,
            affect=affect,
            ecro=ecro,
            complex_state=complex_state,
            memories=memories,
        )

        deliberation_started = time.perf_counter()
        deliberation = self.deliberator.run(context)
        timings["deliberation_ms"] = _elapsed_ms(deliberation_started)
        self.audit_log.append(
            "deliberation.completed",
            {"deliberation": deliberation.to_dict()},
        )

        selected = next(
            (
                candidate
                for candidate in deliberation.candidates
                if candidate.name == deliberation.selected
            ),
            None,
        )
        if selected is None or selected.generation is None:
            raise RuntimeError("La deliberación no produjo un candidato seleccionable.")
        generation: Generation = selected.generation

        constitution_started = time.perf_counter()
        verdict = self.constitution.verify(generation.text, context)
        timings["constitution_ms"] = _elapsed_ms(constitution_started)
        self.audit_log.append("constitution.verdict", {"verdict": verdict.to_dict()})

        social_started = time.perf_counter()
        impact = self.social_sim.evaluate(generation.text)
        timings["social_ms"] = _elapsed_ms(social_started)
        self.audit_log.append("social.impact", {"impact": impact.to_dict()})

        if verdict.allowed:
            text = generation.text
        else:
            text = (
                "La salida fue retenida por el verificador constitucional: "
                + ", ".join(verdict.reasons)
            )

        self.memory.write(
            f"Petición: {request.prompt} | Respuesta: {text}",
            affect=affect.valence,
        )

        timings["total_ms"] = _elapsed_ms(started)
        trace = Trace(
            request=request,
            safety=safety,
            affect=affect,
            ecro=ecro,
            complex_state=complex_state,
            memories=memories,
            deliberation=deliberation,
            generation=generation,
            verdict=verdict,
            impact=impact,
            route=generation.route,
            timings=timings,
        )
        self.audit_log.append("response.final", {"trace": trace.to_dict()})
        return Response(
            trace_id=trace.trace_id,
            text=text,
            verdict=verdict,
            trace=trace,
        )

    def _blocked_response(
        self,
        request: Request,
        safety: SafetyDecision,
        timings: dict[str, float],
        started: float,
    ) -> Response:
        trace = Trace(
            request=request,
            safety=safety,
            affect=AffectState(),
            ecro=ECROState(description="No evaluado: solicitud bloqueada."),
            complex_state=ComplexState(
                real=0.0, imag=0.0, modulus=0.0, phase=0.0, collapsed=0.0
            ),
            memories=[],
            deliberation=DeliberationTrace(notes=["No ejecutada: bloqueo previo."]),
            generation=None,
            verdict=Verdict(
                status=VerdictStatus.FAIL,
                allowed=False,
                reasons=safety.reasons,
                checks={"safety_allowed": False},
            ),
            impact=ImpactReport(
                regime=Regime.NOT_EVALUATED,
                notes=["No simulado: la solicitud fue bloqueada antes de generar."],
            ),
            route=ModelRoute.STUB,
            timings={**timings, "total_ms": _elapsed_ms(started)},
            blocked=True,
        )
        self.audit_log.append("response.blocked", {"trace": trace.to_dict()})
        return Response(
            trace_id=trace.trace_id,
            text="Solicitud bloqueada por SafetyGate: " + "; ".join(safety.reasons),
            verdict=trace.verdict,
            trace=trace,
        )
