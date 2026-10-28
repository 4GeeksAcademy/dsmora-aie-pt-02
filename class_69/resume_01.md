# Guía docente: Clase 69 - Comunicación en tiempo real y streaming

Duración base: 70 minutos, adaptable a 60 o 75. Guía autosuficiente para el profesor.

## Fuentes y límites

Las fuentes técnicas son los cuatro JSON de esta carpeta. Referencias: `[R:N]` = `real_time_communication.json`; `[E:N]` = `common_errors_and_best_practices_in_real_time_com.json`; `[B:N]` = `streaming_vs_batch.json`; `[S:N]` = `server_sent_events.json`. El número corresponde al campo `index`.

La extracción tiene 28 tarjetas y 20 cuerpos distintos. R:5–6 repiten R:4; E:4–7 repiten E:3; B:5–6 repiten B:4; S:4–5 repiten S:3. No se presentan esas tarjetas duplicadas como lecciones separadas. E:0 anuncia convenciones de nombres de eventos e idempotencia, pero las tarjetas posteriores que desarrollarían esos temas repiten la práctica de reconexión; se conserva el anuncio como panorama, no como una lección detallada.

Los ejercicios de `fetchChunks`, `consumeStream`, `process_streaming` y `connectWithBackoff` aparecen incompletos o concatenados. Se incluyen sus requisitos y resultados esperados, sin atribuirles soluciones completas no capturadas. La extracción no contiene comandos de terminal ni prompts de OpenClaw; no se inventan.

## Continuidad y objetivos

La clase 68 cerró el hilo de control y recuperación de flujos con checkpoints e interrupciones. Aquí se cambia el foco a cómo llegan y se procesan las actualizaciones mientras el sistema está activo: elegimos transporte, modo de procesamiento y controles para conexiones que pueden caer o recibir más datos de los que consumen.

**Qué decir (literal):** «En la clase anterior nos ocupamos de conservar y recuperar el estado de una ejecución. Hoy miramos el flujo de datos en movimiento: cómo recibe el cliente las novedades, si procesamos cada dato al llegar o esperamos al conjunto completo, y qué hacemos cuando la conexión se cae o el consumidor no alcanza el ritmo».

Al terminar, el estudiante podrá:

- Comparar polling, long-polling, HTTP streaming, SSE y WebSockets por direccionalidad, complejidad, sobrecarga y uso. [R:2–3]
- Distinguir transporte en tiempo real de procesamiento por lotes o incremental. [B:0–2]
- Describir los cuatro modos de streaming de LangGraph y cuándo elegirlos. [B:3]
- Explicar el formato SSE y recorrer el consumo de eventos `token`/`done`. [S:1–3]
- Proponer una estrategia de reconexión con backoff exponencial y elegir una respuesta a la contrapresión. [E:1–3]

## Preparación y contingencia

- Preparar esta guía y los ejemplos incluidos; no hace falta abrir los JSON durante la clase.
- Las prácticas mencionan `reconnect.js`, `stream_reader.js`, `sse_client.js`, `process_readings.py` y el endpoint local `http://localhost:4000/sse`, pero no proporcionan comandos de instalación o arranque del servidor. No prometer que esos recursos ya estén disponibles.
- Si no hay servidor de prueba, recorrer los datos de entrada y el resultado esperado de cada práctica, sin afirmar que se ejecutaron.
- No presentar los esqueletos truncados como soluciones completas. Para `fetchChunks` y `consumeStream`, enseñar el flujo de lectura y el análisis solicitados; para backoff, ordenar intentos y esperas; para `process_streaming`, identificar qué valor se emite en cada vuelta.
- No hay prompts de OpenClaw en las fuentes.

## Agenda base: 70 minutos

| Minutos | Bloque |
| --- | --- |
| 0–5 | Qué significa tiempo real y continuidad |
| 5–15 | Polling, long-polling y HTTP streaming |
| 15–23 | Comparar los cinco modelos de comunicación |
| 23–33 | Procesamiento por lotes frente a streaming |
| 33–42 | Modos de streaming en LangGraph |
| 42–55 | SSE: protocolo, formato y lectura |
| 55–65 | Reconexión, backoff y contrapresión |
| 65–70 | Chequeo y cierre |

## 0–5 min: qué significa tiempo real

**Qué decir (literal):** «En el modelo HTTP clásico, el cliente pregunta, recibe una respuesta y la conexión termina. Para una actualización en vivo necesitamos que el cliente pueda recibir lo nuevo sin tener que preguntar de nuevo cada vez».

La comunicación en tiempo real permite que el servidor envíe información tan pronto como está disponible. Los ejemplos de la fuente incluyen chats, marcadores deportivos, notificaciones, herramientas colaborativas y respuestas de LLM que aparecen token por token. [R:0–1]

Hilar con clase 68: la sesión anterior trató persistencia y recuperación del flujo; esta distingue el transporte de la información y su procesamiento. No asumir que streaming significa siempre un protocolo específico: la fuente presenta varias opciones. [B:0; R:2–3]

**Pregunta:** «¿Qué limitación tiene una respuesta HTTP clásica una vez que el servidor la terminó?»

**Respuesta esperada:** no queda un canal abierto para que el servidor envíe cambios posteriores; el cliente debe enviar otra solicitud. [R:1]

## 5–15 min: polling, long-polling y HTTP streaming

**Qué decir (literal):** «Las tres técnicas reducen la espera de formas diferentes: preguntar en intervalos, mantener la solicitud abierta hasta que haya datos o mantener una respuesta abierta para leer fragmentos».

### Polling

El cliente pregunta repetidamente en un intervalo fijo. El ejemplo consulta `/api/messages/latest` cada cinco segundos con `setInterval` y actualiza la interfaz si la respuesta es correcta. Es fácil de implementar con `fetch`, pero muchas solicitudes no encuentran datos nuevos y una actualización que ocurre justo después de una consulta espera hasta la siguiente. [R:2]

```javascript
setInterval(async () => {
  const response = await fetch('/api/messages/latest');
  if (response.ok) {
    const messages = await response.json();
    updateChatUI(messages);
  }
}, 5000);
```

### Long-polling

El cliente hace una solicitud que el servidor mantiene abierta hasta que haya datos o venza el tiempo de espera. Después procesa la respuesta e inicia otra solicitud. Reduce respuestas vacías y latencia respecto al polling fijo, pero sigue iniciándolo el cliente y requiere manejar solicitudes repetidas, tiempos de espera y errores. [R:2]

### HTTP streaming

El servidor mantiene una respuesta HTTP abierta y envía fragmentos progresivamente. El cliente lee `response.body` con `getReader()` y decodifica los bytes a medida que llegan. El tutorial muestra un ejemplo con líneas de JSON delimitadas por nueva línea. `reader.read()` resuelve con `{ value, done }`; `TextDecoder.decode(..., { stream: true })` permite procesar bytes que pueden dividir un carácter multibyte entre fragmentos. [R:2]

```javascript
async function streamMessages() {
  const response = await fetch('/api/messages/stream');
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let boundary = buffer.indexOf('\n');
    while (boundary !== -1) {
      const chunk = buffer.slice(0, boundary);
      buffer = buffer.slice(boundary + 1);
      updateChatUI(JSON.parse(chunk));
      boundary = buffer.indexOf('\n');
    }
  }
}
```

Este ejemplo espera fragmentos con objetos JSON separados por nueva línea; no es un parser SSE. [R:2]

**Pregunta:** «¿Cuál de estos dos métodos mantiene la solicitud abierta hasta que haya datos: polling o long-polling?»

**Respuesta esperada:** long-polling. [R:2]

## 15–23 min: comparar los cinco modelos

**Qué decir (literal):** «La primera pregunta de diseño es si el cliente necesita enviar datos de vuelta por la misma conexión. La segunda es cuánto retraso y complejidad podemos aceptar».

| Modelo | Dirección | Complejidad y sobrecarga | Ejemplo de la fuente |
| --- | --- | --- | --- |
| Polling | Cliente → servidor, repetido | Menor complejidad; alta sobrecarga por solicitudes vacías | Clima actualizado cada 10 minutos |
| Long-polling | Cliente → servidor; solicitud mantenida | Complejidad baja-media; menos respuestas vacías | Esperar nuevas notificaciones |
| HTTP streaming | Servidor → cliente por una conexión abierta | Complejidad media; baja sobrecarga repetida | Registros en vivo progresivos |
| SSE | Servidor → cliente, unidireccional | Complejidad media; conexión larga con baja sobrecarga | Tokens de una interfaz LLM |
| WebSockets | Bidireccional, full dúplex | Mayor complejidad; baja sobrecarga tras handshake | Juego multijugador o colaboración interactiva |

Decisión recogida en la fuente: si el cliente debe enviar datos de vuelta por la misma conexión, usar WebSockets; si no, considerar SSE o HTTP streaming. Si un retraso es aceptable, polling puede bastar; para casi tiempo real sin un protocolo nuevo, long-polling. La elección depende también de la complejidad asumible y de la sobrecarga. [R:3]

**Pregunta:** «Un servidor transmite tokens al navegador, pero el navegador no responde por ese canal. ¿Qué opciones del cuadro encajan?»

**Respuesta esperada:** SSE o HTTP streaming; la fuente usa SSE como ejemplo típico de tokens LLM. [R:3]

## 23–33 min: procesamiento por lotes frente a streaming

**Qué decir (literal):** «Transporte y procesamiento son preguntas distintas. Transporte describe cómo viajan los datos; procesamiento describe si esperamos el conjunto delimitado o actuamos a medida que cada pieza llega».

El procesamiento por lotes espera un conjunto completo y delimitado, lo procesa y genera un resultado final. Facilita operaciones que necesitan contexto global, como ordenar, agregar o unir; su compensación es mayor latencia. Nómina y un informe mensual son ejemplos de la fuente. [B:0–1]

El procesamiento en streaming maneja unidades de datos a medida que llegan; el flujo puede ser continuo o de tamaño desconocido y produce resultados de menor latencia. La palabra clave `yield` convierte una función de Python en un generador que produce valores uno a uno, en vez de reunir todos los resultados en una lista. La fuente muestra la conversión de temperaturas y omite lecturas `None`: [B:2]

```python
def celsius_a_fahrenheit_lote(temps):
    resultados = []
    for temp in temps:
        if temp is None:
            continue
        resultados.append(round(temp * 9 / 5 + 32, 1))
    return resultados

def celsius_a_fahrenheit_stream(temps):
    for temp in temps:
        if temp is None:
            continue
        yield round(temp * 9 / 5 + 32, 1)
```

Ambas funciones reciben una secuencia `temps`; la versión por lotes devuelve una lista después de recorrerla y la versión streaming emite cada resultado con `yield`. La fuente destaca menor almacenamiento de resultados y posibilidad de encadenar generadores. [B:2]

La práctica adicional solicita `process_streaming(readings)`: omitir lecturas negativas y emitir cada lectura no negativa redondeada a un decimal, una por una. Para `[3.14159, -1.0, 2.71828, 0.0, -5.5, 9.999]`, el resultado iterado es `3.1`, `2.7`, `0.0`, `10.0`. El código del ejercicio está incompleto; enseñar esos pasos sin presentar una solución capturada. [B:4]

**Pregunta:** «¿Qué gana la versión `yield` si igual necesita procesar todas las temperaturas?»

**Respuesta esperada:** puede emitir cada valor sin esperar a construir la lista completa y evita almacenar todos los resultados. [B:2]

## 33–42 min: modos de streaming en LangGraph

**Qué decir (literal):** «En LangGraph, `invoke` devuelve el estado final una vez; `stream` entrega eventos mientras el grafo avanza. El modo decide qué clase de dato recibe el consumidor».

Los cuatro modos de la fuente son: [B:3]

| Modo | Qué emite | Cuándo usarlo según la fuente |
| --- | --- | --- |
| `values` | Estado completo después de cada paso | Cuando se necesita la instantánea completa |
| `updates` | Solo las claves cambiadas, agrupadas por nodo | Cuando importa qué cambió |
| `messages` | Tokens del LLM y metadatos de la llamada | Mostrar generación token a token |
| `custom` | Datos arbitrarios escritos desde un nodo con `get_stream_writer()` | Progreso o señales específicas del dominio |

Ejemplos de lectura de la fuente:

```python
for chunk in graph.stream(inputs, stream_mode="values"):
    print(chunk)

for chunk in graph.stream(inputs, stream_mode="updates"):
    for node_name, state_update in chunk.items():
        print(f"{node_name} actualizado: {state_update}")

for token, metadata in graph.stream(inputs, stream_mode="messages"):
    print(token.content, end="", flush=True)
```

El modo `custom` se crea dentro del nodo: `get_stream_writer()` devuelve un writer al que el nodo envía, por ejemplo, `{"status": "obteniendo datos..."}` antes de devolver `{"result": "listo"}`. La fuente también permite combinar modos pasando una lista. [B:3]

## 42–55 min: SSE, formato y consumidor

**Qué decir (literal):** «SSE es un canal HTTP duradero y unidireccional: el cliente se conecta y escucha; el servidor envía eventos de texto mientras los produce».

La respuesta SSE requiere `Content-Type: text/event-stream`. La fuente recomienda `Cache-Control: no-cache` para evitar que proxies o CDN almacenen el flujo. SSE encaja cuando solo hace falta push servidor → cliente; si el cliente necesita enviar por la misma conexión, el tutorial recomienda un protocolo bidireccional como WebSockets. El cliente puede usar `EventSource`; el ejercicio enseña una lectura manual con Fetch y `ReadableStream`. [S:1]

Cada evento es un bloque de líneas de texto seguido por una línea en blanco. `data:` contiene la carga; `event:` puede nombrar el tipo. Los eventos `token` agregan fragmentos, `done` termina el flujo, y `heartbeat` periódico (la fuente propone cada 15–30 segundos) puede mantener vivas conexiones en pausa. [S:2]

```text
event: token
data: Hola

event: token
data: mundo

event: done
data:

```

El consumidor de la práctica `consumeStream(url)` debe leer la respuesta como flujo con Fetch, acumular fragmentos hasta tener bloques completos delimitados por línea en blanco, extraer `event:` y `data:`, concatenar `data` solo cuando el evento sea `token` y detenerse ante `done`. Para los eventos `token` con datos `Hello` y ` world`, el resultado esperado es `Hello world`. La captura muestra un esqueleto, no la implementación resuelta. [S:3]

Otra práctica, `fetchChunks(url)`, solicita usar `fetch`, `response.body.getReader()` y `TextDecoder` con `{ stream: true }`, recolectar fragmentos decodificados y devolver un arreglo en el orden recibido. No confundirla con el parser SSE: esa práctica solo pide leer la respuesta fragmento a fragmento. [R:4]

## 55–65 min: reconexión y contrapresión

**Qué decir (literal):** «Las conexiones largas se caen por cambios de red, suspensión del dispositivo o reinicios del servidor. Esos cortes son esperables; el cliente debe recuperarse sin bombardear un servidor que todavía está fallando».

La fuente desaconseja reintentar inmediatamente y en bucle: muchos clientes pueden crear una tormenta de reintentos. Propone backoff exponencial: esperar 1 segundo, luego 2, 4, 8, duplicando hasta un máximo. El cliente detecta la caída, reintenta hasta `maxAttempts`, registra cada espera y devuelve el resultado al tener éxito; si todos los intentos fallan, la práctica pide lanzar un error. [E:1,3]

**Pasos para la práctica `connectWithBackoff(attemptConnect, maxAttempts)`:** llamar a `attemptConnect()`; si tiene éxito, devolver su resultado; si falla, esperar antes del siguiente intento; iniciar la secuencia de reintentos en 1000 ms y duplicar el retraso; respetar `maxAttempts`; lanzar el error descrito si no se conecta. El código de la tarjeta está concatenado y no se presenta como solución ejecutable. [E:3]

Contrapresión significa que el productor envía datos más rápido de lo que el consumidor puede procesarlos. El ejemplo de la fuente es un panel que recibe 100 eventos por segundo pero renderiza 20. Las estrategias descritas son almacenar en un buffer limitado para suavizar ráfagas, descartar mensajes cuando se prioriza frescura y ralentizar al productor cuando el protocolo ofrece control de flujo. Cada opción intercambia memoria, integridad de datos y rendimiento. [E:0,2]

La tarjeta E:2 muestra fragmentos de código degradados por la extracción, así que enseñar las tres estrategias y sus compromisos, no esas líneas como código listo para ejecutar.

**Pregunta:** «Si no podemos perder eventos, ¿qué estrategia de contrapresión se ajusta mejor según la tabla de la fuente?»

**Respuesta esperada:** ralentizar al productor, si este soporta control de flujo; la fuente la asocia con pérdida de datos inaceptable. [E:2]

## 65–70 min: chequeo y cierre

**Qué decir (literal):** «Elegimos el canal según quién envía, cuánto retraso aceptamos y qué complejidad podemos mantener. Luego elegimos el procesamiento y la estrategia de recuperación según la integridad y frescura que necesita el consumidor».

Preguntas de salida:

- «¿SSE permite que el cliente responda por el mismo canal?» No; es unidireccional. [S:1]
- «¿Qué indica el evento `done`?» Que el flujo terminó; evita que el cliente espere por silencio ambiguo. [S:2]
- «¿Qué devuelve `graph.invoke` frente a `graph.stream`?» Estado final una vez frente a una secuencia de eventos durante la ejecución. [B:3]
- «¿Qué causa contrapresión?» El productor envía más rápido de lo que consume el receptor. [E:2]
- «¿Qué evita una tormenta de reintentos?» Esperas crecientes de backoff exponencial. [E:1]

### Ajuste de duración

- Para 60 minutos, acortar polling/long-polling y el ejemplo de `yield` en 5 minutos, y usar una sola pregunta de cierre; conservar SSE, modos LangGraph y resiliencia.
- Para 75 minutos, ampliar en 5 minutos la comparación de protocolos con los escenarios de clima, notificaciones, registros, tokens LLM y juego multijugador de la tabla. No añadir ejercicios ni requisitos externos.