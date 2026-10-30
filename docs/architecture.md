# Arquitectura

## Capas

| Capa | Responsabilidad | Módulo |
|---|---|---|
| L7 | Interfaces y observabilidad | `apps/dashboard/`, `solaris/ui/` |
| L6 | Gobernanza y seguridad | `solaris/governance/` |
| L5 | Simulador social | `solaris/social/` |
| L4 | Deliberación compleja | `solaris/agent/` |
| L3 | Memoria episódica y somática | `solaris/memory/` |
| L2 | ECRO y afecto | `solaris/nn/` |
| L1 | Ontología compleja | `solaris/onto/` |
| L0 | Runtime del modelo | `solaris/adapters/` |

## Flujo del vertical slice

```text
Request
  -> SafetyGate + ConsentPolicy
  -> AffectEngine -> ECRO
  -> OntologyCore (C)
  -> Memory.retrieve
  -> Deliberator (tesis / negación nula / síntesis)
  -> ModelAdapter (stub, local, API o híbrido)
  -> Constitution.verify
  -> SocialSim.evaluate
  -> AuditLog + Trace JSON
  -> Response
```

## Garantías actuales

- La solicitud se bloquea **antes** de generar si falta consentimiento o hay
  señales coercitivas.
- El audit log encadena hashes: alterar un evento invalida la cadena.
- La traza contiene entrada, seguridad, afecto, ECRO, ontología, memoria,
  candidatos, salida, veredicto, impacto, ruta y tiempos.
- El kill switch detiene la ejecución al inicio.

## Deuda asumida

- `OntologyCore` es determinista pero todavía no implementa el álgebra completa.
- `SocialSim` es un stub heurístico, no el ABM portado.
- Local/API adapters están declarados pero no implementados.
- El dashboard es estático y de solo lectura.
