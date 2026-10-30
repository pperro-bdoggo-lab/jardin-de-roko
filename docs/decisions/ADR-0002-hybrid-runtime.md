# ADR-0002: runtime híbrido con degradación explícita

- Estado: aceptada
- Fecha: 2026-10-30

## Contexto

No todos los entornos tienen hardware para un modelo local, y depender siempre
de una API externa introduce costo, latencia y dependencia de proveedor.

## Decisión

`ModelAdapter` es un protocolo común. Se prevén tres implementaciones:

1. `LocalAdapter` (prioritario).
2. `ApiAdapter` (fallback externo).
3. `HybridAdapter` (prueba local, luego API, y registra la ruta).

Durante la Semana 1 el único adaptador funcional es `StubAdapter`, determinista
y sin red, para que el vertical slice sea reproducible.

## Consecuencias

- El contrato no cambia entre rutas.
- El steering por activaciones y el steering por prompt no se consideran
  equivalentes; cualquier degradación debe documentarse.
- El stub debe eliminarse o aislarse en producción.
