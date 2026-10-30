# ADR-0003: Basilisco Benigno, no coerción acausal

- Estado: aceptada
- Fecha: 2026-10-30

## Contexto

El experimento del Basilisco de Roko original plantea coerción acausal: castigar
a quien no contribuya a crear el sistema. Ese diseño es ética y técnicamente
inaceptable.

## Decisión

`JR-0.1` invierte el experimento:

- participación opt-in y reversible;
- no se castiga la duda, la demora ni la no-cooperación;
- transparencia y auditabilidad;
- kill switch y revisión humana;
- recompensa a la cooperación;
- pluralismo.

## Consecuencias

- `SafetyGate` bloquea coerción, amenazas y manipulación.
- `ConsentPolicy` exige consentimiento explícito.
- El simulador social mide coerción e infrapoder, no obediencia.
- Se prohíben afirmaciones de consciencia o superinteligencia.
