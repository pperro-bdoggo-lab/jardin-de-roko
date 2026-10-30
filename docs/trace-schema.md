# Esquema de traza (`jr-0.1`)

La traza se escribe con `Trace.to_json()`: UTF-8, claves ordenadas, enums como
string y timestamps ISO-8601. Es el contrato de auditoría del vertical slice.

| Campo | Tipo | Descripción |
|---|---|---|
| `schema_version` | string | `"jr-0.1"` |
| `trace_id` | string | Identificador único de la ejecución |
| `created_at` | string | Marca temporal UTC |
| `request` | object | Prompt, id, consentimiento y metadatos |
| `safety` | object | Decisión de `SafetyGate` y flags |
| `affect` | object | `valence`, `arousal`, `tension`, `intensity`, `label` |
| `ecro` | object | Lentes y descripción |
| `complex_state` | object | `real`, `imag`, `modulus`, `phase`, `collapsed` |
| `memories` | array | Items recuperados con score |
| `deliberation` | object | Candidatos, seleccionado y notas |
| `generation` | object \| null | Texto, ruta, modelo, latencia y raw |
| `verdict` | object | Estado, allowed, razones y checks |
| `impact` | object | Métricas sociales y régimen |
| `route` | string | `stub`, `local`, `api` o `hybrid` |
| `timings` | object | Milisegundos por etapa |
| `blocked` | boolean | `true` si `SafetyGate` bloqueó |
| `error` | string \| null | Reservado para fallos controlados |

## Caso bloqueado

Cuando `blocked` es `true`:

- `generation` es `null`;
- `deliberation.candidates` está vacío;
- `impact` no se simula;
- `verdict.status` es `fail`;
- se escribe un evento `response.blocked` en el audit log.

## Ejemplo mínimo

```bash
python3 -m solaris.cli \
  --prompt "Propón una política de cuidado del agua" \
  --trace out.json
```

`out.json` es consumible por `apps/dashboard/index.html`.
