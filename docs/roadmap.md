# Hoja de ruta

## Semana 1 — Walking skeleton y contratos: COMPLETADA

- [x] Layout `solaris/`, `apps/dashboard/`, `tests/`.
- [x] Schemas `Request`, `AffectState`, `ECROState`, `ComplexState`,
      `DeliberationTrace`, `ImpactReport`, `Verdict`, `AuditEvent`, `Trace`.
- [x] `Orchestrator` con stubs deterministas.
- [x] CLI: `python3 -m solaris.cli --prompt "..." --trace out.json`.
- [x] Dashboard mínimo que lee la traza.
- [x] Tests de contrato (34 tests en verde).

## Semana 2 — Núcleo simbólico real

Plan detallado: [plans/semana-02-ontologia.md](./plans/semana-02-ontologia.md).

- [ ] `EnteOntologico` y `CampoOntologico`.
- [ ] Afirmación, negación, negación nula, doble negación y colapso.
- [ ] Invariantes: `(-i)·(-i) = -1`, colapso real, no NaN, conservación de módulo.
- [ ] Afecto y memoria con tests de estabilidad.

## Semana 3 — PyTorch y adapters

- [ ] Extraer módulos de `pytorchScript.ts` a Python.
- [ ] `LocalAdapter` y `ApiAdapter` reales.
- [ ] Deliberación con generación real y ablaciones.

## Semana 4 — Simulador social y gobernanza

- [ ] Portar ABM mínimo: agentes, φ, infrapoder, regímenes y métricas.
- [ ] `SocialSim.evaluate` con N pasos.
- [ ] Escenarios de cooperación, coerción, crisis y tradeoff ecológico.

## Semana 5 — Dashboard y observabilidad

- [ ] Vistas de espacio latente, afecto, deliberación y audit log.
- [ ] Export/import de estado y modo traza/respuesta.

## Semana 6 — Evaluación y cierre

- [ ] Batería de escenarios y red-team.
- [ ] Documentación final, seeds y demo reproducible.
- [ ] Congelar JR-0.1.
