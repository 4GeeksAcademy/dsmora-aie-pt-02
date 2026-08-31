# Clase 45 — Guía práctica: cómo explicar el contrato del evento, el envío confiable y los guardrails sin ambigüedad

## Nota de alcance

Este documento complementa a [resume_01.md](resume_01.md). No agrega casos nuevos ni datos que no estén en los cuatro JSON de la carpeta (`understanding_telemetry_from_the_frontend_4glwptjz.json`, `sending_telemetry_from_the_frontend.json`, `capturing_telemetry_in_next_js.json`, `telemetry_best_practices_guardrails.json`) ni en el proyecto asociado (`ai-eng-telemetry-capture`). Su objetivo es dar al profesor un método reutilizable para **explicar cualquier campo o evento con rigor técnico** y para que el grupo **distinga con seguridad las decisiones que suelen confundirse** al instrumentar telemetría de frontend, incluyendo los errores de comprensión más comunes al enseñar este tema.

## 1. Método para explicar cualquier campo del contrato de evento

Un error frecuente al enseñar el contrato de evento es presentarlo como una lista de campos a memorizar ("tiene `event`, `timestamp`, `user`, `context`, `properties`") en lugar de como una herramienta de diseño. Para evitarlo, cada campo o evento debe descomponerse siempre en tres partes, en este orden:

1. **Qué captura exactamente:** el dato concreto, sin ambigüedad (un `event_type` en `snake_case`, un `userId` opaco, un `timestamp` en formato ISO).
2. **Decisión que habilita:** qué pregunta de producto, soporte o seguridad responde ese campo. Si nadie puede nombrar la decisión, el campo probablemente no pertenece al evento (principio de datos a decisión de resume_01, bloque 4).
3. **Riesgo si falta o se hace mal:** qué se rompe — un panel de análisis, una alerta legal (GDPR/CCPA), la reproducibilidad de un bug, o el presupuesto del backend.

Recomendación práctica: pedirle al grupo que complete esta frase en voz alta para cada campo del contrato antes de seguir:

> *"Capturamos `[campo]` porque necesitamos responder `[decisión]`; si falta o está mal formado, se rompe `[riesgo concreto]`."*

### 1.1 Ejemplos del material, descompuestos con el método de 3 partes

| Campo / evento | Qué captura | Decisión que habilita | Riesgo si falta o está mal |
|---|---|---|---|
| `anonymousId` | Identificador persistente en `localStorage` antes del login | Vincular la actividad de un visitante anónimo con su cuenta cuando inicia sesión (`identity_stitched`) | Se pierde el historial de un usuario que exploró la app antes de registrarse |
| `sessionId` | Identificador temporal que expira tras 30 min de inactividad | Agrupar todos los eventos de una sola visita para reconstruir un flujo de uso | Sin él, no se puede saber si dos eventos pertenecen a la misma sesión o a visitas distintas |
| `userId` (nunca correo/teléfono en bruto) | Identificador opaco del usuario autenticado | Personalización y soporte, sin exponer PII | Violación de privacidad (GDPR/CCPA) si se usa el correo directamente |
| `appVersion` en `context` | Versión de la app que generó el evento | Detectar si un despliegue específico causó un aumento de errores (ejemplo de Netflix en resume_01) | Imposible correlacionar un pico de errores con el release que lo causó |
| `schemaVersion` | Versión del esquema del evento | Permitir que el backend/analistas sepan qué forma esperar y evolucionar el contrato sin romper paneles | Cambios de esquema silenciosos rompen dashboards y modelos ya entrenados |

Usar esta tabla como guion en el aula: leer la fila completa en voz alta transmite mejor la lógica que solo nombrar el campo.

### 1.2 Error común a corregir en clase

> "El evento tiene que llevar `properties: { email, telefono, ... }` por si después lo necesitamos" no es diseño de contrato, es acumulación de riesgo.

La versión correcta, que hay que modelar frente al grupo:

> "Este evento captura `userId` (no el correo) porque la decisión que habilita es identificar al usuario para soporte y personalización sin exponer PII; si se necesitara contactar al usuario, eso se resuelve con un lookup en el backend usando ese `userId`, no incluyendo el correo en el evento de telemetría."

## 2. Cómo diferenciar "cuándo enviar" de "cómo enviar" sin ambigüedad

### 2.1 El error de confusión más común: política de envío vs mecanismo de transporte

Este es el punto donde más se confunden los desarrolladores nuevos en telemetría de frontend, y conviene aclararlo explícitamente en clase, siguiendo la misma lógica que ya se usó en resume_02 de la clase 43 para stream vs batch:

> **Batching + debounce responde "¿cuándo agrupo y disparo el envío?". `fetch` vs `navigator.sendBeacon` responde "¿con qué mecanismo viaja ese envío?". Son decisiones independientes que se combinan, no se sustituyen.**

Ejemplo para desarmar la confusión en el aula, con el material de resume_01 (bloque 5):

- El buffer se llena o expira el temporizador de debounce (política de **cuándo**) → en ese momento, si la página sigue activa, el envío normal se hace con `fetch` a `POST /telemetry/events`.
- Si en ese mismo instante el usuario cierra la pestaña (`visibilitychange` → `hidden`), el envío del buffer pendiente **no puede esperar** al ciclo normal de debounce: se dispara inmediatamente con `navigator.sendBeacon`, que es el mecanismo (**cómo**) diseñado para sobrevivir a la descarga de la página.

Error típico a corregir: pensar que "usar `sendBeacon`" ya resuelve la confiabilidad completa del sistema. En realidad `sendBeacon` solo cubre el caso de descarga de página, tiene un límite de carga útil (menor a 64KB) y es "fire-and-forget" (no hay respuesta, así que no se sabe si el servidor realmente lo procesó). Por eso el material también exige, para los fallos de red durante uso normal (pestaña abierta), una **cola de reintentos con backoff exponencial** guardada en `localStorage` — un patrón de confiabilidad distinto, que resuelve un problema distinto (fallo de red, no cierre de pestaña).

### 2.2 Checklist de dos preguntas para decidir el mecanismo correcto en clase

Para cualquier punto de envío que el grupo proponga, aplicar este checklist en orden:

1. **¿La página sigue activa y hay margen de tiempo?** Si sí, usar el flujo normal: agrupar en buffer (batching + debounce) y enviar con `fetch`.
2. **¿La página se está cerrando o el usuario está navegando fuera?** Si sí, no hay margen: usar `navigator.sendBeacon` con lo que haya en el buffer en ese instante, sin esperar al debounce.

Y, en paralelo, para el caso de fallo de red (independiente de las dos preguntas anteriores): **¿el envío por `fetch` falló?** Si sí, encolar en la cola de reintentos con backoff (1s/2s/4s) y descartar tras el máximo de intentos, tal como especifica la Fase 2 del proyecto `ai-eng-telemetry-capture` ("reintentos con backoff, hasta 3 intentos").

## 3. Por qué importa el orden de los cinco guardrails (no es arbitrario)

### 3.1 La razón económica detrás del orden

Al enseñar los cinco guardrails (consentimiento, limpieza, lista blanca, muestreo, separación de entornos), un error común es presentarlos como una lista sin justificar el orden. El material es explícito sobre por qué el consentimiento va primero:

> "¿Por qué verificar el consentimiento primero? Es la verificación más económica y crítica. Evita el procesamiento innecesario de eventos que no deben enviarse."

Esto es un patrón general que conviene explicitar en clase: dentro de `guardEvent()`, cada barrera tiene un costo computacional distinto, y conviene ordenar de la más barata/crítica a la más costosa, para no gastar ciclos limpiando o filtrando un evento que de todas formas se va a descartar:

1. **Consentimiento** — una sola lectura booleana (`consent.analytics === false`). Si falla, se corta todo el resto de inmediato.
2. **Limpieza (scrubbing)** — recorrer campos de texto libre con regex (más costoso que un booleano, pero necesario antes de decidir qué propiedades quedan).
3. **Lista blanca (allowlist)** — filtrar claves del objeto `properties`.
4. **Muestreo (sampling)** — solo aplica a un subconjunto de eventos verbosos (`api_latency`, `scroll_depth`, `mousemove`); no tiene sentido aplicarlo antes de saber que el evento ya pasó las barreras de privacidad.
5. **Separación de entornos** — puerta final, evita que el resultado ya "limpio" de desarrollo contamine producción.

### 3.2 Error común a corregir en clase

> "Da igual el orden de las barreras, total todas se ejecutan igual" — es la afirmación que hay que desarmar explícitamente.

Contraejemplo para el aula: si se aplicara la limpieza (regex sobre texto libre) **antes** de verificar el consentimiento, el sistema estaría gastando ciclos de CPU sanitizando datos de un usuario que nunca debió ser rastreado — trabajo desperdiciado y, peor, procesamiento de datos personales sin base legal, que es justo lo que el guardrail de consentimiento existe para evitar.

## 4. Guion ampliado para reforzar identidad y sesión (para usar tal cual en el aula)

> "Piensen en `anonymousId`, `sessionId` y `userId` como tres capas de la misma persona en el tiempo. El `anonymousId` es el visitante antes de que sepamos quién es — vive en `localStorage` porque tiene que sobrevivir entre sesiones. El `sessionId` es la visita de hoy — vive en `sessionStorage` y expira a los 30 minutos de inactividad porque solo necesita agrupar lo que pasó en esta visita. El `userId` aparece recién cuando la persona inicia sesión, y ahí es donde ocurre el `identity_stitched`: el sistema le dice al backend 'este `anonymousId` de las últimas tres semanas y este `userId` que acaba de loguearse son la misma persona'."

Pregunta de cierre para el grupo:

> "Si un usuario navega dos días sin loguearse y al tercer día se registra, ¿qué evento(s) permite reconectar todo ese historial con su cuenta nueva?" (Respuesta esperada: el evento `identity_stitched`, que vincula el `anonymousId` acumulado con el `userId` recién creado.)

## 5. Rúbrica rápida para autoevaluar la explicación en clase

Antes de pasar al siguiente bloque de la agenda, el profesor puede chequear en 10 segundos si la explicación de un campo o mecanismo fue completa:

- [ ] ¿Se nombró el campo o evento de forma concreta (no una generalidad tipo "guarda información del usuario")?
- [ ] ¿Se explicitó la decisión de producto/soporte/seguridad que ese campo habilita?
- [ ] ¿Se mencionó el riesgo concreto si el campo falta o expone PII?
- [ ] Si la explicación involucra envío de eventos, ¿se distinguió la política de "cuándo" (batching+debounce) del mecanismo de "cómo" (`fetch` vs `sendBeacon`), y no se trató como lo mismo?
- [ ] Si la explicación involucra `guardEvent()`, ¿se justificó el orden de las barreras por costo/criticidad, y no solo se enumeraron las cinco?

Si alguna casilla queda sin marcar, es la señal de volver sobre ese punto antes de avanzar con la agenda de resume_01.
