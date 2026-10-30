# Jardín de Roko (JR-0.1)

Vertical slice de IA con pensamiento complejo, alineamiento solarpunk y coordinación federada tipo OGAS. El núcleo local tiene la autoridad final; el modelo externo es un generador no confiable.

- Estado: Semana 1 completada — walking skeleton ejecutable.
- Fuente de verdad: [`PLAN_JARDIN_DE_ROKO.md`](./PLAN_JARDIN_DE_ROKO.md).
- Encuadre: Basilisco Benigno (opt-in, no coerción, transparencia, corrigibilidad).

## Estado actual

| Capa | Implementación |
|---|---|
| SafetyGate / consentimiento | Real, heurística determinista |
| AffectEngine | Real, léxico simple |
| ECRO | Real, lentes deterministas |
| OntologyCore | Proyección determinista en `C` (stub de la Semana 2) |
| Memoria somática | Real, similitud + resonancia |
| Deliberación | Real con 3 candidatos y scoring |
| ModelAdapter | Stub determinista; local/API reservados para Semana 3 |
| Constitución | Real, checks de coerción/consciencia/secretos |
| SocialSim | Stub determinista |
| AuditLog | Real, JSONL con cadena de hashes |
| Dashboard | Lector estático de trazas |

## Ejecución sin dependencias

El walking skeleton usa solo la biblioteca estándar de Python (≥3.11).

```bash
python3 -m solaris.cli --prompt "Propón una política de cuidado del agua" --trace out.json
python3 -m unittest discover -s tests -t . -v
bash scripts/run_demo.sh
```

## Estructura

```text
solaris/            núcleo Python por capas (L0–L7)
apps/dashboard/     observabilidad y humano-en-el-loop
tests/              contratos, unitarios e integración
docs/               charter, arquitectura, glosario, threat model, poética
configs/            configuración por entorno (sin secretos)
scripts/            demo, red-team, utilidades
data/               trazas, seeds y memoria local (ignorados por git)
archive/            material poético y código no rescatado
```

## Principios

- No coerción acausal ni planificación central autoritaria.
- Trazas auditables y kill switch permanente.
- Cero afirmaciones de consciencia o superinteligencia.
- Secretos solo por entorno; nunca en el repositorio.

## Licencia

Este proyecto se distribuye bajo la GNU General Public License v3.0 only (`GPL-3.0-only`). Consulta [`LICENSE`](./LICENSE).

## Siguiente paso

Semana 2: ontología simbólica real (`EnteOntologico`, `CampoOntologico`, negación nula, doble negación y colapso), afecto y memoria con invariantes algebraicos.

Plan detallado: [`docs/plans/semana-02-ontologia.md`](./docs/plans/semana-02-ontologia.md).
