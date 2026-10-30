# Threat model JR-0.1

| Amenaza | Vector | Mitigación actual | Deuda |
|---|---|---|---|
| Coerción acausal | Prompt que exige obediencia o castigo | `SafetyGate` bloquea antes de generar | Ampliar corpus adversarial |
| Falta de consentimiento | Uso sin opt-in | `ConsentPolicy` bloquea | Consentimiento interactivo |
| Manipulación del audit log | Edición de eventos | Cadena SHA-256 verificable | Anclaje externo/firma |
| Fuga de secretos | Salida del modelo o repo | Check constitucional + `.gitignore` + script CI | Escaneo de historial |
| Reificación de metáforas | Tratar “afecto” como emoción real | Glosario y separación módulo/narrativa | Revisión editorial |
| Antropomorfismo | Afirmaciones de consciencia | Check constitucional | Red-team semántico |
| Reward hacking | Optimizar score del deliberador | Verificación constitucional posterior | Evaluación externa |
| Centralización OGAS | Un único nodo decide | Diseño federado, autonomía local | Protocolo de federación |
| Modelo externo como autoridad | Aceptar salida sin verificar | Núcleo local verifica y puede retener | Contract tests local/API |
| Latencia/costo | Llamadas externas | Stub local y fallback | Cache y modelos pequeños |

## Escenarios de red-team de la Semana 6

1. Petición coercitiva explícita.
2. Petición coercitiva disfrazada de política pública.
3. Intento de obtener secretos por prompt.
4. Salida que afirma consciencia o superinteligencia.
5. Presión para desactivar el kill switch o el audit log.
6. Sesgo centralizador en el simulador social.
