## Qué cambia

<!-- Describe el cambio -->

## Cómo probarlo

- [ ] `python3 -m unittest discover -s tests -t . -v`
- [ ] `bash scripts/run_demo.sh`
- [ ] `bash scripts/check_no_secrets.sh`

## Checklist

- [ ] No incluye secretos ni datos locales.
- [ ] No rastrea `data/traces/*` ni `apps/dashboard/trace.json`.
- [ ] Mantiene la compatibilidad de la traza `jr-0.1`.
- [ ] Actualiza `docs/roadmap.md` si corresponde.
