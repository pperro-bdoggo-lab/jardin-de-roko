# Dashboard JR-0.1

Lector estático de trazas. No requiere build ni dependencias.

## Uso

Opción directa:

1. Ejecuta `bash scripts/run_demo.sh`.
2. Abre `apps/dashboard/index.html` en el navegador.
3. Carga `data/traces/demo.json` con el selector.

Opción servidor local (recomendada):

```bash
python3 -m http.server 8000
```

Abre `http://localhost:8000/apps/dashboard/`. El botón **Cargar trace.json**
busca `apps/dashboard/trace.json`; `run_demo.sh` copia ahí la última traza.

## Qué muestra

- solicitud, ruta del modelo y estado de bloqueo;
- decisión de `SafetyGate`;
- estado afectivo y lentes ECRO;
- estado ontológico en `C`;
- candidatos de deliberación y seleccionado;
- veredicto constitucional;
- métricas de impacto social;
- memoria recuperada y tiempos por etapa.

El dashboard es solo observabilidad. No ejecuta el núcleo ni toma decisiones.
