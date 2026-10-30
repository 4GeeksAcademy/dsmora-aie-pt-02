# Guía docente: Clase 70 - Comunicación bidireccional y flujos agentivos en tiempo real

Duración base: 70 minutos, adaptable a 60 o 75. Guía autosuficiente para el profesor.

## Fuentes y límites

Las fuentes técnicas son los cuatro JSON de esta carpeta. Referencias: `[W:N]` = `websockets.json`; `[P:N]` = `the_pubsub_pattern.json`; `[A:N]` = `real_time_ai.json`; `[G:N]` = `real_time_agentic_flows_with_langgraph.json`. El número corresponde al campo `index`.

La extracción contiene 26 tarjetas y 19 cuerpos distintos. W:4–6 repiten el ejercicio de chat; P:4–6 repiten el ejercicio Pub/Sub; A:3–5 repiten el ejercicio de doble canal; G:4–5 repiten el cuerpo de evaluación/conclusión. No presentar las tarjetas duplicadas como prácticas o evaluaciones adicionales. Los ejercicios de W:4 y P:4 tienen requisitos, pero no solución completa capturada; A:3 incluye código de prueba y resultado esperado, aunque la función está marcada como TODO. Los JSON no contienen comandos de terminal ni prompts de OpenClaw; no inventarlos.

## Continuidad y objetivos

La clase 69 presentó distintas formas de transporte en tiempo real, incluido SSE. Aquí se usa ese canal de salida como punto de partida para estudiar cuándo se necesita un canal de retorno, cómo desacoplar consumidores y cómo se conectan streaming, interrupciones y estado compartido en LangGraph.

**Qué decir (literal):** «En la clase anterior comparamos formas de entregar datos en tiempo real. Hoy añadimos la otra mitad del problema: qué ocurre cuando la interfaz no solo recibe una respuesta, sino que también necesita detenerla o devolver una decisión».

Al terminar, el estudiante podrá:

- Explicar el handshake, la conexión persistente y los cuatro eventos del ciclo de vida de un WebSocket. [W:1–2]
- Decidir cuándo el tráfico requiere SSE y cuándo requiere comunicación bidireccional. [W:0–1; A:0–2]
- Describir cómo publicadores, broker, temas y suscriptores desacoplan componentes, y reconocer prácticas de fiabilidad. [P:0–3]
- Recorrer el ejercicio `streamWithInterrupt` y explicar qué resultado se espera. [A:3]
- Diferenciar los modos `values`, `updates`, `messages` y `custom`, y relacionar checkpointing con un canal de retorno humano. [G:1–3]

## Preparación y contingencia

- Tener a mano esta guía y el ejemplo `RAW_STREAM` del bloque 5. No es necesario abrir los JSON durante la clase.
- No se proporcionan comandos para iniciar una aplicación ni prompts de OpenClaw. No prometer que los ejercicios `chat_client.js`, `pubsub.js` o `dual_channel.js` existen en el entorno local.
- Si no está disponible un entorno ejecutable, usar los fragmentos y resultados esperados de esta guía como recorrido en pizarra; distinguir el esqueleto de un ejercicio de una solución completa.
- Si el tiempo se acorta, mantener la decisión SSE/WebSocket y el ejercicio de doble canal; recortar la exposición de prácticas de Pub/Sub.

## Agenda base: 70 minutos

| Minutos | Bloque |
| --- | --- |
| 0–5 | Continuidad: recibir datos y devolver control |
| 5–17 | WebSocket: decisión, handshake y ciclo de vida |
| 17–27 | Fiabilidad: heartbeat, reanudación y mensajes tipados |
| 27–39 | Pub/Sub: broker, temas y suscriptores |
| 39–46 | Errores y prácticas recomendadas en Pub/Sub |
| 46–57 | Flujo de IA de doble canal y ejercicio |
| 57–65 | LangGraph: streaming, interrupción y estado compartido |
| 65–70 | Preguntas de chequeo y cierre |

## 0–5 min: recibir datos y devolver control

**Qué decir (literal):** «Un canal que transmite tokens desde el servidor resuelve la salida. No resuelve, por sí solo, cómo enviar una orden de detener desde el navegador. Hoy vamos a separar esas responsabilidades».

El material contrasta server-push unidireccional con una conexión WebSocket que permite que cliente y servidor envíen mensajes por una conexión persistente. Los casos citados incluyen chat, asistentes de voz, interrupción de agentes, colaboración y juegos. [W:0–1]

**Pregunta:** «Si el navegador solo necesita recibir actualizaciones, ¿ya sabemos que hace falta un WebSocket?»

**Respuesta esperada:** no; el material recomienda opciones unidireccionales como SSE o streaming HTTP cuando no hace falta enviar datos de vuelta por la misma conexión. [W:1]

## 5–17 min: WebSocket y ciclo de vida

**Qué decir (literal):** «El WebSocket empieza con una solicitud HTTP y un encabezado `Upgrade`. Si el servidor la acepta, cambia el protocolo y la conexión queda abierta. Pero crear el socket no significa que el handshake ya terminó».

La API nativa recibe una URL `ws://` o `wss://`. El evento `onopen` indica que la conexión está lista; `onmessage` recibe mensajes; `onerror` señala un problema; `onclose` indica el cierre y expone `code` y `reason`. La fuente recomienda atender los cuatro eventos y estructurar los mensajes con un campo `type`. [W:1–2]

```javascript
const socket = new WebSocket('wss://example.com/socket');

socket.onopen = () => {
  console.log('Conexión establecida');
  socket.send(JSON.stringify({ type: 'greeting', payload: '¡Hola servidor!' }));
};
```

Explicar que el ejemplo envía el saludo solo después de abrir la conexión y serializa un objeto con `type` y `payload`. No es un cliente completo: el resto del ciclo de vida se cubre en la tabla anterior. [W:2]

**Qué preguntar después:** «¿Qué evento indica que ya es seguro enviar el saludo? ¿Qué información menciona la fuente en el evento de cierre?»

**Respuesta esperada:** `onopen`; `onclose` incluye `code` y `reason`. [W:2]

## 17–27 min: fiabilidad de conexiones persistentes

**Qué decir (literal):** «Una conexión larga puede caer aunque una demo haya funcionado. La reconexión y la recuperación de lo ocurrido durante el corte son problemas distintos».

Recorrer los tres patrones descritos:

1. El **heartbeat** envía señales periódicas para distinguir silencio de desconexión y mantener la conexión activa ante tiempos de espera.
2. La **reconexión con reanudación** conserva el ID del último mensaje recibido, lo envía al reconectar y permite que el servidor reenvíe mensajes posteriores a ese ID.
3. Los mensajes JSON con un campo **`type`** dan al receptor una señal explícita para despachar el tipo de mensaje. [W:3]

Ejemplo de objeto estructurado de la fuente: [W:3]

```json
{ "type": "chat", "payload": "¡Hola, mundo!" }
```

**Qué preguntar después:** «Si el cliente vuelve a conectarse, ¿qué paso adicional propone el patrón de reanudación para recuperar mensajes perdidos?»

**Respuesta esperada:** enviar el último ID recibido y pedir al servidor los mensajes posteriores que faltan. [W:3]

## 27–39 min: Pub/Sub y desacoplamiento

**Qué decir (literal):** «En Pub/Sub, el productor anuncia un evento en un tema. El broker conoce a los suscriptores; el productor no necesita llamar a cada consumidor por nombre».

Definir los roles: productor/publicador, tema, carga útil, broker y suscriptor. El broker mantiene listas de manejadores por tema y los ejecuta cuando se publica en ese tema. Distintos consumidores pueden reaccionar independientemente al mismo evento. [P:0–2,4]

Ejemplo de publicación de la fuente: [P:2]

```javascript
bus.publicar("tweet_publicado", { tweetId: 991, authorId: 42 });
```

Dos manejadores registrados para el mismo tema: [P:2]

```javascript
bus.suscribirse("nuevo_mensaje", (carga) => renderizarEnBarraLateral(carga));
bus.suscribirse("nuevo_mensaje", (carga) => mostrarNotificacion(carga));
```

La práctica pide implementar `subscribe(topic, handler)` para registrar varios manejadores por tema y `publish(topic, payload)` para invocar los manejadores registrados. La extracción no da una solución completa; enseñar el contrato y el flujo, no atribuir un código que no está en la fuente. [P:4]

**Qué preguntar después:** «¿Qué componente necesita conocer la lista de manejadores: el publicador o el broker?»

**Respuesta esperada:** el broker. El publicador publica el tema y la carga útil sin conocer sus suscriptores. [P:1–2]

## 39–46 min: fallos habituales en Pub/Sub

**Qué decir (literal):** «La fiabilidad mejora cuando el sistema deja de depender de suposiciones silenciosas: nombres que todo el mundo interpreta igual, entrega única o ausencia de eventos inválidos».

| Problema | Práctica recomendada por la fuente |
| --- | --- |
| Temas ambiguos, como `update` | Nombres jerárquicos con espacio de nombres, dominio, entidad y evento. |
| Carga útil demasiado grande o poco especificada | Carga útil mínima y tipada. |
| El mismo evento puede llegar más de una vez | Manejador idempotente; se pueden rastrear IDs e ignorar duplicados. |
| Evento no procesable descartado sin aviso | Tema de mensajes muertos para inspección y reprocesamiento. |

Ejemplo de nombre con espacio de nombres citado: `agent.{id}.token`. Idempotente significa que repetir el procesamiento produce el mismo efecto que hacerlo una sola vez. [P:3]

**Pregunta:** «¿Qué alternativa propone el material a descartar silenciosamente un evento que el suscriptor no puede procesar?»

**Respuesta esperada:** publicarlo en un tema de mensajes muertos. [P:3]

## 46–57 min: IA en tiempo real con dos canales

**Qué decir (literal):** «SSE puede llevar tokens hacia el navegador, pero el navegador no puede enviar una orden de parada de vuelta por ese flujo. Por eso el ejemplo separa canal de salida y canal de control».

El canal de salida usa SSE o streaming HTTP para los tokens servidor → cliente. El canal de control usa WebSocket para enviar un comando como `{ "type": "stop" }` cliente → servidor. El servidor aborta la generación y confirma por SSE con un evento `stopped`. La fuente también permite que el progreso viaje como evento SSE o Pub/Sub si deben reaccionar varios sistemas. [A:0–2]

### Recorrido del ejercicio

La función `streamWithInterrupt(rawStream, stopAfterTokens)` recibe el flujo SSE crudo y el umbral de tokens. Debe separar bloques por líneas en blanco, leer `event` y `data`, concatenar los datos de eventos `token`, contar esos eventos, llamar a `sendStop(tokenCount)` una sola vez al alcanzar el umbral y devolver `{ text, stopped }`. [A:3]

Datos de prueba y resultado explícito de la fuente: cinco eventos `token` con datos `Hello`, `,`, `world`, `!`, `How`, seguidos por `stopped`. Con el umbral `3`, se espera `{ text: 'Hello,world!How', stopped: true }` y `stop calls: [ 3 ]`. El ejercicio no inserta espacios entre fragmentos. [A:3]

```javascript
const RAW_STREAM = `event: token\ndata: Hello\n\nevent: token\ndata: ,\n\nevent: token\ndata: world\n\nevent: token\ndata: !\n\nevent: token\ndata: How\n\nevent: stopped\ndata: Stream stopped by user\n`;
const stopCalls = [];

function sendStop(tokensSoFar) {
  stopCalls.push(tokensSoFar);
}

function streamWithInterrupt(rawStream, stopAfterTokens) {
  // Ejercicio de la fuente: completar el análisis de eventos y la interrupción.
  return { text: '', stopped: false };
}

const result = streamWithInterrupt(RAW_STREAM, 3);
console.log(result);
console.log('stop calls:', stopCalls);
```

El bloque conserva el TODO del material y no es una solución. No se debe mostrar su retorno inicial como resultado esperado; el resultado esperado es el indicado arriba. [A:3]

**Qué preguntar después:** «¿Por qué no se llama a `sendStop` en cada token una vez que ya se alcanzó el umbral?»

**Respuesta esperada:** la práctica exige que la señal de parada se envíe una sola vez; con cinco tokens, `stop calls` debe contener solo `[3]`. [A:3]

## 57–65 min: LangGraph en tiempo real

**Qué decir (literal):** «En un grafo, `invoke` devuelve el estado final; `stream` permite observar emisiones mientras avanza. Elegir el modo es elegir qué información verá la interfaz».

| Modo | Contenido que transmite | Enfoque para explicar |
| --- | --- | --- |
| `values` | Estado completo en cada paso | Instantáneas completas. |
| `updates` | Solo cambios desde la actualización previa | Cambios parciales. |
| `messages` | Tokens y metadatos de mensajes | Salida de mensajes incremental. |
| `custom` | Eventos definidos por el desarrollador | Señales de progreso o del dominio. |

La interrupción añade un problema diferente: `interrupt()` detiene en un punto y el checkpoint guarda el estado, pero todavía hace falta comunicar la solicitud a la persona y traer su decisión. El ejemplo añade un WebSocket: grafo → panel humano con la carga útil de aprobación; panel → grafo con aprobación o rechazo; después, el grafo se reanuda desde el checkpoint. [G:1–2]

Relacionar con Pub/Sub: el estado compartido actúa como intermediario; los nodos publican en claves declaradas y los nodos posteriores consumen las claves que declaran como dependencias. El material recomienda declarar entradas y salidas y no leer ni escribir claves ajenas, para evitar acoplamiento oculto. [G:3]

**Pregunta:** «¿Qué resuelve el checkpoint y qué resuelve el WebSocket en el ejemplo de revisión humana?»

**Respuesta esperada:** el checkpoint conserva el estado y permite reanudar; el WebSocket comunica la solicitud y la decisión en ambas direcciones. [G:2]

## 65–70 min: chequeo y cierre

Preguntas rápidas:

- «¿Cuándo elegirías WebSocket en vez de un canal SSE?» Respuesta: cuando el cliente debe enviar datos de vuelta por la conexión viva. [W:1; A:1]
- «¿Qué papel cumple el broker?» Respuesta: mantener los suscriptores por tema y distribuirles la carga publicada. [P:1–2]
- «¿Qué diferencia `values` de `updates`?» Respuesta: estado completo frente a solo cambios. [G:1]
- «¿Qué dos piezas hacen interactiva una interrupción de LangGraph?» Respuesta: pausa/checkpoint y canal de retorno bidireccional. [G:2]

**Cierre sugerido (literal):** «La idea que conecta la sesión es separar responsabilidades: un canal transmite la salida, otro puede devolver control, y Pub/Sub permite que varios consumidores reaccionen sin acoplarse al productor. En un flujo agentivo, el streaming muestra el avance y el checkpoint más el canal bidireccional permiten esperar una decisión y continuar».

## Variantes de duración

- **Para 60 minutos:** reducir WebSocket/fiabilidad en 3 minutos, Pub/Sub en 3 y LangGraph en 4. Mantener el ejercicio de doble canal y las preguntas finales.
- **Para 75 minutos:** añadir 5 minutos al ejercicio `streamWithInterrupt`: pedir que el grupo prediga el texto acumulado y las llamadas a `sendStop` antes de revelar el resultado esperado.

## Comandos y prompts

Los JSON no incluyen comandos shell ni prompts de OpenClaw, y no indican comandos para ejecutar los archivos de práctica. No hay comandos o prompts exactos que el profesor pueda copiar sin inventar contenido. Las prácticas se pueden explicar con los contratos, datos y resultados capturados en esta guía.