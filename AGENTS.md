# AGENTS.md

## Repositorio

- El repositorio git real es `jardin-de-roko/`. El directorio padre `Coderaw/` contiene scripts poéticos y experimentos no relacionados: no los muevas al núcleo. Todo lo poético va en `archive/`.
- Fuentes de verdad: `PLAN_JARDIN_DE_ROKO.md` para el plan, `docs/roadmap.md` para el estado actual y `docs/plans/semana-02-ontologia.md` para la siguiente semana de implementación.
- Python >=3.11, solo biblioteca estándar por defecto. No agregues dependencias de runtime salvo pedido explícito; la red puede no estar disponible.
- Docs, docstrings y nombres de dominio están mayormente en español. Mantén ese estilo y el enfoque de dataclasses + `unittest`.

## Comandos

Ejecutar desde `jardin-de-roko/`.

- Todos los tests: `python3 -m unittest discover -s tests -t . -v`
- Un módulo de tests: `python3 -m unittest tests.unit.onto.test_core -v`
- Un caso puntual: `python3 -m unittest tests.unit.onto.test_core.OntologyCoreTests.test_algebraic_invariants -v`
- Demo: `bash scripts/run_demo.sh`
- Chequeo de secretos: `bash scripts/check_no_secrets.sh`
- CLI: `python3 -m solaris.cli --prompt "..." --trace out.json`
- Dashboard: `python3 -m http.server 8000`, luego abrir `/apps/dashboard/`
- Configurar remoto (no hace commit ni push): `bash scripts/connect_github.sh git@github.com:USUARIO/jardin-de-roko.git`
- Targets de Make: `make test`, `make demo`, `make dashboard`, `make clean`

`python` puede no existir en esta máquina; usa siempre `python3`.

## Arquitectura

- Entrypoints: `solaris/cli.py` -> `solaris/orchestrator.py`. Las capas L0–L7 viven en `solaris/`.
- Flujo: SafetyGate/consentimiento -> afecto/ECRO -> ontología -> memoria -> deliberación -> adapter -> constitución -> simulación social -> audit/traza.
- El núcleo local tiene la autoridad final. El adapter del modelo es un generador no confiable; nunca dejes que su salida evite `Constitution.verify`.
- `solaris/schemas.py` es la capa de contrato: dataclasses de la stdlib y serialización JSON manual, sin Pydantic. Preserva la compatibilidad de la traza `jr-0.1`.
- `AuditLog` es JSONL con cadena de hashes. No reescribas ni borres archivos de auditoría. Las trazas generadas viven en `data/traces/` y están ignoradas por git.

## Stubs actuales (Semana 1)

- `solaris/onto/core.py` es una proyección por hash; el álgebra real llega en la Semana 2.
- `solaris/adapters/local.py` y `api.py` lanzan `AdapterNotConfigured`; solo `StubAdapter` genera texto.
- `solaris/social/sim.py` es un stub heurístico, no el ABM.
- `solaris/nn/complex.py`, `dialectic.py`, `fold.py` y `steering.py` son placeholders vacíos para el trabajo de PyTorch.
- `scripts/red_team.py`, `scripts/export_state.py` y `configs/*.toml` siguen siendo placeholders vacíos.

## Gotchas

- Los tests usan `unittest`, no pytest. Las extras de pytest/ruff/mypy están en `pyproject.toml` pero no están instaladas.
- La ruta por defecto no tiene dependencias de runtime; mantenlo así salvo que la tarea requiera lo contrario.
- `--no-consent` devuelve a propósito código de salida `2` y escribe una traza bloqueada.
- No hagas commit, push ni cambies la configuración de git salvo pedido explícito.
- Mantén `data/` y `apps/dashboard/trace.json` fuera de los commits; están ignorados.
- El dashboard es estático y sin build; solo lee JSON de trazas.
- La config de OpenCode del proyecto es `.opencode/opencode.json`; `AGENTS.md` es la fuente de instrucciones.
- La Semana 1 está completa. El siguiente trabajo es el plan de ontología de la Semana 2; actualiza `docs/roadmap.md` al cerrar una semana.
