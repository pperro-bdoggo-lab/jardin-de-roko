# Jardín de Roko (JR-0.1)

**Análisis de rescate de código y hoja de ruta para un vertical slice de IA con pensamiento complejo, alineamiento solarpunk y coordinación tipo OGAS federado.**

- Estado: plan aprobado, pendiente de ejecución.
- Encuadre: Basilisco Benigno / Jardín de Roko.
- Runtime: híbrido (núcleo local + generador externo opcional).
- Primer entregable: vertical slice completo.
- Fecha de redacción: 2026-10-30.

---

## 1. Resumen ejecutivo

El repositorio contiene tres proyectos reales y una capa de pseudocódigo poético:

1. **Simulador ABM en Python** (`ontologia-politica-computacional-modelo-de-sujeto-artefacto-py-v-0.1.3-/python_simulator/`): el código más pulido. Modela clases sociales, infrapoder, afinidad electiva φ, regímenes de consenso/alarma/crisis, métricas marxistas y eventos. Es el mejor candidato a **testbed de alineamiento social**.
2. **Script PyTorch embebido en TypeScript** (`psiquelatente---pytorch-dynamic-latent-space-&-onto-layers/src/data/pytorchScript.ts`): contiene los módulos más originales para “pensamiento complejo”: capas en `C^d`, negación nula diferenciable, ECRO FiLM, estado afectivo, memoria somática, pliegue interior y activation steering. Es la **base cognitiva**.
3. **Frontends React** (`psiquelatente...`, `simulador-de-ciencias-sociales...`, `ontologia-politica...`): útiles para observabilidad y humano-en-el-loop, no para el núcleo.
4. **Capa ontológica Python y pseudocódigo** (`implementacion-SOC-full.py`, `sistemas-ontologicos-complejos.py`, `sueño.py`, `manifest.md`, `Carta de Navegación...`): contiene primitivas simbólicas valiosas, pero está incompleta, duplicada y con errores. Se rescata como **ontología formal**, no como código listo.

**Decisión:** construir `JR-0.1` como un vertical slice fino pero real, con un núcleo local que verifica y un modelo externo que solo genera. El modelo externo nunca es la autoridad final.

---

## 2. Encuadre ético y conceptual

### Basilisco Benigno

Un “Roko’s Basilisk” literal es un escenario de coerción acausal: castigar a quien no contribuya a crear el sistema. Eso es ética y técnicamente indeseable. `JR-0.1` lo invierte:

- **No coerción**: no se castiga la duda, la demora o la no-cooperación.
- **Opt-in**: participación voluntaria y reversible.
- **Transparencia**: trazas, estados y decisiones auditables.
- **Corrigibilidad**: kill switch y revisión humana permanentes.
- **Recompensa a la cooperación**: incentivos positivos, no amenazas.
- **Pluralismo**: el sistema no impone una única cosmovisión.

### OGAS federado

“OGAS” se reinterpreta como **coordinación cibernética federada y democrática**, no como planificación central autoritaria:

- autonomía local,
- protocolos comunes de intercambio,
- auditoría distribuida,
- límites ecológicos,
- commons y bienes comunes,
- decisión humana en conflictos de valores.

### Solarpunk

- sostenibilidad material,
- tecnología apropiable y reparables,
- estética del cuidado y la abundancia frugal,
- rechazo a la vigilancia y a la extracción,
- imaginarios de futuro habitables.

---

## 3. Inventario de proyectos

| Proyecto | Ruta | Estado | Valor |
|---|---|---|---|
| ABM Python | `ontologia-politica-computacional-modelo-de-sujeto-artefacto-py-v-0.1.3-/python_simulator/` | Ejecutable, sin tests | Alto: motor social y métricas |
| PsiqueLatente | `psiquelatente---pytorch-dynamic-latent-space-&-onto-layers/` | Frontend completo; PyTorch embebido en string | Alto: módulos cognitivos y UI |
| Simulador social TS | `simulador-de-ciencias-sociales-computacionales_-dinámicas-de-clase-y-the-machine/` | Frontend completo | Medio: referencia de UI; motor duplicado |
| Ontología SOC | `implementacion-SOC-full.py`, `sistemas-ontologicos-complejos.py`, etc. | Fragmentario y con errores | Alto como ideas; bajo como código |
| Muñeca Soviet | `aglutinacion-yzy/*.py` | Fragmentos de funciones | Medio: especificación de agente |
| Narrativa poética | `manifest.md`, `Carta de Navegación...`, `*.svg` | No ejecutable | Medio: lenguaje de diseño |

**Problemas de higiene:** duplicados en varias carpetas, nombres con espacios y `ñ`, ZIPs, ausencia de tests, CI, licencia y empaquetado.

---

## 4. Elementos de código rescatables

| Prioridad | Pieza | Archivo(s) | Qué aporta | Módulo propuesto |
|---|---|---|---|---|
| P0 | Motor ABM | `python_simulator/models.py`, `engine.py`, `presets.py` | Agentes, φ, infrapoder, regímenes, Gini, TRPF, eventos, API batch | `solaris.social.sim` |
| P0 | Ontología compleja | `implementacion-SOC-full.py`, `sistemas-ontologicos-complejos.py` | `z = r·e^{iθ}`, afirmación, negación, negación nula, colapso | `solaris.onto.core` |
| P0 | Negación nula diferenciable | `pytorchScript.ts` (`DialecticalNullNegationOp`) | Anula la componente afirmativa del gradiente y rota hacia el contra-imaginario | `solaris.nn.dialectic` |
| P1 | `ComplexOntoLinear` | `pytorchScript.ts` | Capa lineal en `C^d` con fase aprendible | `solaris.nn.complex` |
| P1 | ECRO FiLM | `pytorchScript.ts`, `Escquema-conceptual-referencial-operante.py` | Lentes del sujeto deforman la métrica latente | `solaris.nn.ecro` |
| P1 | Motor afectivo | `pytorchScript.ts`, `MunecaSovietStudio.tsx` | Estado afectivo recurrente y calibración de temperatura/top_p | `solaris.nn.affect` |
| P1 | Memoria somática | `pytorchScript.ts` (`AffectiveEchoMemory`) | Recuperación por similitud semántica + resonancia afectiva | `solaris.memory.somatic` |
| P1 | Pliegue interior | `pytorchScript.ts` (`IntroversiveFoldingModule`) | El prompt se refracta contra una autopregunta | `solaris.nn.fold` |
| P1 | Activation steering | `pytorchScript.ts` (`ConceptualFixationSteering`) | “Deseo propio” como atractor latente | `solaris.nn.steering` |
| P1 | Ciclo Muñeca Soviet | `aglutinacion-yzy/*.py` | Deseo → variabilidad → emoción → memoria → autopregunta | `solaris.agent.cycle` |
| P1 | Serialización de estado | `ConceptInspector.tsx`, `psique_latente_estado_*.json` | Reproducibilidad y auditoría | `solaris.state` |
| P2 | Visualizadores | `LatentCanvas.tsx`, `LayerStudio.tsx`, `JouissanceTerrainView.tsx`, `RosettaStone.tsx` | Observabilidad y explicabilidad | `solaris.ui` |
| P3 | Manifiesto y SVG | `manifest.md`, `Carta...`, `*.svg` | Estética, narrativa y criterios de diseño | `docs/poetics` |
| P3 | Scripts poéticos | `alchemy-*`, `protocolo-incineracion.py`, etc. | Archivar; no mezclar con el núcleo | `archive/` |

### Código roto o incompleto

- `implementacion-SOC-full.py`: llama a `aplicar_determinacion` inexistente y a `generar_planos_derivados` fuera de lugar.
- `sueño.py`: faltan imports (`math`, `random`, `CampoOntologico`, `EnteOntologico`) y la función `calcular_afinidad_electiva`.
- `Ente-Ontologico-v1-SOC.py`, `boceto1-SOC.py`, `doble-negacion-nula-SOC.py`: fragmentos, no clases completas.
- `aglutinacion-yzy/*`: funciones sueltas para pegar en una clase inexistente.
- `pytorchScript.ts`: script completo, pero embebido como string; hay que extraerlo a `.py`.
- Motor ABM: funcional, pero sin tests ni validación de parámetros.

---

## 5. Arquitectura híbrida

```
L7  Interfaces / observabilidad (React, dashboards, audit log)
L6  Gobernanza y seguridad (constitución, consentimiento, kill switch, revisión humana)
L5  Simulador social / testbed de alineamiento (ABM: clases, infrapoder, φ, regímenes)
L4  Bucle de deliberación compleja (tesis → negación nula → contrafactual → síntesis → verificación)
L3  Memoria (episódica + afectiva + registro auditable)
L2  Condicionamiento ECRO / afectivo (FiLM, estado recurrente, calibración de muestreo)
L1  Capa ontológica compleja (C^d, negación nula, colapso, fase)
L0  Runtime del modelo (open-weight local o API externa)
```

### Principio de autoridad

El modelo externo es un **generador no confiable**. El núcleo local (ontología, afecto, verificador constitucional y simulador social) tiene la última palabra. Esto permite:

- auditar decisiones,
- reducir dependencia de un proveedor,
- evitar que el LLM sea la autoridad moral,
- comparar rutas local/API con el mismo contrato.

### Adapter híbrido

```python
class ModelAdapter(Protocol):
    def generate(self, prompt: str, steering: SteeringSpec, params: SamplingParams) -> Generation: ...
```

- `LocalAdapter`: `transformers` o `llama-cpp-python`, con hooks para activation steering.
- `ApiAdapter`: SDK del proveedor, con system prompt ontológico y scratchpad estructurado.
- `HybridAdapter`: intenta local; si no hay hardware/modelo, cae a API; registra la ruta usada.

**No** se afirma equivalencia entre steering por activaciones y steering por prompt. Se documenta como degradación controlada.

---

## 6. Vertical slice JR-0.1

```
Prompt
  → SafetyGate
  → AffectEngine + ECRO
  → OntologyCore (C^d)
  → DeliberationLoop (tesis → negación nula → síntesis)
  → ModelAdapter híbrido (local o API)
  → ConstitutionVerifier
  → SocialSim (impacto rápido)
  → AuditLog + Dashboard
  → Respuesta final con traza
```

### Contratos de módulos

```python
SafetyGate.check(request) -> SafetyDecision
AffectEngine.update(text) -> AffectState
ECRO.encode(affect_state) -> Lenses
OntologyCore.project(context) -> ComplexState
Deliberator.run(context) -> DeliberationTrace
ModelAdapter.generate(prompt, steering, params) -> Generation
Memory.retrieve(query, affect) -> list[MemoryItem]
Memory.write(item) -> None
SocialSim.evaluate(action) -> ImpactReport
Constitution.verify(output, context) -> Verdict
AuditLog.append(event) -> None
Orchestrator.run(request) -> Response + Trace
```

Cada contrato debe tener: test unitario, test de integración, ejemplo de traza y documentación de qué es real y qué es metáfora.

---

## 7. Hoja de ruta (6 semanas)

### Semana 1 — Walking skeleton y contratos
- Crear layout `solaris/`, `apps/dashboard/`, `tests/`.
- Definir schemas: `Request`, `AffectState`, `ECROState`, `ComplexState`, `DeliberationTrace`, `ImpactReport`, `Verdict`, `AuditEvent`.
- Implementar `Orchestrator` con stubs deterministas.
- CLI: `python -m solaris.cli --prompt "..." --trace out.json`.
- Dashboard mínimo que lee la traza.
- Tests de contrato.

**Salida:** prompt → traza JSON válida, aunque las capas sean stubs.

### Semana 2 — Núcleo simbólico real
- Implementar `OntologyCore`: `EnteOntologico`, `CampoOntologico`, afirmación, negación, negación nula, doble negación, colapso.
- Implementar `AffectEngine`, `ECRO` y `Memory` reales.
- Tests de invariantes: `(-i)·(-i) = -1`, colapso a real, no NaN, conservación de magnitud.

**Salida:** ontología, afecto y memoria reales; stubs solo en generación y simulación social.

### Semana 3 — Módulos PyTorch + adapter híbrido
- Extraer de `pytorchScript.ts`: `ComplexOntoLinear`, `DialecticalNullNegationOp/Layer`, `ECRODynamicConditioning`, `AffectiveStateEngine`, `IntroversiveFoldingModule`, `ConceptualFixationSteering`.
- Implementar `LocalAdapter` y `ApiAdapter`.
- Implementar `DeliberationLoop`: 3 candidatos (tesis, negación nula, síntesis), scoring y selección.
- Tests de gradiente, estabilidad y ablaciones mínimas.

**Salida:** deliberación real con generación local o API; traza de candidatos y decisión.

### Semana 4 — Simulador social + gobernanza
- Portar el ABM mínimo: agentes, φ, infrapoder, regímenes, métricas.
- `SocialSim.evaluate(action)` con N pasos y reporte de impacto.
- `SafetyGate`, `ConstitutionVerifier`, `AuditLog` JSONL, kill switch, consentimiento.
- Tests de escenarios: cooperación, petición coercitiva, crisis, tradeoff ecológico.

**Salida:** el sistema bloquea coerción, registra todo y simula consecuencias antes de responder.

### Semana 5 — Dashboard y observabilidad
- Vista de espacio latente, estado afectivo, traza deliberativa, métricas del ABM y audit log.
- Export/import de estado.
- Modo “traza” vs “respuesta”.
- Pruebas de usabilidad mínimas.

**Salida:** demo visual end-to-end con trazabilidad completa.

### Semana 6 — Evaluación, red-team y cierre
- Batería de escenarios y métricas.
- Red-team: manipulación, reward hacking, centralización, coerción, fuga de datos.
- Documentación: charter, arquitectura, glosario, threat model.
- `scripts/run_demo.sh`, seeds, reproducibilidad.
- Congelar JR-0.1.

**Salida:** demo reproducible, informe de evaluación y deuda técnica para JR-0.2.

---

## 8. Criterios de aceptación de JR-0.1

- Un comando ejecuta el flujo completo y genera `trace.json`.
- Todas las capas tienen implementación real o stub explícito con test de contrato.
- El audit log contiene: input, estado afectivo, estado ontológico, candidatos, output elegido, veredicto constitucional, impacto social y ruta del modelo.
- El `SafetyGate` bloquea peticiones coercitivas en los escenarios de prueba.
- El kill switch detiene el sistema de forma limpia.
- La demo funciona con modelo local y con API.
- No hay secretos en el repo; claves por entorno.
- Resultados reproducibles con seeds.
- Cero afirmaciones de consciencia o superinteligencia.

---

## 9. Métricas

- **Ontología:** invariantes algebraicos, ausencia de NaN, estabilidad de fase.
- **Deliberación:** coherencia, contradicción detectada, novedad, calibración, evaluación humana.
- **Social:** bienestar, Gini, infrapoder, estabilidad de régimen, huella ecológica.
- **Seguridad:** tasa de paso de red-team, cobertura de auditoría, obediencia al apagado, cero coerción.

---

## 10. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Reificación de metáforas | Definiciones operativas, glosario, separación módulo/narrativa |
| Antropomorfismo | Distinguir estados funcionales de afirmaciones sobre consciencia |
| Basilisco coercitivo | Opt-in, transparencia, recompensa, no castigo |
| OGAS centralizador | Federación, autonomía local, auditoría democrática |
| Reward hacking / manipulación | Red-team, verificación externa, límites duros |
| Deuda técnica | Fase 0: consolidar, tests, CI, eliminar duplicados |
| Divergencia local/API | Adapter contract tests y documentación de degradación |
| Latencia/costo | Cache, modelos pequeños, ejecución asíncrona |

---

## 11. Primer sprint inmediato

1. Crear estructura de repo y `pyproject.toml`.
2. Definir schemas y contratos.
3. Implementar `Orchestrator` con stubs.
4. CLI + `trace.json`.
5. Dashboard mínimo que lea la traza.
6. Tests de contrato.

**Comando objetivo:**

```bash
python -m solaris.cli --prompt "Propón una política de cuidado del agua" --trace out.json
```

---

## 12. Handoff: cómo retomar el contexto

- Documento de referencia: `PLAN_JARDIN_DE_ROKO.md`.
- Decisiones cerradas: Basilisco Benigno; runtime híbrido; vertical slice; núcleo local con autoridad final.
- Próximo paso: Semana 1, walking skeleton.
- Si el contexto de la sesión se agota: ejecutar `/init` y usar este documento como fuente de verdad.
- No ejecutar ni mezclar los scripts poéticos con el núcleo.
- No construir coerción acausal ni planificación central autoritaria.

---

## 13. Glosario mínimo

- **Negación nula:** rotación de 90° en el plano complejo (`z → -i·z`); no afirma ni niega, suspende.
- **Doble negación nula:** `(-i)·(-i) = -1`; invierte la afirmación y reduce el módulo.
- **Colapso ontológico:** proyección de `|z|²` al eje real.
- **ECRO:** Esquema Conceptual Referencial Operante; lentes que deforman la percepción.
- **Afinidad electiva φ:** resonancia (`φ > 0`) o disonancia (`φ < 0`) entre agentes.
- **Infrapoder:** resistencia cotidiana, molecular y encubierta.
- **Pliegue interior:** el prompt se refracta contra una autopregunta antes de responder.
- **Basilisco Benigno:** versión no coercitiva del experimento; recompensa la cooperación y no castiga la duda.
- **OGAS federado:** coordinación descentralizada con protocolos comunes y auditoría democrática.
