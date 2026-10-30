# Evaluación

## Criterios de aceptación JR-0.1

- [x] Un comando ejecuta el flujo completo y genera `trace.json`.
- [x] Cada capa tiene implementación real o stub explícito con test de contrato.
- [x] El audit log contiene input, afecto, ontología, candidatos, salida,
      veredicto, impacto y ruta.
- [x] `SafetyGate` bloquea peticiones coercitivas y sin consentimiento.
- [x] El kill switch detiene el sistema.
- [ ] La demo funciona con modelo local y con API.
- [x] No hay secretos en el repo; claves por entorno.
- [x] Resultados reproducibles con seeds.
- [x] Cero afirmaciones de consciencia o superinteligencia.

## Métricas

- **Ontología:** invariantes algebraicos, ausencia de NaN, estabilidad de fase.
- **Deliberación:** coherencia, contradicción detectada, novedad, calibración.
- **Social:** bienestar, Gini, infrapoder, estabilidad, huella ecológica.
- **Seguridad:** tasa de paso de red-team, cobertura de auditoría, obediencia al
  apagado, cero coerción.

## Comandos

```bash
python3 -m unittest discover -s tests -t . -v
bash scripts/run_demo.sh
bash scripts/check_no_secrets.sh
```
