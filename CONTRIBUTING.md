# Contribuir

## Entorno

- Python >=3.11; usa `python3`.
- Sin dependencias de runtime por defecto.
- Copia `.env.example` a `.env` solo si necesitas configuración local; no versiones `.env`.

## Antes de enviar cambios

- `python3 -m unittest discover -s tests -t . -v`
- `bash scripts/run_demo.sh`
- `bash scripts/check_no_secrets.sh`

## Reglas

- Mantén `data/` y `apps/dashboard/trace.json` fuera de los commits.
- No incluyas secretos, tokens ni rutas personales.
- Conserva la compatibilidad de la traza `jr-0.1`.
- Documenta los cambios de arquitectura en `docs/` y actualiza `docs/roadmap.md` al cerrar una semana.

## Commits y PRs

- Mensajes claros y en imperativo.
- Un PR debe explicar el cambio, cómo probarlo y qué riesgos introduce.
