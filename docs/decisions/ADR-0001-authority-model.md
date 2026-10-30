# ADR-0001: el núcleo local tiene la autoridad final

- Estado: aceptada
- Fecha: 2026-10-30

## Contexto

El vertical slice puede usar un modelo local open-weight o una API externa. Un
LLM generativo no es una autoridad moral ni un verificador confiable.

## Decisión

El modelo externo es un **generador no confiable**. `Constitution`,
`SafetyGate`, `OntologyCore` y `SocialSim` pertenecen al núcleo local y pueden
retener, bloquear o rechazar cualquier salida.

## Consecuencias

- Toda salida pasa por verificación constitucional.
- La traza registra la ruta del modelo usada.
- Las rutas local/API comparten el mismo contrato.
- El sistema no delega la decisión final al proveedor.
