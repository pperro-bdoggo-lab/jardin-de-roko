# Plan detallado — Semana 2: núcleo simbólico real

- Proyecto: Jardín de Roko `JR-0.1`
- Estado de partida: Semana 1 cerrada, 34 tests en verde, ontología basada en hash.
- Objetivo: reemplazar la proyección stub por una ontología algebraica real sobre
  `C`, integrada en la traza y auditable.
- Fuera de alcance: PyTorch, adapters local/API reales, ABM social y red-team.

---

## 1. Criterio de salida

Al terminar la Semana 2:

- `solaris/onto/` implementa `EnteOntologico`, `CampoOntologico` y las
  operaciones `afirmar`, `negar`, `negar_nula`, `doble_negacion_nula` y
  `colapsar`.
- La traza incluye los pasos ontológicos y los invariantes verificados.
- Afecto, ECRO y memoria tienen tests de estabilidad además de los actuales.
- No hay `NaN` ni `inf` en ninguna traza generada.
- Todos los tests existentes siguen pasando y la demo sigue funcionando.
- Documentación actualizada: glosario, contratos, esquema de traza y roadmap.

---

## 2. Decisiones matemáticas

Sea un ente `z = a + b·i = r·e^{iθ}`, con `r = |z| ≥ 0` y `θ ∈ (-π, π]`.

| Operación | Fórmula | Interpretación operativa |
|---|---|---|
| Afirmación | `A(z) = z` | Mantiene la posición ontológica |
| Negación | `N(z) = -z` | Rotación de 180°, invierte la afirmación |
| Negación nula | `Ø(z) = -i·z` | Rotación de 90°, suspende sin negar |
| Doble negación nula | `Ø²(z) = (-i)·(-i)·z = -z` | Equivale a `N(z)`; conserva módulo |
| Colapso | `C(z) = |z|² = a² + b²` | Proyección real no negativa |

### Nota sobre “reducir el módulo”

El plan original dice que la doble negación nula “invierte la afirmación y reduce
el módulo”. Algebraicamente `(-i)·(-i) = -1`, por lo que el módulo se conserva.
Para no introducir una contradicción:

- la operación base **conserva** el módulo;
- cualquier amortiguación futura será un parámetro explícito (`damping`) y no
  parte de la definición algebraica;
- el glosario se corregirá para distinguir “reduce la componente afirmativa”
  (interpretación) de “reduce el módulo” (falso en el álgebra exacta).

### Precisión numérica

- Cálculos internos en `float` de doble precisión.
- Redondeo a 6 decimales solo al serializar (`ComplexState`/`OntologyStep`).
- Tolerancia de tests: `1e-9` para igualdades algebraicas, `1e-6` para trazas.
- Validación obligatoria: `math.isfinite` en parte real e imaginaria.

---

## 3. Archivos a crear y modificar

### Nuevos

```text
solaris/onto/operations.py          funciones puras sobre complex
solaris/onto/entities.py            EnteOntologico, CampoOntologico
tests/unit/onto/test_operations.py  invariantes algebraicos
tests/unit/onto/test_entities.py    campo, coherencia, serialización
tests/unit/nn/test_affect_stability.py
tests/unit/memory/test_memory_stability.py
tests/integration/test_ontology_trace.py
docs/plans/semana-02-ontologia.md   este documento
```

### Modificados

```text
solaris/onto/core.py                OntologyCore.evaluate/project
solaris/onto/__init__.py            exports públicos
solaris/schemas.py                  OntologyStep, OntologyTrace, Trace.ontology
solaris/orchestrator.py             calcula y audita la ontología
solaris/cli.py                      resumen de módulo/fase/colapso
apps/dashboard/src/main.js          muestra pasos ontológicos
docs/glossary.md                    definiciones corregidas
docs/module-contracts.md            estado real de ontología
docs/trace-schema.md                nuevos campos
docs/roadmap.md                     marcar Semana 2
tests/unit/onto/test_core.py        adaptar a la nueva implementación
```

---

## 4. Diseño de módulos

### 4.1 `operations.py`

Funciones puras, sin estado, fáciles de testear:

```python
def ensure_finite(z: complex) -> complex: ...
def from_polar(modulus: float, phase: float) -> complex: ...
def to_polar(z: complex) -> tuple[float, float]: ...
def normalize_phase(phase: float) -> float: ...
def afirmar(z: complex) -> complex: ...
def negar(z: complex) -> complex: ...
def negar_nula(z: complex) -> complex: ...
def doble_negacion_nula(z: complex) -> complex: ...
def colapsar(z: complex) -> float: ...
```

Reglas:

- `ensure_finite` lanza `ValueError` si `real` o `imag` no son finitos.
- `normalize_phase` devuelve el ángulo en `(-π, π]`.
- `to_polar(0)` devuelve `(0.0, 0.0)` sin error.
- `colapsar` devuelve `abs(z) ** 2`, siempre `≥ 0`.

### 4.2 `entities.py`

```python
@dataclass(frozen=True)
class EnteOntologico:
    z: complex
    etiqueta: str = "contexto"
    origen: str = ""

    def __post_init__(self) -> None: ...
    @property
    def modulus(self) -> float: ...
    @property
    def phase(self) -> float: ...
    def con_z(self, z: complex, etiqueta: str | None = None) -> "EnteOntologico": ...
    def to_state(self, is_collapsed: bool = False) -> ComplexState: ...
```

```python
@dataclass
class CampoOntologico:
    entes: list[EnteOntologico] = field(default_factory=list)

    def agregar(self, ente: EnteOntologico) -> None: ...
    def afirmar(self) -> "CampoOntologico": ...
    def negar(self) -> "CampoOntologico": ...
    def negar_nula(self) -> "CampoOntologico": ...
    def doble_negacion_nula(self) -> "CampoOntologico": ...
    def colapsar(self) -> float: ...
    def centroide(self) -> complex: ...
    def coherencia(self) -> float: ...
    def estado_final(self) -> ComplexState: ...
```

`coherencia` se define como:

```text
coherencia = |Σ z_i| / Σ |z_i|   si Σ |z_i| > 0
coherencia = 0.0               si el campo está vacío
```

Propiedades: `0 ≤ coherencia ≤ 1`; un campo alineado tiende a 1, uno con fases
opuestas tiende a 0. No implica consenso normativo: es solo una métrica
geométrica.

### 4.3 `core.py`

Mantener compatibilidad con el contrato actual:

```python
@dataclass
class OntologyCore:
    def project(self, context: str) -> ComplexState:
        """Compatibilidad: devuelve el estado final."""

    def evaluate(self, context: str) -> OntologyTrace:
        """Nuevo: devuelve pasos, estado final e invariantes."""
```

Flujo de `evaluate`:

1. Derivar un ente determinista desde `sha256(context)`.
2. Crear `CampoOntologico` con ese ente.
3. Registrar `afirmacion` (`z`).
4. Registrar `negacion_nula` (`-i·z`).
5. Registrar `doble_negacion_nula` (`-z`).
6. Registrar `colapso` (`|z|²`) y estado final.
7. Verificar invariantes y devolver `OntologyTrace`.

La proyección sigue siendo determinista para el mismo `context`, pero ahora el
estado final se obtiene de operaciones algebraicas reales, no solo de un hash.

### 4.4 Schemas nuevos

```python
@dataclass
class OntologyStep(JsonModel):
    name: str
    real: float
    imag: float
    modulus: float
    phase: float
    collapsed: float
    note: str = ""

@dataclass
class OntologyTrace(JsonModel):
    final: ComplexState
    steps: list[OntologyStep] = field(default_factory=list)
    invariants: dict[str, bool] = field(default_factory=dict)
    coherencia: float = 0.0
```

Añadir a `Trace` un campo opcional al final para no romper compatibilidad:

```python
ontology: OntologyTrace | None = None
```

En solicitudes bloqueadas, `ontology` queda en `None`.

---

## 5. Integración con el orquestador

### 5.1 `Orchestrator.run`

Reemplazar:

```python
complex_state = self.ontology.project(request.prompt)
```

por:

```python
ontology_trace = self.ontology.evaluate(request.prompt)
complex_state = ontology_trace.final
```

Y añadir a la traza final:

```python
ontology=ontology_trace,
```

Audit log: nuevo evento antes de la deliberación.

```python
self.audit_log.append(
    "ontology.computed",
    {"ontology": ontology_trace.to_dict()},
)
```

### 5.2 `DeliberationContext`

No es obligatorio cambiarlo en Semana 2. El deliberador sigue usando
`complex_state`; los pasos ontológicos quedan disponibles en la traza para la
Semana 3, cuando la generación real pueda consumirlos.

### 5.3 CLI

Añadir al resumen:

```text
ontología: módulo=... fase=... colapso=... coherencia=...
```

### 5.4 Dashboard

Añadir una sección “Ontología” que muestre:

- pasos (`afirmacion`, `negacion_nula`, `doble_negacion_nula`, `colapso`);
- módulo, fase y colapso por paso;
- `invariants` como lista de checks;
- `coherencia`.

Debe tolerar trazas antiguas sin `ontology` mostrando “sin datos”.

---

## 6. Endurecimiento de afecto, ECRO y memoria

La Semana 2 también exige que estas capas sean “reales”. Ya existe una base; el
trabajo es estabilidad y contrato.

### AffectEngine

- Normalizar palabras con y sin tilde (`cooperacion`/`cooperación`).
- Manejar texto vacío, solo signos y textos muy largos.
- Garantizar `valence ∈ [-1,1]`, `arousal/tension/intensity ∈ [0,1]`.
- Añadir tests de mezcla positiva/negativa y de no `NaN`.

### ECRO

- Garantizar cinco lentes y rango `[0,1]`.
- Añadir test de monotonía: mayor `valence` no reduce `cuidado`.
- Añadir test de estabilidad para estados extremos.

### Memoria

- Orden determinista ante empates: `score`, luego `created_at`, luego `item_id`.
- Validar `limit > 0`.
- Garantizar `0 ≤ score ≤ 1`.
- Tests de consulta vacía, límite y resonancia afectiva.
- No persistir nada fuera de `data/` en tests.

---

## 7. Matriz de tests

### Ontología

| Test | Assertion |
|---|---|
| `from_polar`/`to_polar` | roundtrip con tolerancia `1e-9` |
| Afirmación | `afirmar(z) == z` |
| Negación | fase difiere en `π`, módulo conservado |
| Negación nula | `-i·z`; fase rota `-π/2` |
| Doble negación nula | `Ø²(z) == -z` |
| Identidad clave | `(-i) * (-i) == -1` |
| Colapso | `colapsar(z) == abs(z) ** 2`, real y `≥ 0` |
| Cero | `colapsar(0) == 0`, sin excepción |
| No finitos | `NaN`/`inf` lanzan `ValueError` |
| Fase | siempre en `(-π, π]` |
| Campo vacío | `coherencia == 0`, centroide `0` |
| Campo alineado | `coherencia ≈ 1` |
| Campo opuesto | `coherencia ≈ 0` |
| Serialización | `OntologyTrace` es JSON puro |

### Integración

- La traza contiene `ontology.steps` con al menos 4 pasos.
- `ontology.final` coincide con `complex_state`.
- `invariants` contiene `double_null_negation`, `collapse_real`,
  `modulus_conserved`, `no_nan`.
- El audit log contiene `ontology.computed`.
- La solicitud bloqueada no calcula ontología.
- La demo sigue produciendo `data/traces/demo.json`.
- El dashboard tolera trazas sin `ontology`.

### Regresión

- Los 34 tests existentes siguen en verde.
- `bash scripts/run_demo.sh` termina con código 0.
- `bash scripts/check_no_secrets.sh` termina con código 0.

---

## 8. Secuencia de implementación

### Paso 1 — Matemática pura

- Crear `operations.py`.
- Escribir `test_operations.py` antes o junto con la implementación.
- Verificar invariantes algebraicamente.

### Paso 2 — Entidades y campo

- Crear `entities.py`.
- Añadir `test_entities.py`.
- Validar `coherencia`, `centroide` y serialización.

### Paso 3 — Schemas

- Añadir `OntologyStep`, `OntologyTrace` y `Trace.ontology`.
- Asegurar que `to_dict()` sigue siendo JSON puro.
- Añadir tests de serialización.

### Paso 4 — Núcleo e integración

- Implementar `OntologyCore.evaluate`.
- Mantener `project` como wrapper compatible.
- Integrar en `Orchestrator`.
- Añadir evento de auditoría.
- Actualizar `tests/unit/onto/test_core.py`.

### Paso 5 — Afecto, ECRO y memoria

- Añadir tests de estabilidad.
- Corregir solo lo que fallen los tests.
- Evitar cambios de API innecesarios.

### Paso 6 — Observabilidad y documentación

- Actualizar CLI.
- Actualizar dashboard.
- Actualizar `docs/glossary.md`, `docs/module-contracts.md`,
  `docs/trace-schema.md` y `docs/roadmap.md`.
- Añadir el enlace a este plan en `docs/README.md`.

### Paso 7 — Cierre

- Ejecutar suite completa.
- Ejecutar demo y verificar audit log.
- Revisar que no queden stubs en `solaris/onto/`.
- Actualizar el recuento de tests en la documentación.

---

## 9. Estimación

| Bloque | Sesiones |
|---|---|
| Matemática pura + tests | 1 |
| Entidades y campo + tests | 1 |
| Schemas y serialización | 0.5 |
| Núcleo + orquestador + auditoría | 1 |
| Afecto/ECRO/memoria | 0.5 |
| Dashboard y documentación | 1 |
| Regresión y cierre | 0.5 |

Total estimado: **5–6 sesiones de trabajo**.

---

## 10. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Ambigüedad de “reducir módulo” | Definición algebraica explícita; damping separado |
| Romper trazas antiguas | `Trace.ontology` opcional; dashboard con fallback |
| Errores de precisión flotante | Tolerancias por tipo de test; redondeo solo al serializar |
| Reificación de metáforas | Glosario y docs de “real vs. metáfora” |
| Scope creep hacia PyTorch | Semana 3; no tocar `nn/complex.py` ni adapters |
| Tests frágiles por hash | No testear valores concretos de hash; testear propiedades |
| Crecimiento del audit log | Evento adicional acotado; no duplicar toda la traza |

---

## 11. Definition of Done

La Semana 2 se considera cerrada cuando:

- [ ] `solaris/onto/operations.py` y `entities.py` existen y están testeados.
- [ ] `OntologyCore.evaluate` devuelve `OntologyTrace` real.
- [ ] `Orchestrator` incluye `ontology` en la traza y `ontology.computed` en el audit.
- [ ] Los invariantes algebraicos pasan con `1e-9`.
- [ ] La traza no contiene `NaN` ni `inf` para el corpus de pruebas.
- [ ] Afecto, ECRO y memoria tienen tests de estabilidad.
- [ ] Dashboard muestra los pasos ontológicos.
- [ ] Documentación actualizada.
- [ ] Suite completa y demo en verde.
- [ ] Sin dependencias externas nuevas.
