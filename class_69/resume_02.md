# Dossier para NotebookLM: comunicación en tiempo real, streaming y SSE

## Alcance y procedencia

Este documento organiza las cuatro extracciones de Learn-Pack de `class_69`. Las únicas fuentes técnicas son los JSON nombrados abajo. Las relaciones entre conceptos, tablas de consulta y encabezados son organización editorial; no añaden bibliografía ni contenido técnico externo.

| Código | JSON | Tarjetas extraídas | Tarjetas con contenido distinto |
| --- | --- | ---: | ---: |
| R | `real_time_communication.json` | 7 | 5 |
| E | `common_errors_and_best_practices_in_real_time_com.json` | 8 | 4 |
| B | `streaming_vs_batch.json` | 7 | 5 |
| S | `server_sent_events.json` | 6 | 4 |

Las referencias `[R:N]`, `[E:N]`, `[B:N]` y `[S:N]` apuntan al campo `index` de cada JSON, no a la posición visual de una tarjeta.

### Duplicados y límites de extracción

- R:5–6 repiten R:4, el ejercicio `fetchChunks`.
- E:4–7 repiten E:3, el ejercicio `connectWithBackoff`. Aunque los títulos anuncian diseño de eventos, idempotencia, evaluación de confiabilidad y conclusión, esos cuerpos no fueron capturados como lecciones diferenciadas.
- B:5–6 repiten B:4, el ejercicio `process_streaming`.
- S:4–5 repiten S:3, el ejercicio `consumeStream`.

E:0 sí presenta una vista general que menciona nombres claros de eventos verbo-sustantivo con espacio de nombres, sobres estables e idempotencia de manejadores. Al no haber una lección de desarrollo distinta en las tarjetas posteriores, este dossier conserva esa mención como panorama y no inventa pautas, código o criterios adicionales.

Algunos bloques de práctica están concatenados o truncados. Se conservan sus enunciados y resultados esperados, pero no se reconstruyen soluciones ausentes. E:2 tiene fragmentos de buffer parcialmente dañados por la extracción, por lo que sus estrategias se explican con el texto descriptivo y la tabla, no como código ejecutable. No se extrajeron comandos shell ni prompts de OpenClaw.

## 1. Qué significa comunicación en tiempo real

En una interacción HTTP clásica, el cliente inicia una solicitud, el servidor responde una vez y la conexión se cierra; para conocer un cambio posterior, el cliente debe solicitar otra respuesta. La comunicación en tiempo real permite que el cliente reciba nueva información cuando está disponible, sin una nueva pregunta en cada ocasión. [R:0–1]

Los escenarios incluidos son chat, notificaciones, marcadores deportivos, colaboración y texto de un LLM que aparece progresivamente. La motivación común es que el servidor puede conocer un cambio antes de la siguiente solicitud periódica del cliente. [R:0–1]

La fuente presenta un espectro de técnicas; no hay una única solución que convenga para todos los usos. La dirección del tráfico, la tolerancia al retraso, la sobrecarga y la complejidad determinan la elección. [R:2–3]

## 2. Polling, long-polling y HTTP streaming

### 2.1 Polling

El cliente consulta al servidor repetidamente en un intervalo fijo. El ejemplo usa `setInterval` para llamar a `fetch('/api/messages/latest')` cada 5000 ms, procesa la respuesta cuando `response.ok` y actualiza la interfaz. Es fácil de implementar con Fetch, pero puede producir muchas solicitudes sin novedades; además, si un cambio ocurre justo después de una consulta, el cliente espera al siguiente intervalo. [R:2]

### 2.2 Long-polling

El cliente inicia una solicitud y el servidor la mantiene abierta hasta que tenga datos o se produzca un timeout. Después de procesar la respuesta, el ejemplo inicia otra solicitud. Reduce las respuestas vacías y el retraso respecto del polling fijo, pero conserva un patrón iniciado por el cliente y requiere manejar solicitudes sucesivas, timeout y errores. [R:2]

### 2.3 HTTP streaming

El servidor mantiene abierta una respuesta y envía fragmentos progresivamente. La fuente muestra una respuesta con fragmentos JSON delimitados por nueva línea. El cliente obtiene un lector con `response.body.getReader()`, acumula bytes decodificados en un buffer y procesa cada línea completa. [R:2]

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

`reader.read()` entrega `{ value, done }`: `value` contiene el siguiente fragmento y `done` indica que el flujo terminó. `TextDecoder` con `{ stream: true }` conserva correctamente la decodificación si un carácter multibyte llega dividido entre fragmentos. La fuente identifica como ventajas la baja sobrecarga y la actualización progresiva; como coste, exige soporte del servidor para respuestas fragmentadas y más trabajo del lado cliente. [R:2]

La tarjeta no documenta el formato de la línea final ni manejo de errores/cierre en este ejemplo. Se presenta como demostración de lectura progresiva de JSON delimitado por saltos de línea, no como cliente robusto completo.

## 3. Comparación de modelos

| Modelo | Dirección de datos | Complejidad indicada | Sobrecarga indicada | Caso de uso de la fuente |
| --- | --- | --- | --- | --- |
| Polling | Cliente → servidor, repetidamente | La más baja | Alta por solicitudes vacías | Actualizaciones de baja frecuencia y retraso aceptable |
| Long-polling | Cliente → servidor; solicitud mantenida | Baja a media | Media | Actualizaciones casi en tiempo real sin un protocolo nuevo |
| HTTP streaming | Servidor → cliente en una conexión abierta | Media | Baja, conexión única | Entrega progresiva cuando se controlan ambos extremos |
| SSE | Servidor → cliente, unidireccional | Media | Baja, conexión de larga duración | Notificaciones y tokens de LLM |
| WebSockets | Bidireccional, full dúplex | La más alta | Baja después del handshake | Chat, juegos multijugador y colaboración interactiva |

Proceso de decisión explícito en la fuente: [R:3]

1. Si el cliente necesita enviar datos de vuelta por la misma conexión viva, elegir WebSockets.
2. Si el canal es solo servidor → cliente, considerar SSE o HTTP streaming.
3. Si se tolera cierto retraso, polling puede ser suficiente; para casi tiempo real sin un protocolo nuevo, considerar long-polling.
4. Ajustar la elección a la complejidad que el sistema puede asumir.

Los ejemplos asociados son clima actualizado cada diez minutos (polling), espera de nuevas alertas (long-polling), registros enviados progresivamente (HTTP streaming), tokens de LLM (SSE) y movimientos/actualizaciones de un juego multijugador (WebSockets). [R:3]

## 4. Transporte no es procesamiento

La fuente de batch y streaming separa dos preguntas: cómo se mueve la información (transporte) y cómo la procesa el programa cuando llega (procesamiento). Los datos pueden transportarse hasta un servidor y, una vez allí, procesarse como lote o de manera incremental. [B:0]

### 4.1 Lotes

El procesamiento por lotes opera sobre un conjunto completo, delimitado y disponible antes de comenzar. El programa recorre ese conjunto y produce un resultado final. Tener el conjunto completo facilita ordenar, agregar o unir datos y puede favorecer cálculos que dependen del contexto global. La compensación es esperar hasta completar el lote, por lo que hay más latencia. Nómina y el informe mensual de ventas son ejemplos de la fuente. [B:0–1]

### 4.2 Streaming

El procesamiento en streaming procesa una unidad a medida que llega. La fuente lo asocia con datos potencialmente ilimitados o de tamaño desconocido y baja latencia. Es útil cuando los datos llegan continuamente y el cálculo puede expresarse de forma incremental, como monitorización de sensores, detección de fraude o salida token a token de un LLM. [B:0,2]

En Python, `yield` convierte una función en un generador que emite resultados durante el recorrido, en lugar de devolver una lista completa. La fuente compara dos funciones de conversión de temperaturas: ambas omiten entradas `None` y redondean a un decimal, pero una acumula una lista y la otra emite cada resultado. [B:2]

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

La fuente destaca tres propiedades de `yield`: comenzar a producir antes de procesar todos los datos, evitar almacenar toda la lista de resultados y permitir encadenar generadores. No se afirma que cualquier cálculo pueda procesarse incrementalmente: el tutorial condiciona su conveniencia a que el cálculo admita ese enfoque. [B:2]

La práctica B:4 solicita `process_streaming(readings)`: ignorar lecturas negativas, redondear las no negativas a un decimal y producirlas una a una. Con `[3.14159, -1.0, 2.71828, 0.0, -5.5, 9.999]`, espera `3.1`, `2.7`, `0.0`, `10.0` en ese orden. El esqueleto de implementación está incompleto en la extracción; estos requisitos y valores sí son legibles. [B:4]

## 5. Streaming en LangGraph

La fuente distingue `graph.invoke(...)`, que ejecuta el grafo y devuelve el estado final una vez, de `graph.stream(...)`, que produce eventos mientras el grafo avanza. `stream_mode` selecciona qué forma de dato recibe el consumidor. [B:3]

| Modo | Contenido de cada emisión | Necesidad descrita |
| --- | --- | --- |
| `values` | Estado completo después de cada paso | Instantánea completa en cada punto |
| `updates` | Solo las claves cambiadas, indexadas por nodo | Saber qué cambió en cada paso |
| `messages` | Tokens LLM y metadatos de la llamada que los produjo | Renderizar salida de modelo token a token |
| `custom` | Datos arbitrarios escritos desde un nodo con `get_stream_writer()` | Progreso o señales específicas del dominio |

Ejemplos capturados:

```python
for chunk in graph.stream(inputs, stream_mode="values"):
    print(chunk)

for chunk in graph.stream(inputs, stream_mode="updates"):
    for node_name, state_update in chunk.items():
        print(f"{node_name} actualizado: {state_update}")

for token, metadata in graph.stream(inputs, stream_mode="messages"):
    print(token.content, end="", flush=True)
```

Para el modo `custom`, la fuente muestra un nodo que obtiene `writer = get_stream_writer()`, emite `{"status": "obteniendo datos..."}` y devuelve `{"result": "listo"}`. Los modos también pueden combinarse pasando una lista a `stream_mode`. [B:3]

## 6. Server-Sent Events (SSE)

SSE es un protocolo sobre HTTP con una conexión duradera y unidireccional: el cliente abre la conexión y escucha; el servidor transmite eventos de texto en ella. Está pensado para push servidor → cliente y evita la complejidad de un protocolo bidireccional cuando el cliente no necesita responder por el mismo canal. El tutorial menciona soporte nativo del navegador con `EventSource` y reconexión automática; su práctica opta deliberadamente por Fetch y lectura manual. [S:1]

La respuesta requiere `Content-Type: text/event-stream`. La fuente recomienda `Cache-Control: no-cache` para que proxies o CDN no almacenen el flujo. Sin el primer encabezado, navegador y proxies no interpretan la respuesta como SSE; omitir el segundo no invalida el protocolo, pero puede causar almacenamiento o buffering. [S:1]

### 6.1 Formato de cable

Cada evento es un bloque de una o más líneas terminado por una línea en blanco. La línea `data:` contiene la carga útil; una línea `event:` puede nombrar el tipo. Los eventos nombrados permiten separar tokens, errores y señales de finalización. [S:2]

```text
event: token
data: Hola

event: token
data: mundo

event: done
data:

```

`token` entrega fragmentos que el cliente concatena; `done` señala explícitamente el final. El silencio no basta para decidir si el servidor terminó o sigue procesando. Para pausas largas, la fuente describe heartbeats periódicos cada 15–30 segundos: comentarios (`:`) o un evento mínimo `heartbeat`. [S:2]

Un flujo SSE para salida de LLM se resume en: encabezado `Content-Type`, eventos de token según se generan, heartbeats periódicos si hace falta y evento final `done`. [S:1–2]

### 6.2 Práctica de consumo en bruto

La práctica S:3 define un endpoint `http://localhost:4000/sse` y solicita `consumeStream(url)` en `sse_client.js`, sin usar `EventSource`. El consumidor debe:

1. Obtener la respuesta con Fetch y leer el body como `ReadableStream`.
2. Decodificar fragmentos y almacenarlos en un buffer hasta reunir uno o varios bloques completos separados por línea en blanco.
3. Para cada evento, extraer el nombre `event:` y el valor `data:`.
4. Concatenar `data` cuando el nombre sea `token`.
5. Dejar de leer y devolver el resultado al recibir `done`.

Para `token` con datos `Hello`, luego ` world`, y finalmente `done`, el resultado esperado es `Hello world`. La tarjeta contiene un esqueleto incompleto; no muestra una implementación completa del parser. Tampoco documenta un comando para iniciar el endpoint local. [S:3]

### 6.3 Práctica de lectura de fragmentos

La práctica R:4 separa la lectura genérica del parsing SSE. Pide completar `fetchChunks(url)` para llamar a `fetch(url)`, obtener `response.body.getReader()`, leer hasta `done`, decodificar cada fragmento con `TextDecoder` usando `{ stream: true }` y devolver un arreglo de cadenas, una por fragmento en el orden recibido. La fuente espera que el servidor local de prueba transmita lentamente, pero no incluye sus instrucciones de arranque. [R:4]

## 7. Fallos habituales en tiempo real

La introducción E:0 nombra cuatro categorías: conexiones caídas, consumidores abrumados, nombres/payloads poco claros y entrega duplicada. Describe los cortes de red como comportamiento esperado; recomienda capas de resiliencia a nivel de conexión y diseño de mensaje. El detalle posterior de reconexión y contrapresión está disponible; los títulos posteriores de diseño de eventos, idempotencia y evaluación están duplicados en los JSON. [E:0–3]

### 7.1 Reconexión con backoff exponencial

Las conexiones largas pueden cerrarse por cambio entre Wi-Fi y celular, suspensión del dispositivo, reciclaje del balanceador o reinicios del servidor. La fuente dice que son cortes esperables. Reintentar de inmediato repetidamente puede crear una tormenta si muchos clientes encuentran un servidor caído o sobrecargado. [E:1]

El retroceso exponencial espera un segundo después del primer fallo, dos después del segundo, luego cuatro y ocho, duplicando el intervalo hasta un retraso máximo. La reconexión es responsabilidad del cliente: detectar el corte y gestionar sus reintentos. [E:1]

La práctica `connectWithBackoff(attemptConnect, maxAttempts)` pide llamar a `attemptConnect()`, devolver enseguida el resultado exitoso, esperar y reintentar ante fallo, duplicar el retraso comenzando en 1000 ms, registrar cada retraso y lanzar un error tras agotar `maxAttempts`. El resultado esperado cubre una conexión que falla dos veces y luego funciona, y otra que falla siempre. La captura del código está truncada; no se reconstruye como implementación completa. [E:3]

### 7.2 Contrapresión

Hay contrapresión cuando el productor envía datos más rápido de lo que el consumidor los procesa. El ejemplo recibe 100 eventos por segundo mientras el navegador solo renderiza 20; los excedentes se acumulan en memoria, una cola o la tubería de renderizado. Esto puede congelar la interfaz, causar fallos o perder la conexión. [E:2]

| Estrategia descrita | Integridad/frescura | Uso indicado |
| --- | --- | --- |
| Almacenar con límite | Mantener eventos durante ráfagas breves; consume memoria y puede introducir retraso | Suavizar ráfagas temporales |
| Descartar eventos cuando se llena el buffer | Controla memoria, pero pierde datos intermedios y prioriza frescura | Ticker de precios donde importa el valor reciente |
| Ralentizar al productor | Conserva los datos, con menor rendimiento; necesita soporte del productor/protocolo | Cuando perder datos no es aceptable |

Los fragmentos de código de esta tarjeta tienen caracteres degradados, por lo que se conserva la descripción y la tabla de compromisos, no las líneas como código ejecutable. [E:2]

## 8. Preguntas de consulta

- **¿Streaming y SSE significan lo mismo?** No. Streaming describe procesamiento o entrega progresiva; SSE es un protocolo concreto de eventos servidor → cliente. La fuente trata además el streaming por lotes y los modos de grafo como conceptos distintos. [B:0–3; R:2–3; S:1]
- **¿Cuándo no es suficiente SSE?** Cuando el cliente necesita enviar mensajes por la misma conexión; la comparación recomienda WebSockets para bidireccionalidad. [R:3; S:1]
- **¿Por qué separar eventos con una línea en blanco?** Marca el límite del bloque SSE que se parsea como un evento. [S:2]
- **¿Por qué no usar el silencio para terminar un stream?** Es ambiguo; `done` indica explícitamente el final. [S:2]
- **¿Qué modo de LangGraph expone solo cambios?** `updates`; `values` expone el estado completo. [B:3]
- **¿Qué compromiso hace batch?** Espera el conjunto completo a cambio de simplicidad y contexto global; streaming prioriza baja latencia y procesamiento incremental. [B:0–2]
- **¿Qué significa contrapresión?** El productor supera la capacidad de procesamiento del consumidor. [E:2]

## 9. Continuidad pedagógica

La clase 68 se centró en el control de una ejecución: checkpoints, pausas y reanudación. La 69 toma el siguiente aspecto del flujo de trabajo: transportar y procesar eventos mientras ocurren, y manejar cortes o ritmos desiguales. Este enlace es una transición pedagógica entre clases; el contenido técnico de este dossier procede exclusivamente de los cuatro JSON de class_69.