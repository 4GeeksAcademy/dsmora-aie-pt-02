# Clase 45: Telemetría de frontend — de la taxonomía al envío, la captura en Next.js y los guardrails

## Nota de alcance

Esta guía se redacta exclusivamente a partir de los cuatro JSON guardados en esta carpeta:

- `understanding_telemetry_from_the_frontend_4glwptjz.json` (15 lecciones): taxonomía de las seis categorías de señales de telemetría frontend (identidad/sesión, perfil, contexto de ejecución, uso del producto, rendimiento/calidad, consentimiento), objetivos de la telemetría y cómo las señales se convierten en decisiones de producto.
- `sending_telemetry_from_the_frontend.json` (10 lecciones): contrato del evento (event contract), decisiones de transmisión (endpoint único, batching+debounce, autenticación) y patrones de confiabilidad (`navigator.sendBeacon`, cola de reintentos con backoff exponencial).
- `capturing_telemetry_in_next_js.json` (13 lecciones): los tres puntos de captura en Next.js — vistas de página (`routeChangeComplete`), acciones de usuario (ej. búsqueda) y errores/rendimiento (`window.onerror`, `unhandledrejection`, Error Boundaries, `reportWebVitals`).
- `telemetry_best_practices_guardrails.json` (9 lecciones): las cinco barreras de seguridad de telemetría (consentimiento, limpieza/scrubbing, lista blanca, muestreo, separación de entornos) unificadas en la función `guardEvent()`.

**Limitación de las fuentes (léela antes de dar la clase):** en varias lecciones el contenido scrapeado se repite entre índices consecutivos, un bug conocido del scraper (ver `scripts/scraper.py`). En concreto:

- En `understanding_telemetry_from_the_frontend`, las lecciones 4, 6 y 11 son duplicados exactos de las lecciones 3, 5 y 10 respectivamente — impacto menor, el contenido único cubre bien toda la taxonomía.
- En `sending_telemetry_from_the_frontend` el impacto es **severo**: las lecciones 4 a 9 (tituladas "Implementando el enviador por lotes", "Patrones de confiabilidad para envío", "Construye tu enviador de telemetría", "El modelo mental de implementación", "Evaluación de telemetría en tránsito" y "Conclusión del curso") son todas duplicados idénticos del contenido de la lección 3. Ese contenido de la lección 3 sí describe en detalle `navigator.sendBeacon` y una cola de reintentos con backoff exponencial — lo usamos en esta guía porque es real, pero **no existe contenido capturado específico** para "el modelo mental de 6 pasos" que el curso promete ni para la evaluación final; no se inventan aquí.
- En `capturing_telemetry_in_next_js`, las lecciones 5, 7, 9 y 12 duplican el contenido de las lecciones 4, 6, 8 y 11 (patrón lección teórica + lección de ejercicio que comparte el mismo texto capturado) — impacto menor.
- En `telemetry_best_practices_guardrails`, la lección 5 ("Construyendo una función de malla de telemetría") y las lecciones 7 y 8 (evaluación final y cierre del curso) son duplicados de las lecciones 4 y 6 — no hay contenido propio capturado para el código completo de `guardEvent()` combinando las cinco barreras en una sola función, aunque sí lo tenemos para cada barrera por separado.

Además se incorporó el proyecto asociado `ai-eng-telemetry-capture` (obtenido vía API de BreatheCode, slug en español `ai-eng-camptura-de-telemetria`): `ai-eng-telemetry-capture_project_asset.json` y `ai-eng-telemetry-capture_project_README.es.md`.

## Objetivos de aprendizaje

Al terminar, el grupo podrá:

- Explicar la diferencia entre telemetría frontend y observabilidad backend, y nombrar las seis categorías de señales de telemetría frontend.
- Diseñar un contrato de evento (event contract) con campos base, propiedades tipadas, minimización de PII y versionado de esquema.
- Justificar por qué se agrupan eventos (batching + debounce) en lugar de enviarlos uno a uno, y cuándo usar `navigator.sendBeacon` frente a `fetch`.
- Ubicar los tres puntos de captura de telemetría en una app Next.js (vistas de página, acciones de usuario, errores/rendimiento) y por qué `_app.js` es el lugar centralizado para configurarlos.
- Explicar las cinco barreras de seguridad de telemetría (consentimiento, limpieza, lista blanca, muestreo, separación de entornos) y el orden en que se aplican dentro de `guardEvent()`.
- Aplicar todo lo anterior al proyecto `ai-eng-telemetry-capture`: instrumentar un `TelemetryService` con cola local, batch+debounce, `sendBeacon` y reintentos, más un endpoint stub en FastAPI.

## Preparación del profesor

- Tener a la vista los cuatro JSON de esta carpeta y el README del proyecto (`class_45/ai-eng-telemetry-capture_project_README.es.md`).
- Editor abierto para mostrar los snippets de código (identidad/sesión, contexto de ejecución, `RetryQueue`, seguimiento de vistas de página en Next.js, `ErrorBoundary`, `guardEvent()`).
- No se requiere levantar ningún servidor: todos los ejemplos son fragmentos de código para lectura y discusión, no una demo ejecutable end-to-end.

## Agenda de 75 minutos

| Tiempo | Bloque |
|---|---|
| 0-5 min | Qué es la telemetría frontend y por qué importa |
| 5-15 min | Las seis categorías: identidad/sesión, perfil, contexto de ejecución |
| 15-22 min | Uso del producto, rendimiento/calidad y objetivos de la telemetría |
| 22-30 min | El contrato del evento (event contract) |
| 30-38 min | Decisiones de transmisión: batching + debounce, y patrones de confiabilidad |
| 38-50 min | Captura en Next.js: los tres puntos de instrumentación |
| 50-60 min | Los cinco guardrails de telemetría y `guardEvent()` |
| 60-75 min | Bloque de proyecto: `ai-eng-telemetry-capture` |

Para 60 minutos: fusionar el bloque de "uso del producto/objetivos" en 5 minutos (mencionar solo las 5 categorías de eventos de uso sin el mapeo completo objetivo-señal) y presentar el bloque de proyecto en 8 minutos en lugar de 15.

## Desarrollo para el profesor

### 1. Qué es la telemetría frontend y por qué importa (5 minutos)

**Qué decir (literal)**

> Imaginen su aplicación frontend como una ciudad bulliciosa, donde cada clic, desplazamiento e interacción es un mensaje enviado a un centro de mando central. Esos mensajes son señales de telemetría: la esencia de los productos basados en datos. Nos dicen qué hacen los usuarios, cómo funciona la aplicación y dónde se necesitan mejoras.

Diferenciarla de la observabilidad backend: el backend responde "¿está respondiendo el servidor?" o "¿las consultas a la base de datos son lentas?"; la telemetría frontend responde "¿con qué funciones interactúan los usuarios?", "¿la página carga lo suficientemente rápido?", "¿los usuarios encuentran errores o frustraciones?". Porque captura la intención y la experiencia del usuario, es esencial para productos basados en datos.

**Ejemplo del material**

Un usuario envía un formulario de compra: la telemetría captura la acción (evento de envío), el rendimiento (cuánto tardó el envío) y cualquier error encontrado. Juntas, esas señales cuentan una historia completa.

**Pregunta para el grupo**

> ¿Qué distingue la telemetría frontend de la observabilidad backend?

**Respuesta esperada (del quiz del material)**

La telemetría frontend captura interacciones de usuario y rendimiento de la app desde el lado del cliente; la observabilidad backend rastrea la salud del servidor.

### 2. Las seis categorías de señales de telemetría frontend (10 minutos)

**Qué decir (literal)**

> Para organizar los datos que debe recopilar un frontend, las señales se agrupan en seis categorías: datos de identidad y sesión, señales de perfil de usuario, señales de contexto de ejecución, eventos de uso del producto, métricas de rendimiento y señales de calidad y consentimiento. Piensen en cada evento de telemetría como una carta: el mensaje es el dato principal, pero sin un sobre que diga quién lo envió y desde dónde, el mensaje no tiene sentido. Ese sobre es la identidad y el contexto de ejecución.

Presentar los campos clave de **identidad y sesión** (con el código del material):

```javascript
// Generar o recuperar anonymousId
function getOrCreateAnonymousId() {
  let anonId = localStorage.getItem('anonymousId');
  if (!anonId) {
    anonId = 'anon_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('anonymousId', anonId);
  }
  return anonId;
}

// Gestionar sessionId con tiempo de espera por inactividad de 30 minutos
let sessionId = sessionStorage.getItem('sessionId');
let lastActivity = sessionStorage.getItem('lastActivity');
const now = Date.now();
if (!sessionId || !lastActivity || now - lastActivity > 30 * 60 * 1000) {
  sessionId = createSessionId();
  sessionStorage.setItem('sessionId', sessionId);
}
```

Explicar la diferencia entre `userId` (usuario autenticado, persistente), `anonymousId` (antes del login, en `localStorage`) y `sessionId` (temporal, expira tras 30 minutos de inactividad) y el "ensamblaje de identidad" (`identity_stitched`) que vincula ambos cuando el usuario inicia sesión.

Luego, mencionar brevemente **contexto de ejecución** (`appVersion`, `env`, `route`, `referrer`, parámetros UTM, `featureFlags`, `tenantId`) con el ejemplo de Netflix usando `appVersion` para detectar si un despliegue causó errores de reproducción.

**Qué preguntar después**

> ¿Por qué es importante el `sessionId` en telemetría?

**Respuesta esperada (del quiz del material)**

Agrupa todos los eventos dentro de una sola visita.

### 3. Uso del producto, rendimiento/calidad y objetivos (7 minutos)

**Qué decir (literal)**

> No es necesario rastrear cada interacción del usuario. En su lugar, enfóquense en capturar acciones significativas: los eventos de uso del producto. El material propone cinco categorías: eventos de navegación (`page_view`, `route_change`), eventos de acción clave (`checkout_submitted`, `course_enrolled`), eventos de compromiso (`scroll_depth`, `video_play`), interacciones de error (`error_dismissed`, `retry_clicked`) y eventos de búsqueda (`search_performed`).

Enfatizar la convención de nomenclatura `objeto_accion` en `snake_case` (bueno: `checkout_submitted`; evitar: `click`, `userClickedBuyButton`) y la regla de **no sobre-capturar**: 10-20 acciones de alto valor conectadas a decisiones de producto, no cada clic.

Cerrar con los cinco objetivos de la telemetría frontend del material (personalización, análisis de producto, observabilidad, experimentación, soporte) y el ejemplo: un informe de errores con `errorId`, `sessionId` y eventos recientes permite a soporte reproducir problemas rápidamente.

**Qué preguntar después**

> ¿Por qué es importante recopilar datos de telemetría con un propósito claro?

**Respuesta esperada (del quiz del material)**

Para asegurar que la recopilación de datos sea con propósito y vinculada a decisiones del producto; sin esto se genera ruido y se desperdician recursos.

### 4. El contrato del evento (event contract) (8 minutos)

**Qué decir (literal)**

> Un contrato de evento es la especificación acordada que define la forma exacta y el significado de cada evento que la app envía. Es el plano que asegura que frontend, backend y analistas de datos hablen el mismo idioma.

Presentar los cuatro componentes de un buen contrato (del material): campos base (`event`, `timestamp`, `user`, `context`, `properties`), propiedades tipadas y estables, minimización de PII (nunca correos ni teléfonos en bruto, usar `userId` opaco) y versionado del esquema. Mostrar el contraste malo/bueno:

```json
// Malo: nombre vago y violación de PII
{ "event": "click", "properties": { "email": "user@example.com" } }

// Bueno: nombre claro, sin PII, propiedades tipadas
{
  "event": "add_to_cart",
  "timestamp": "2026-04-24T10:30:00.000Z",
  "user": { "userId": "usr_abc123", "anonymousId": null, "sessionId": "sess_xyz789" },
  "context": { "appVersion": "2.4.1", "env": "production", "route": "/cart" },
  "properties": { "item_id": "sku_456", "quantity": 2 }
}
```

Introducir el **principio de datos a decisión**: "¿qué decisión habilita este campo? Si nadie puede responder, probablemente no pertenece al evento."

**Qué preguntar después**

> ¿Qué deberías usar en lugar de correos electrónicos de usuario en bruto para identificar usuarios en eventos de telemetría?

**Respuesta esperada (del quiz del material)**

`userId` (o `anonymousId` para usuarios no autenticados).

### 5. Decisiones de transmisión y patrones de confiabilidad (8 minutos)

**Qué decir (literal)**

> Imaginen 1.000 usuarios activos generando 50 eventos cada uno en una sesión: si envían cada evento como una solicitud HTTP separada, son 50.000 solicitudes por minuto contra su backend. El agrupamiento (batching) reduce esto en más del 95%.

Presentar las tres decisiones del material: endpoint único `POST /telemetry/events` que acepta `{ "events": [...] }`; batching + debounce (enviar al alcanzar un tamaño máximo de buffer o tras N segundos de inactividad); y autenticación vía token/cookie o `anonymousId` para usuarios no autenticados.

Luego, el problema de la descarga de página: si el usuario cierra la pestaña, un `fetch` en curso puede cancelarse y perderse el evento. La solución del material es `navigator.sendBeacon`:

```javascript
function flushOnUnload(buffer) {
  if (buffer.length === 0) return;
  const payload = JSON.stringify({ events: buffer });
  navigator.sendBeacon('/telemetry/events', payload);
  buffer.length = 0;
}

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') {
    flushOnUnload(eventBuffer);
  }
});
```

Y la cola de reintentos con backoff exponencial para fallos de red (mostrar la clase `RetryQueue` del material si hay tiempo: guarda eventos fallidos en `localStorage`, reintenta con retrasos crecientes 1s/2s/4s, descarta tras un máximo de reintentos).

**Qué preguntar después**

> ¿Cómo decide el cliente cuándo enviar el lote de eventos?

**Respuesta esperada (del quiz del material)**

Cuando se alcanza el límite de tamaño del lote o tras un tiempo de debounce (no inmediatamente tras cada evento).

### 6. Captura en Next.js: los tres puntos de instrumentación (12 minutos)

**Qué decir (literal)**

> En Next.js, la telemetría se captura en tres puntos estratégicos: vistas de página, acciones del usuario, y errores/rendimiento. `_app.js` es el centro de control porque envuelve cada página, se ejecuta una vez por navegación y tiene acceso al router — es el lugar ideal para configurar los hooks una sola vez.

**Vistas de página:** la navegación del lado del cliente en Next.js no dispara el evento nativo `load` del navegador más que una vez, así que hay que manejar dos casos — carga inicial y `routeChangeComplete`:

```jsx
useEffect(() => {
  track('page_view', {
    url: window.location.href,
    route: router.pathname,
    referrer: document.referrer || null,
    timestamp: new Date().toISOString(),
  });
  prevUrl.current = window.location.href;

  const handleRouteChange = (url) => {
    track('page_view', {
      url: window.location.origin + url,
      route: router.pathname,
      referrer: prevUrl.current,
      timestamp: new Date().toISOString(),
    });
    prevUrl.current = window.location.origin + url;
  };

  router.events.on('routeChangeComplete', handleRouteChange);
  return () => router.events.off('routeChangeComplete', handleRouteChange);
}, []);
```

**Acciones del usuario:** ejemplo del material con un formulario de búsqueda — sanitizar la entrada (recortar y limitar longitud), colocar la llamada de telemetría después de la operación asíncrona, y nunca enviar la entrada cruda:

```jsx
const handleSearch = async (e) => {
  e.preventDefault();
  const sanitizedQuery = query.trim().substring(0, 100);
  const response = await fetch(`/api/search?q=${encodeURIComponent(sanitizedQuery)}`);
  const data = await response.json();
  setResults(data.results);
  track('search_performed', { query: sanitizedQuery, result_count: data.results.length });
};
```

**Errores y rendimiento:** `window.onerror` y `unhandledrejection` para errores globales, un `ErrorBoundary` de React para errores de renderizado (con `getDerivedStateFromError` y `componentDidCatch`), y la exportación especial `reportWebVitals` de Next.js para Core Web Vitals (LCP, FCP, CLS, FID, TTFB):

```jsx
export function reportWebVitals(metric) {
  track('web_vital', {
    name: metric.name,
    value: Math.round(metric.value),
    rating: metric.rating,
    id: metric.id,
  });
}
```

Enfatizar la sanitización de las trazas de error (eliminar rutas absolutas, truncar a ~2000 caracteres) antes de enviarlas como telemetría.

**Qué preguntar después**

> Una aplicación solo usa `window.onerror` para capturar errores. Un componente React falla durante el renderizado por una referencia nula en JSX. ¿Lo capturará `window.onerror`? ¿Qué falta?

**Respuesta esperada (del material)**

No — `window.onerror` no captura errores de renderizado de React; para eso se necesita un `ErrorBoundary` con `componentDidCatch`.

### 7. Los cinco guardrails de telemetría (10 minutos)

**Qué decir (literal)**

> Sin barreras de seguridad, un sistema de telemetría puede enviar eventos de usuarios que no han dado consentimiento, filtrar información personal a través de campos de texto libre, incluir propiedades sensibles, saturar el backend con eventos de alta frecuencia, o mezclar datos de pruebas con producción. Las cinco barreras del curso son: verificación de consentimiento, limpieza (scrubbing), lista blanca (allowlist), muestreo (sampling) y separación de entornos — todas aplicadas dentro de una función `guardEvent()`.

Explicar el orden y por qué importa (del material): consentimiento primero (para no procesar nada si no hay permiso), luego limpieza, luego lista blanca, luego muestreo, y separación de entornos como puerta final.

Mostrar el ejemplo de limpieza (scrubbing) con regex para correos y teléfonos:

```javascript
const SCRUB_FIELDS = ['query', 'comment', 'message', 'feedback', 'description'];
function scrubField(value) {
  if (typeof value !== 'string') return value;
  return value
    .replace(EMAIL_REGEX, '[email]')
    .replace(PHONE_REGEX, '[phone]')
    .substring(0, 100);
}
```

Y el ejemplo de muestreo para eventos verbosos (`api_latency`, `scroll_depth`, `mousemove`) con tasas bajas (5-10%), nunca aplicado a eventos críticos como errores o compras:

```javascript
const VERBOSE_EVENTS = new Set(['api_latency', 'scroll_depth', 'mousemove']);
function shouldSample(eventName, sampleRate) {
  if (!VERBOSE_EVENTS.has(eventName)) return true;
  return Math.random() < sampleRate;
}
```

Cerrar mostrando dónde se llama `guardEvent()` en la canalización: dentro del sender, antes de agregar el evento al buffer.

```javascript
const safeEvent = guardEvent(event, options);
if (safeEvent !== null) {
  buffer.push(safeEvent);
}
```

**Qué preguntar después**

> ¿Qué barrera debe aplicarse primero en `guardEvent()`? ¿Por qué?

**Respuesta esperada (del quiz del material)**

Verificación de consentimiento — es la más económica y crítica, evita procesar eventos que de todas formas no deben enviarse.

### 8. Bloque de proyecto: `ai-eng-telemetry-capture` (15 minutos, 8 en versión de 60 min)

**Resumen de requisitos del proyecto** (de `ai-eng-telemetry-capture_project_README.es.md`)

- **Fase 1 — Endpoint stub en FastAPI:** crear `POST /telemetry/events` en `services/`, que acepte `{ "events": [...] }`, loguee la cantidad de eventos y el `event_type` de cada uno, y responda `200 OK` con `{ "received": N }`. Definir el modelo Pydantic `TelemetryEvent` con `eventId`, `timestamp`, `sessionId`, `userId`, `event_type`, `schemaVersion`, `requestId`, `properties`. Leer la URL desde la variable de entorno `TELEMETRY_ENDPOINT`.
- **Fase 2 — `TelemetryService` en el frontend:** crear `uis/backoffice/src/services/telemetry.ts` con cola local en memoria, batch+debounce (10s o 20 eventos, lo que ocurra primero), flush confiable con `navigator.sendBeacon` en `visibilitychange`, y reintentos con backoff (hasta 3 intentos). El servicio agrega automáticamente `eventId`, `sessionId`, `userId`, `timestamp`, `schemaVersion` y `requestId`. Se expone una única función pública `track(eventType, properties)`.
- **Fase 3 — Instrumentación amplia:** todas las métricas obligatorias del `CONTEXT-empresa.md` del estudiante, más un piso técnico transversal (errores no capturados, al menos una métrica de rendimiento, vistas de página/navegación), respetando el allowlist de propiedades de cada evento del `event-schemas.json` propio.
- **Actividad adicional:** Web Vitals vía `reportWebVitals`, y eventos de autenticación (login fallido, sesión expirada) sin incluir nunca contraseña o email en `properties`.
- **Entrega:** PR contra el monorepo con título `feat: telemetry event capture`, incluyendo lista de eventos instrumentados, captura de DevTools con un lote llegando al stub con 200, y mención de la actividad adicional si se hizo.

**Cómo hilarlo con las lecciones de hoy**

- El contrato del evento (bloque 4) es literalmente el modelo `TelemetryEvent` que pide la Fase 1: mismos campos base (`eventId`, `timestamp`, `sessionId`, `userId`, `properties`).
- El `TelemetryService` de la Fase 2 es el mismo enviador con batching+debounce y `sendBeacon`/reintentos visto en el bloque 5 — el README pide exactamente "10s / 20 eventos" y "flush con `sendBeacon`", que coincide con los patrones de confiabilidad ya explicados.
- La instrumentación de la Fase 3 (errores, rendimiento, navegación) es el mismo trabajo del bloque 6 (Next.js): `window.onerror`/`unhandledrejection`, `reportWebVitals`, y el patrón de `page_view` en `_app.js`.
- El allowlist de propiedades por `event-schemas.json` es la barrera de "lista blanca" del bloque 7, aplicada ahora con el vocabulario propio de la empresa del estudiante en lugar de nombres genéricos.

**Ejemplos en lenguaje natural**

- "Cuando un usuario hace clic en 'Agregar a inventario', mi `TelemetryService.track('inventory_item_added', { item_id, quantity })` debe encolar el evento, no llamar a `fetch` directamente."
- "Si el usuario cierra la pestaña con 3 eventos pendientes en el buffer, el listener de `visibilitychange` debe disparar `navigator.sendBeacon` antes de que se pierdan."
- "Si `TELEMETRY_ENDPOINT` no está configurado, el stub de FastAPI debe fallar de forma explícita en el arranque, no silenciosamente."

**Mini plan en pseudocódigo**

```text
INICIO
  Paso 1: Backend — crear router `services/telemetry_router.py`
    Definir modelo Pydantic TelemetryEvent (eventId, timestamp, sessionId, userId,
      event_type, schemaVersion, requestId, properties)
    POST /telemetry/events -> loguear N eventos y event_type de cada uno
                            -> responder 200 { "received": N }
    Leer TELEMETRY_ENDPOINT desde variable de entorno

  Paso 2: Frontend — crear uis/backoffice/src/services/telemetry.ts
    Cola local en memoria (array)
    track(eventType, properties):
      agregar eventId, sessionId, userId, timestamp, schemaVersion, requestId
      encolar evento
      si cola >= 20 eventos O pasaron 10s -> enviar lote via fetch a NEXT_PUBLIC_TELEMETRY_ENDPOINT
    listener visibilitychange -> si oculto: navigator.sendBeacon con cola pendiente
    en fallo de envío -> reintentar con backoff hasta 3 veces, luego descartar

  Paso 3: Instrumentar
    Métricas obligatorias del CONTEXT-empresa.md del estudiante
    Piso técnico: window.onerror, unhandledrejection, page_view en _app.js,
                  al menos 1 métrica de rendimiento
    Respetar allowlist de properties de event-schemas.json (nada "por si acaso")

  Paso 4: Verificar
    Abrir DevTools > Network, confirmar lote llegando al stub con 200

  Paso 5: Entregar
    PR "feat: telemetry event capture" con lista de eventos + captura de DevTools
FIN
```

## Cierre sugerido

- Recapitular la cadena completa: taxonomía (qué recopilar) → contrato del evento (cómo estructurarlo) → envío confiable (batching, `sendBeacon`, reintentos) → captura en Next.js (dónde engancharlo) → guardrails (qué NO debe salir nunca).
- Recordar la limitación de fuentes: el "modelo mental de 6 pasos" y el código completo de `guardEvent()` combinando las cinco barreras no están en el material capturado — si alguien pregunta por ellos, aclarar que se explican los principios de cada barrera pero no existe el snippet unificado en las fuentes de esta clase.
- Cerrar con la pregunta de reflexión del material: "¿por qué es crítica la función `guardEvent()` para la preparación en producción de un sistema de telemetría?"
