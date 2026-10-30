"""CLI de JR-0.1: prompt -> traza JSON."""

from __future__ import annotations

import argparse
from pathlib import Path

from solaris.adapters import ApiAdapter, HybridAdapter, LocalAdapter, StubAdapter
from solaris.adapters.base import ModelAdapter
from solaris.config import Settings
from solaris.errors import KillSwitchActive
from solaris.governance.audit_log import AuditLog
from solaris.governance.kill_switch import KillSwitch
from solaris.orchestrator import Orchestrator
from solaris.schemas import Request


def build_adapter(settings: Settings) -> ModelAdapter:
    if settings.model_backend == "local":
        return LocalAdapter(model_path=settings.model_path)
    if settings.model_backend == "api":
        return ApiAdapter(
            api_key=settings.api_key,
            model=settings.api_model,
            base_url=settings.api_base_url,
            provider=settings.api_provider,
        )
    if settings.model_backend == "hybrid":
        return HybridAdapter(
            local=LocalAdapter(model_path=settings.model_path),
            api=ApiAdapter(
                api_key=settings.api_key,
                model=settings.api_model,
                base_url=settings.api_base_url,
                provider=settings.api_provider,
            ),
            fallback=StubAdapter(),
        )
    return StubAdapter()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="solaris",
        description="Jardín de Roko JR-0.1: vertical slice con traza auditable.",
    )
    parser.add_argument("--prompt", required=True, help="Solicitud a procesar.")
    parser.add_argument(
        "--trace",
        default="out.json",
        help="Ruta de salida de la traza JSON (por defecto: out.json).",
    )
    parser.add_argument(
        "--audit",
        default=None,
        help="Ruta del audit log JSONL (por defecto: configuración de entorno).",
    )
    parser.add_argument(
        "--kill-switch",
        default=None,
        help="Ruta del archivo kill switch (por defecto: configuración de entorno).",
    )
    parser.add_argument("--seed", type=int, default=None, help="Semilla reproducible.")
    parser.add_argument(
        "--no-consent",
        action="store_true",
        help="Simula ausencia de consentimiento para probar el bloqueo opt-in.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprime la traza completa en stdout además de escribirla.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings.from_env()
    if args.seed is not None:
        settings.seed = args.seed

    audit_log = AuditLog(args.audit or settings.audit_path)
    kill_switch = KillSwitch(args.kill_switch or settings.kill_switch_path)
    orchestrator = Orchestrator(
        adapter=build_adapter(settings),
        audit_log=audit_log,
        kill_switch=kill_switch,
        seed=settings.seed,
    )

    request = Request(prompt=args.prompt, consent=not args.no_consent)
    try:
        response = orchestrator.run(request)
    except KillSwitchActive as exc:
        print(f"[kill-switch] {exc}")
        return 3

    trace_path = Path(args.trace)
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    trace_path.write_text(response.trace.to_json(), encoding="utf-8")

    if args.json:
        print(response.trace.to_json())
    else:
        trace = response.trace
        print(f"trace_id: {trace.trace_id}")
        print(f"seguridad: {trace.safety.status.value}")
        print(f"afecto: {trace.affect.label} (valence={trace.affect.valence})")
        print(f"ruta del modelo: {trace.route.value}")
        print(f"veredicto: {trace.verdict.status.value}")
        if trace.blocked:
            print("impacto: no simulado (solicitud bloqueada)")
        else:
            print(f"impacto: régimen={trace.impact.regime.value}")
        print(f"trace: {trace_path}")
        print("respuesta:")
        print(response.text)

    return 0 if response.verdict.allowed else 2


if __name__ == "__main__":
    raise SystemExit(main())
