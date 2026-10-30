# Contratos de módulos

| Contrato | Implementación actual | Estado | Test |
|---|---|---|---|
| `SafetyGate.check(request) -> SafetyDecision` | Heurística de coerción + consentimiento | Real | `tests/contract/test_safety_gate.py` |
| `AffectEngine.update(text) -> AffectState` | Léxico determinista | Real | `tests/unit/nn/test_affect.py` |
| `ECRO.encode(affect_state) -> ECROState` | Lentes deterministas | Real | `tests/unit/nn/test_affect.py` |
| `OntologyCore.project(context) -> ComplexState` | Proyección hash en `C` | Stub determinista | `tests/unit/onto/test_core.py` |
| `Memory.retrieve(query, affect) -> list[MemoryItem]` | Similitud de tokens + resonancia | Real, en memoria | `tests/unit/memory/test_somatic.py` |
| `Deliberator.run(context) -> DeliberationTrace` | 3 candidatos + scoring | Real | `tests/unit/nn/test_dialectic.py` |
| `ModelAdapter.generate(prompt, steering, params) -> Generation` | `StubAdapter` determinista | Stub explícito | `tests/integration/test_vertical_slice.py` |
| `SocialSim.evaluate(action) -> ImpactReport` | Heurística de impacto | Stub determinista | `tests/unit/social/test_sim.py` |
| `Constitution.verify(output, context) -> Verdict` | Checks de coerción/consciencia/secretos | Real | `tests/contract/test_constitution.py` |
| `AuditLog.append(event) -> None` | JSONL + cadena SHA-256 | Real | `tests/contract/test_audit_log.py` |
| `Orchestrator.run(request) -> Response` | Flujo completo | Real | `tests/contract/test_orchestrator.py` |
| `KillSwitch` | Archivo de presencia | Real | `tests/contract/test_orchestrator.py` |
| Dashboard | Lector estático de traza | Real, mínimo | Manual |

## Real vs. metáfora

- **Real:** reglas de seguridad, verificación, auditoría, memoria por similitud,
  scoring determinista y serialización de estado.
- **Metáfora operacionalizada:** “afecto”, “ECRO”, “negación nula” y “colapso”
  son nombres de transformaciones matemáticas o heurísticas; no afirman
  experiencia subjetiva.
- **Stub:** generación de lenguaje y simulación social portada del ABM.

Cada contrato debe conservar su test incluso cuando cambie la implementación.
