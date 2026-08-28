# Clase 43: Telemetría — fundamentos, arquitectura y casos reales

## Nota de alcance

Esta guía se redacta exclusivamente a partir de los tres JSON guardados en esta carpeta:

- `introduction_to_telemetry.json` (9 lecciones): qué es la telemetría, mentalidad de hipótesis primero, batch vs stream, viabilidad del transporte y el patrón de sobre de evento (event envelope).
- `telemetry_architecture.json` (10 lecciones): las cuatro decisiones arquitectónicas clave, mecanismos de transporte (serialización, HTTP POST, WebSockets, `sendBeacon`, manejo de fallos), estrategias de limitación y los modelos de procesamiento en flujo/lotes.
- `most_representative_cases_in_telemetry.json` (13 lecciones): telemetría de producto (Spotify, Netflix), telemetría de sistemas y seguridad (Google, Cloudflare, SRE, presupuestos de error, OpenTelemetry, SIEM, EDR) y telemetría del mundo físico (Tesla, Waymo, Uber, DHL).

**Limitación de las fuentes:** en varias lecciones el contenido scrapeado se repite entre índices consecutivos (por ejemplo, "Lote vs Flujo" aparece igual en los índices 2 y 3 del primer tutorial, y el contenido de "Vehículos Conectados y Logística" se repite de forma idéntica desde el índice 6 hasta el índice 12 del tercer tutorial). Esto significa que **no hay contenido real capturado** para "Telemetría de Inteligencia de Negocios" (embudos de fraude, precios dinámicos), "Patrones transversales en telemetría", "Estudios de caso y evaluación" ni la conclusión del tercer curso — solo se sabe, por la lección de bienvenida, que ese dominio existe y que el curso estudia casos de Spotify, Netflix, Google, Cloudflare, Tesla, Waymo, Amazon, Stripe y Airbnb. Esta guía no inventa esos casos: si se menciona el dominio de inteligencia de negocios, se hace solo a nivel general, tal como aparece en la lección de bienvenida.

Además se incorporó el proyecto asociado `ai-eng-telemetry-plan` (obtenido vía API de BreatheCode): `ai-eng-telemetry-plan_project_asset.json` y `ai-eng-telemetry-plan_project_README.es.md`.

## Objetivos de aprendizaje

Al terminar, el grupo podrá:

- Definir telemetría como recolección deliberada de señales observables para habilitar decisiones específicas, y aplicar la mentalidad de "hipótesis primero" para justificar cada evento.
- Distinguir procesamiento en flujo vs por lotes según latencia, costo y caso de uso.
- Diseñar un sobre de evento (event envelope) estándar y justificar por qué la carga útil debe ser pequeña, consistente y estable en el esquema.
- Explicar las cuatro decisiones arquitectónicas de telemetría: dónde procesar, cómo transportar, con qué frecuencia enviar y qué modelo de procesamiento usar.
- Elegir mecanismos de transporte (HTTP POST, WebSockets, `sendBeacon`) y estrategias de limitación (control de tasa, muestreo, debounce) según el caso.
- Reconocer patrones de telemetría de producto, de sistemas/seguridad (SRE, presupuestos de error, OpenTelemetry, SIEM, EDR) y del mundo físico (mantenimiento predictivo, edge processing).
- Aplicar todo lo anterior para responder al RFI del proyecto: diseñar un Plan de Telemetría con catálogo de eventos, Event Envelope y justificación stream/batch.

## Preparación del profesor

- Tener a la vista los tres JSON de esta carpeta y el README del proyecto.
- Editor abierto para mostrar los snippets JavaScript (`TelemetryBuffer`, `sendBeacon`, `emitTelemetry`).
- No se requiere levantar ningún servidor: todos los ejemplos son fragmentos de código para lectura y discusión, no una demo ejecutable end-to-end.

## Agenda de 75 minutos

| Tiempo | Bloque |
|---|---|
| 0-5 min | Qué es la telemetría y por qué importa |
| 5-12 min | Mentalidad de hipótesis primero + batch vs stream |
| 12-22 min | Event Envelope y viabilidad del transporte |
| 22-30 min | Arquitectura de telemetría: capas y 4 decisiones clave |
| 30-42 min | Mecanismos de transporte + demo de código |
| 42-50 min | Estrategias de limitación y modelos de procesamiento en flujo |
| 50-58 min | Telemetría de producto y de sistemas/seguridad |
| 58-64 min | Telemetría del mundo físico |
| 64-75 min | Bloque de proyecto: Plan de Telemetría |

Para 60 minutos: recortar el bloque de telemetría del mundo físico a una mención breve (1 min) y presentar el bloque de proyecto en 8 minutos en lugar de 11.

## Desarrollo para el profesor

### 1. Qué es la telemetría y por qué importa (5 minutos)

**Qué decir (literal)**

> Imaginen construir una aplicación sin saber realmente cómo interactúan los usuarios con ella: lanzan funciones nuevas pero no saben si son útiles, dónde se atascan los usuarios o por qué abandonan. Esa es la realidad de muchos equipos: construyen a ciegas. La telemetría es la práctica que cambia esto — es la recopilación deliberada de datos observables de sistemas en funcionamiento y usuarios, que permite tomar decisiones basadas en evidencia en lugar de suposiciones.

Diferenciarla de la recolección genérica de datos: la telemetría captura lo que los usuarios **hacen**, no solo lo que dicen que hacen. Mencionar por qué importa en la era de IA: los modelos de IA se están comoditizando, pero la ventaja competitiva está en los datos propietarios y de alta calidad que la telemetría produce.

**Ejemplos del material**

- Netflix rastrea qué escenas se rebobinan, no porque el usuario lo reporte, sino porque el reproductor emite eventos de telemetría.
- Un embudo de compra instrumentado revela que el 40% de los usuarios abandona en el paso de dirección de envío — algo que ninguna encuesta descubriría.
- Un tutor de IA entrenado con datos de qué explicaciones releen los estudiantes supera a uno entrenado solo con calificaciones auto-reportadas.

**Pregunta para el grupo**

> ¿Por qué los datos de telemetría (comportamiento observado) son más confiables que una encuesta de satisfacción (comportamiento auto-reportado)?

**Respuesta esperada**

Porque capturan lo que realmente hace el usuario, no lo que dice o recuerda haber hecho.

### 2. Mentalidad de hipótesis primero + batch vs stream (7 minutos)

**Qué decir (literal)**

> Cada evento de telemetría debe responder a una pregunta específica o apoyar una decisión — la mentalidad de hipótesis primero evita rastrear todo indiscriminadamente. Si no pueden explicar qué decisión habilita un evento, no vale la pena capturarlo.

Presentar los dos modelos de procesamiento:

- **Procesamiento en flujo (stream):** maneja eventos uno a la vez, de inmediato. Latencia muy baja, mayor costo de infraestructura (siempre activo). Casos de uso: detección de fraude, alertas en tiempo real, paneles en vivo. Ejemplo del material: una plataforma de pagos que detecta transacciones fraudulentas en milisegundos.
- **Procesamiento por lotes (batch):** acumula eventos durante un período y los procesa juntos. Latencia mayor, menor costo por evento. Casos de uso: informes semanales, análisis de tendencias. Ejemplo del material: un equipo de marketing que revisa informes semanales de participación.

**Tabla de la compensación (del material)**

| Aspecto | Procesamiento en flujo | Procesamiento por lotes |
|---|---|---|
| Latencia | Baja (tiempo real) | Alta (retrasada) |
| Costo | Alto (sistemas siempre activos) | Bajo (procesamiento periódico) |
| Formato de datos | Eventos individuales | Arreglos de eventos en lotes |

Mencionar que muchos sistemas usan un **enfoque híbrido**: flujo para eventos críticos (errores, fraude) y lotes para datos menos urgentes (clics, vistas).

**Qué preguntar después**

> Un cuadro de búsqueda dispara un evento en cada tecla presionada. Un usuario escribe "fastapi tutorial" (16 caracteres). ¿Deberíamos enviar 16 eventos?

**Respuesta esperada (del quiz del material)**

No: conviene usar **desaceleración (debounce)** — esperar a que el usuario deje de escribir por un corto período y disparar un solo evento con la consulta final, en lugar de **limitación (throttling)** de un evento por segundo sin importar la actividad.

### 3. Event Envelope y viabilidad del transporte (10 minutos)

**Qué decir (literal)**

> Sin un mecanismo de transporte viable y una carga útil bien estructurada, los datos de telemetría corren el riesgo de perderse, retrasarse o corromperse. Una carga útil viable debe ser pequeña (para reducir ancho de banda y costo), consistente (para que los sistemas posteriores la procesen sin errores) y estable en el esquema (para no romper paneles y pipelines).

> Imaginen enviar un evento de 2KB, 10.000 veces por segundo — eso es 20MB/s de tráfico. Optimizar el tamaño de la carga no es solo velocidad, también es costo y confiabilidad.

Presentar el **patrón del sobre de evento (event envelope)**: una estructura JSON predecible con campos base fijos y un objeto `properties` flexible para datos específicos.

| Campo | Propósito |
|---|---|
| `event` | Nombre del evento (ej. `lesson_completed`) |
| `timestamp` | Cuándo ocurrió, en ISO 8601 |
| `userId` | Identificador del usuario |
| `sessionId` | Identificador de la sesión |
| `context` | Metadatos adicionales (ej. IDs de curso o lección) |
| `properties` | Datos específicos del evento |

**Ejemplo del material**

```json
{
  "event": "lesson_completed",
  "timestamp": "2026-06-16T09:00:00Z",
  "userId": "u_abc123",
  "sessionId": "s_xyz789",
  "context": {
    "courseId": "c_456",
    "lessonId": "l_7"
  },
  "properties": {
    "timeSpentSeconds": 420
  }
}
```

**Qué decir (literal)**

> Renombrar `user_id` a `userId` a mitad de proyecto puede hacer que todas las consultas que esperan el campo antiguo dejen de retornar resultados. A eso se le llama deriva del esquema — rompe paneles y pipelines silenciosamente.

Mecanismos de transporte mencionados en el material: **POST a endpoints por lotes** (el más común), **streams WebSocket** (entrega en tiempo real) y **`navigator.sendBeacon`** (confiable al cerrar una página).

**Pregunta para el grupo**

> ¿Qué mecanismo de transporte es el más adecuado para enviar datos de telemetría cuando el usuario cierra una pestaña del navegador?

**Respuesta esperada**

`navigator.sendBeacon`, porque envía datos de forma confiable sin bloquear la descarga de la página.

### 4. Arquitectura de telemetría: capas y 4 decisiones clave (8 minutos)

**Qué decir (literal)**

> Imaginen intentar arreglar un coche sin ningún indicador en el tablero — sin velocímetro, sin indicador de combustible. Los sistemas de software enfrentan el mismo problema sin telemetría.

Presentar las tres partes de la arquitectura de telemetría (del material):

1. **Punto de recolección:** donde se genera y captura la información (dispositivos cliente, servidores).
2. **Capa de transporte:** cómo se mueve la información hacia los sistemas de procesamiento.
3. **Capa de procesamiento:** dónde y cómo se analiza y almacena.

Y las **cuatro decisiones arquitectónicas clave** que deben tomarse antes de construir cualquier sistema:

1. **Dónde procesar los datos:** ¿cliente, servidor o híbrido?
2. **Cómo transportar los datos:** ¿qué formatos y mecanismos?
3. **Con qué frecuencia enviar los datos:** ¿qué estrategias de limitación?
4. **Qué modelo de procesamiento usar:** ¿flujo o lotes?

**Qué decir (literal)**

> Estas decisiones están interconectadas. Procesar en el cliente reduce el tamaño de los datos enviados por red, lo que afecta las elecciones de transporte y las necesidades de limitación. Cambiar estas decisiones después de la implementación es costoso y complejo — hay que planificarlas con anticipación.

**Ejemplo del material**

> Spotify recopila cada salto, repetición y búsqueda fallida no para espiar a los usuarios, sino para alimentar algoritmos de recomendación.

**Qué preguntar después**

> Procesar datos en el lado del cliente típicamente ayuda a... ¿qué?

**Respuesta esperada**

Reducir el uso de ancho de banda y dar retroalimentación local más rápida (frente a enviar todo en bruto al servidor).

### 5. Mecanismos de transporte + demo de código (12 minutos)

**Qué decir (literal)**

> La serialización convierte estructuras de datos complejas en un formato adecuado para transmisión. JSON es legible y fácil de depurar, pero tiene cargas más pesadas y es más lento de analizar. Los formatos binarios como Protocol Buffers o MessagePack son compactos y rápidos, pero menos legibles y requieren herramientas adicionales. El compromiso: usar JSON para desarrollo y depuración, y cambiar a binario cuando el tamaño y el rendimiento sean críticos.

Repasar los tres mecanismos de transporte con más detalle: **HTTP POST** (el más simple, solicitudes discretas), **WebSockets** (conexión persistente full-duplex para tiempo real) y **`sendBeacon`** (envío sin espera al descargar la página).

Presentar el manejo de fallos: **colas de reintento**, **buffer local** (para cuando el cliente está sin conexión) y **estrategias de respaldo** (cambiar de método de transporte si uno falla).

**Comando/código exacto para mostrar en clase**

```javascript
class TelemetryBuffer {
  constructor() {
    this.queue = [];
    this.sending = false;
  }

  enqueue(event) {
    this.queue.push(event);
    this.sendNext();
  }

  async sendNext() {
    if (this.sending || this.queue.length === 0) return;
    this.sending = true;
    const event = this.queue[0];
    try {
      await fetch('https://telemetry.example.com/collect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(event)
      });
      this.queue.shift(); // eliminar evento enviado
    } catch (e) {
      // Fallo de red: mantener evento en cola y reintentar después
    } finally {
      this.sending = false;
      if (this.queue.length > 0) this.sendNext();
    }
  }
}
```

```javascript
window.addEventListener('pagehide', () => {
  const payload = JSON.stringify({ eventType: 'pagehide', timestamp: Date.now() });
  navigator.sendBeacon('https://telemetry.example.com/collect', payload);
});
```

**Qué decir (literal)**

> Esto asegura que los datos de telemetría se envíen incluso si el usuario cierra la pestaña o navega fuera.

**Prompt exacto para la demo con agente de IA**

```text
Completa la clase TelemetrySender del reto de código del material: agrega listeners para el cierre de página y cambios de estado de red en el constructor, implementa enqueue para agregar el evento a la cola e intentar enviarlo, y en sendNext usa fetch POST con JSON.stringify(event) como body, eliminando el evento de la cola solo si el envío fue exitoso y manteniéndolo en cola si falla.
```

**Pregunta para el grupo**

> ¿Por qué el manejo de fallos (colas de reintento, buffer local) es esencial en un sistema de telemetría?

**Respuesta esperada**

Porque las redes son poco fiables; sin estas estrategias se pierden eventos cuando falla una petición o el cliente está sin conexión.

### 6. Estrategias de limitación y modelos de procesamiento en flujo (8 minutos)

**Qué decir (literal)**

> Las estrategias de limitación controlan el volumen de datos para evitar sobrecargar los sistemas sin perder señales importantes.

Mencionar, tal como aparecen en el material, las estrategias de limitación por nombre: **control de tasa (rate limiting)**, **muestreo (sampling)** y **debounce** — sin profundizar más allá de esto, ya que el material no desarrolla el detalle técnico de cada una fuera de las preguntas de evaluación.

Profundizar en el procesamiento en flujo (el material sí lo detalla):

- **Manejo atómico de eventos:** cada evento se procesa como una unidad autónoma, sin esperar a otros.
- **Ingesta de eventos:** con un broker de mensajes como Apache Kafka.
- **Particionado:** por una clave (ej. ID de usuario) para mantener el procesamiento ordenado por entidad.
- **Transformaciones sin estado** (filtros, enriquecimiento) y **procesamiento con estado** (almacenes de estado local para agregados o sesión).
- **Tolerancia a fallos:** checkpoint y reproducción, para reanudar sin perder o duplicar eventos.

**Ejemplo del material**

> Una aplicación deportiva en vivo procesa cada actualización de puntaje de inmediato y la envía a los clientes conectados vía WebSockets.

**Escenario para discutir en grupo (del quiz del material)**

> Una aplicación de transporte compartido necesita detectar en tiempo real cuando un conductor excede la velocidad y alertar de inmediato al equipo de operaciones. ¿Qué modelo de procesamiento aplica?

**Respuesta esperada**

Procesamiento en flujo, porque se requieren resultados casi en tiempo real para una alerta inmediata.

### 7. Telemetría de producto y de sistemas/seguridad (8 minutos)

**Qué decir (literal)**

> La telemetría de producto captura señales de comportamiento a nivel de evento — no solo qué hacen los usuarios, sino, con el contexto y la secuencia de eventos, por qué lo hacen.

Ejemplos del material:

- **Spotify:** rastrea saltos (y el segundo exacto en que ocurren), repeticiones, búsquedas fallidas y adiciones a listas — alimenta el sistema de recomendación sin depender de calificaciones explícitas.
- **Netflix:** monitorea tiempo hasta la primera reproducción, tasas de finalización por episodio, patrones de pausa y re-visionado — informa decisiones de qué series renovar o cancelar.

Diferenciar telemetría de producto (comportamiento y compromiso del usuario) de la observabilidad del backend (salud y rendimiento del sistema).

**Qué decir (literal)**

> La telemetría de sistemas puede ser de 10 a 100 veces el volumen de la telemetría de producto, se genera automáticamente y suele requerir detección casi en tiempo real.

Presentar, tal como en el material:

- **Google Search:** cada solicitud HTTP genera telemetría de producto (qué se buscó) y de sistemas (tiempo de respuesta, errores).
- **Cloudflare:** procesa 50 millones de solicitudes HTTP por segundo, usando telemetría de sistemas para la infraestructura y de seguridad para mitigar ataques DDoS en tiempo real.
- **SRE y presupuestos de error:** el enfoque de Google para gestionar confiabilidad usando telemetría para cumplir SLAs; los presupuestos de error cuantifican el tiempo de inactividad aceptable.
- **OpenTelemetry:** estándar abierto que unifica trazas, métricas y registros entre proveedores.
- **SIEM:** agrega registros de múltiples fuentes (firewalls, servidores, red) y correlaciona eventos para detectar patrones de ataque complejos (ej. login fallido + escaneo de puertos desde la misma IP).
- **EDR:** recopila telemetría continua de endpoints (ejecuciones de procesos, escrituras de archivos, conexiones de red) para caza proactiva de amenazas.

**Código del material (captura en el borde para detección de anomalías)**

```javascript
function emitTelemetry(request) {
  const telemetryEvent = {
    sourceIP: request.ip,
    timestamp: Date.now(),
    headers: request.headers,
    payloadSize: request.body.length,
    responseCode: request.response.statusCode
  };
  sendToTelemetryPipeline(telemetryEvent);
}
```

**Qué preguntar después**

> ¿Por qué la telemetría de seguridad exige análisis en milisegundos, más que la telemetría de producto?

**Respuesta esperada**

Porque las amenazas deben detectarse y mitigarse antes de que causen daño; en producto, la decisión suele tolerar más latencia.

### 8. Telemetría del mundo físico (6 minutos)

**Qué decir (literal)**

> La telemetría del mundo físico transforma cómo las empresas mantienen vehículos y optimizan logística, convirtiendo datos de sensores en decisiones accionables.

Casos del material:

- **Tesla:** procesa la mayoría de los datos de batería/temperatura/motor localmente en el vehículo (edge), y envía solo resúmenes comprimidos y anomalías a la nube. Si una anomalía supera un umbral (ej. 0.1% de la flota), dispara una actualización OTA para ajustar la gestión de batería antes de que ocurra una falla.
- **Waymo:** genera terabytes de datos de sensores por hora (LiDAR, radar, cámaras, GPS); los casos límite (comportamientos inusuales de peatones) se señalan a bordo y alimentan el reentrenamiento del modelo.
- **Uber:** combina GPS, tráfico en vivo y comportamiento del conductor (frenadas bruscas) para actualizar el ETA cada 30 segundos y puntuar la seguridad del conductor en tiempo real.
- **DHL:** sensores en flota y paquetes miden ubicación, combustible, temperatura e impactos; un paquete que supera 30°C dispara una alerta para intervención humana.

**Puntos clave (del material)**

- El procesamiento en el borde reduce costos de transmisión al analizar localmente y enviar solo lo esencial.
- El mantenimiento predictivo detecta anomalías antes de fallas, reduciendo tiempos de inactividad frente al mantenimiento programado.
- La telemetría habilita bucles de retroalimentación: recolección → análisis → decisión → nuevos datos.

**Para 60 minutos:** mencionar solo el caso de Tesla (edge processing + OTA) como ejemplo representativo y pasar directo al proyecto.

### 9. Cierre y transición al proyecto (2-4 minutos)

**Qué decir (literal)**

> Han visto el ciclo completo: qué es la telemetría, cómo se transporta de forma confiable, cómo se procesa (flujo o lotes) y cómo se aplica en producto, sistemas/seguridad y el mundo físico. El proyecto de hoy les pide aplicar exactamente esto: diseñar, sin escribir una línea de instrumentación todavía, el plan de telemetría completo de su compañía.

**Preguntas de cierre**

- ¿Qué campos no pueden faltar en el Event Envelope que van a diseñar?
- Para un evento de "intento de modificar stock directamente rechazado por el sistema", ¿lo procesarían en flujo o en lotes? ¿Por qué?

## Puntos clave para reforzar

- Cada evento debe responder a una hipótesis y habilitar una decisión concreta; si no, se descarta.
- El Event Envelope estandariza campos base (`event`/`eventId`, `timestamp`, `userId`, `sessionId`, `properties`) para evitar deriva de esquema.
- Las cuatro decisiones arquitectónicas (dónde procesar, cómo transportar, con qué frecuencia, qué modelo) están interconectadas y deben planearse con anticipación.
- Stream = baja latencia y alto costo de infraestructura; batch = mayor latencia y menor costo por evento; muchos sistemas combinan ambos.
- La telemetría de sistemas/seguridad exige mayor volumen y menor latencia que la de producto.

## Bloque de proyecto: Plan de Telemetría (11 minutos para 75 min / 8 minutos para 60 min)

### Resumen de requisitos del proyecto

El proyecto (`ai-eng-telemetry-plan` / "Diseño del plan de telemetría de tu compañía") responde a un RFI del equipo de gestión: la compañía tiene un sistema de inventario en FastAPI + Supabase donde el stock no se modifica directamente, solo mediante órdenes de entrada/salida trazables. El equipo de operaciones no tiene visibilidad de qué pasa en el sistema. El entregable es un **documento de diseño**, no código:

- `docs/telemetry/telemetry-plan.md`: catálogo de eventos, Event Envelope, y justificación stream/batch.
- `docs/telemetry/event-schemas.json`: esquema exportado de todos los eventos.

Fases del proyecto:

1. **Catálogo exhaustivo:** incluir las métricas obligatorias del `CONTEXT-empresa.md` (piso, no techo), mapear al menos 5 puntos de instrumentación en el flujo de inventario (incluyendo intentos rechazados de modificar stock directamente), y explorar otras secciones del backoffice (autenticación, rendimiento, errores de frontend, navegación). Cada evento debe completar la frase: *"Capturamos `[event_type]` porque necesitamos saber `[hipótesis]`, lo que nos permite tomar la decisión `[decisión]`."*
2. **Event Envelope:** definir campos obligatorios (`eventId`, `timestamp` ISO 8601, `sessionId`, `userId`, `event_type` en formato `entidad_acción`, `schemaVersion`, `requestId`, `properties`), diseñar todos los eventos obligatorios más al menos 8 adicionales cubriendo 3+ categorías, con allowlist de propiedades y marcado de datos sensibles/PII.
3. **Estrategia de entrega:** justificar stream vs batch por evento según urgencia de la decisión (no preferencia técnica), documentar throttle/debounce para eventos de alta frecuencia, y escribir una sección de riesgos y exclusiones.

### Cómo hilarlo con las lecciones previas

- El Event Envelope del proyecto (`eventId`, `timestamp`, `sessionId`, `userId`, `event_type`, `schemaVersion`, `requestId`, `properties`) es una extensión directa del sobre de evento visto en el bloque 3 — mismo patrón de campos base + `properties` flexible.
- La decisión stream vs batch por evento (fase 3) aplica directamente el criterio de latencia/costo/caso de uso del bloque 2 y 6.
- El throttle/debounce para eventos de alta frecuencia conecta con la pregunta del cuadro de búsqueda vista en el bloque 2.
- La distinción entre eventos "obligatorios" (negocio/inventario) y "oportunidades identificadas" (autenticación, rendimiento, errores, navegación) refleja la separación entre telemetría de producto y telemetría de sistemas/seguridad del bloque 7.

### Ejemplos en lenguaje natural (alineados al brief)

- "Capturamos `direct_stock_edit_rejected` porque necesitamos saber cuántos intentos hay de modificar stock sin pasar por una orden, lo que nos permite decidir si hace falta reforzar permisos o capacitar usuarios."
- "Capturamos `session_expired` porque necesitamos saber con qué frecuencia los operadores pierden su sesión a mitad de tarea, lo que nos permite decidir si extendemos el tiempo de expiración."
- "Capturamos `stock_threshold_triggered` porque necesitamos saber qué tan seguido se dispara la alerta de stock mínimo, lo que nos permite decidir ajustes en los puntos de reorden."

### Mini plan en pseudocódigo

```text
INICIO
  Paso 1: Leer CONTEXT-empresa.md y extraer métricas obligatorias, entidades y restricciones de negocio
  Paso 2: Crear carpeta docs/telemetry/ en el monorepo de la compañía
  Paso 3: Mapear el flujo de inventario e identificar >= 5 puntos de instrumentación
           (incluye intentos rechazados, validaciones fallidas, umbrales mínimos)
  Paso 4: Explorar backoffice (auth, rendimiento, errores frontend, navegación)
           y listar oportunidades adicionales, amplio y sin límite mínimo
  Paso 5: Para cada evento candidato, completar
           "Capturamos [event_type] porque necesitamos saber [hipótesis],
            lo que nos permite tomar la decisión [decisión]"
           Si no se puede completar -> descartar el evento
  Paso 6: Clasificar cada evento como obligatorio u oportunidad identificada
  Paso 7: Definir el Event Envelope estándar (eventId, timestamp, sessionId,
           userId, event_type, schemaVersion, requestId, properties)
  Paso 8: Diseñar el esquema de cada evento con allowlist de propiedades
           y marcar datos sensibles/PII con su estrategia de anonimización
  Paso 9: Para cada evento, decidir y justificar stream vs batch según urgencia
  Paso 10: Documentar throttle/debounce para eventos de alta frecuencia
  Paso 11: Escribir sección de riesgos y exclusiones (qué se descartó y por qué)
  Paso 12: Exportar event-schemas.json y redactar telemetry-plan.md
  Paso 13: Abrir PR "docs: telemetry design plan" con resumen de conteo de eventos,
           categorías cubiertas y la decisión de diseño más difícil
FIN
```
