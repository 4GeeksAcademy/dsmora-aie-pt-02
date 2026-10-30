# Dossier ampliado para NotebookLM: comunicación en tiempo real con WebSockets, Pub/Sub y flujos de IA

## Alcance y procedencia

Este documento organiza las cuatro extracciones de Learn-Pack de `class_70`. Las únicas fuentes técnicas son los JSON indicados en la tabla. Las referencias `[W:N]`, `[P:N]`, `[A:N]` y `[G:N]` apuntan al campo `index` de cada JSON, no a la posición visual de la tarjeta.

| Código | JSON | Tarjetas extraídas | Cuerpos distintos |
| --- | --- | ---: | ---: |
| W | `websockets.json` | 7 | 5 |
| P | `the_pubsub_pattern.json` | 7 | 5 |
| A | `real_time_ai.json` | 6 | 4 |
| G | `real_time_agentic_flows_with_langgraph.json` | 6 | 5 |

En total hay 26 tarjetas y 19 cuerpos distintos. La comparación se hizo sobre el contenido extraído, no sobre los títulos:

- W:4–6 comparten el mismo cuerpo. El material de la práctica de chat en vivo aparece repetido bajo los títulos de evaluación y conclusión. [W:4–6]
- P:4–6 comparten el mismo cuerpo. La práctica de implementación Pub/Sub aparece repetida bajo los títulos de evaluación y conclusión. [P:4–6]
- A:3–5 comparten el mismo cuerpo. El ejercicio de flujo de doble canal aparece también como evaluación y conclusión. [A:3–5]
- G:4–5 comparten el mismo cuerpo para evaluación y conclusión. [G:4–5]

Por ello, las tarjetas repetidas no se presentan como lecciones o evaluaciones independientes. Las prácticas de W y P contienen enunciados, pero no una solución completa capturada; no se reconstruyen sus implementaciones. El ejercicio de A:3 sí incluye una función, datos de prueba y resultado esperado, pero su cuerpo se repite en las tarjetas posteriores. Los JSON no proporcionan comandos de terminal ni prompts de OpenClaw.

## Continuidad con la clase anterior

Como continuidad editorial de `class_69/resume_02.md`, esta clase pasa del panorama de transporte en tiempo real y SSE a dos necesidades que ese canal unidireccional no resuelve por sí solo: enviar control desde el cliente y desacoplar reacciones independientes. Las afirmaciones técnicas que siguen se limitan a las fuentes de `class_70`.

## 1. Modelo general: salida, control y coordinación

El material conecta tres mecanismos:

1. **Salida en vivo:** SSE o streaming HTTP entrega tokens o actualizaciones del servidor al cliente.
2. **Control en vivo:** WebSockets u otro canal bidireccional permite que el cliente envíe acciones como detener una generación o responder a una interrupción.
3. **Coordinación desacoplada:** Pub/Sub permite que un productor publique un evento sin conocer los consumidores que reaccionarán a él. [A:0–2; G:0–3; P:0–2; W:0–1]

La elección depende de la dirección necesaria. Si la interfaz solo recibe datos, SSE puede cubrir el canal de salida. Si también debe enviar una señal por una conexión abierta, WebSockets aportan comunicación bidireccional. Pub/Sub aborda otra dimensión: quién produce un evento y cuántos componentes reaccionan a él. [W:0–1; A:0–2; P:0–1]

## 2. WebSockets

### 2.1 Qué son y cuándo usarlos

Un WebSocket comienza con una solicitud HTTP que incluye `Upgrade: websocket`. Si el servidor la acepta, la conexión cambia al protocolo WebSocket y permanece abierta. Cliente y servidor pueden enviar mensajes independientemente por una conexión TCP persistente. [W:1]

La pregunta de decisión del material es: **¿necesita el cliente enviar datos por la misma conexión mientras permanece abierta?** Si no, el curso recomienda considerar SSE o streaming HTTP; si sí, pone como casos adecuados asistentes de voz, agentes interrumpibles, edición colaborativa y juegos multijugador. WebSockets añaden trabajo para gestionar ciclo de vida, errores y conexión activa, por lo que no se proponen como solución automática para todo flujo. [W:1]

### 2.2 Apertura y ciclo de vida

La API nativa del navegador crea la conexión con `WebSocket`. `ws://` corresponde a una conexión no segura y `wss://` a una segura. La llamada inicia el handshake; no significa que ya se pueda enviar. El ejemplo de la fuente espera a `onopen` antes de enviar un saludo estructurado: [W:1–2]

```javascript
const socket = new WebSocket('wss://example.com/socket');

socket.onopen = () => {
  console.log('Conexión establecida');
  socket.send(JSON.stringify({ type: 'greeting', payload: '¡Hola servidor!' }));
};
```

Los cuatro eventos que se deben considerar son:

| Evento | Qué indica según la fuente |
| --- | --- |
| `onopen` | El handshake terminó y la conexión está lista para enviar. |
| `onmessage` | Llegó un mensaje del otro extremo. |
| `onerror` | Ocurrió un problema de conexión. |
| `onclose` | La conexión terminó; el evento incluye `code` y `reason`. |

El tutorial recomienda atender los cuatro para evitar fallos silenciosos o mensajes perdidos. También recomienda mensajes JSON con un campo `type`, para que el receptor pueda distinguir el propósito de cada mensaje. [W:2]

### 2.3 Fiabilidad de la conexión

Una conexión persistente puede caer por interrupciones de red, reinicios del servidor o tiempos de espera. El material presenta tres medidas: [W:3]

- **Heartbeat:** enviar señales periódicas para distinguir una conexión silenciosa pero viva de una desconectada y ayudar a mantenerla activa ante tiempos de espera de intermediarios.
- **Reconexión con reanudación:** el cliente conserva el ID del último mensaje recibido correctamente; al reconectar lo envía y el servidor reenvía los mensajes perdidos.
- **Mensajes estructurados:** incluir un campo `type` en el objeto JSON para identificar el tipo de mensaje.

Ejemplo de la forma de un mensaje estructurado: [W:3]

```json
{
  "type": "chat",
  "payload": "¡Hola, mundo!"
}
```

El material presenta heartbeat como detección/mantenimiento y reconexión con reanudación como recuperación de mensajes. Reconectar sin reanudar no garantiza, por sí mismo, que el cliente haya recibido lo que ocurrió durante la desconexión. [W:3]

## 3. Patrón Pub/Sub

### 3.1 Roles y flujo

Pub/Sub desacopla al productor de los consumidores. El productor publica un evento en un tema nombrado a través de un broker; cualquier número de suscriptores puede registrar una función para ese tema. El productor no necesita conocerlos y cada consumidor reacciona independientemente. [P:0–2]

El broker mantiene la relación entre nombres de tema y manejadores. En la práctica, el material describe su estructura básica como un mapa de temas a listas de manejadores. Publicar un evento invoca a los manejadores registrados para ese tema y les pasa la carga útil. [P:1–2,4]

Ejemplo de publicación del curso: [P:2]

```javascript
bus.publicar("tweet_publicado", { tweetId: 991, authorId: 42 });
```

Ejemplo de dos suscriptores independientes para el mismo tema: [P:2]

```javascript
bus.suscribirse("nuevo_mensaje", (carga) => renderizarEnBarraLateral(carga));
bus.suscribirse("nuevo_mensaje", (carga) => mostrarNotificacion(carga));
```

La explicación del ejercicio usa `subscribe(topic, handler)` para registrar un manejador y `publish(topic, payload)` para invocar los manejadores del tema con la carga útil. El ejercicio solicita implementar ambos métodos y permitir varios manejadores por tema, pero la extracción no contiene una solución completa. [P:4]

### 3.2 Errores y prácticas recomendadas

La lección agrupa cuatro problemas y una respuesta para cada uno: [P:3]

| Problema | Práctica recomendada |
| --- | --- |
| Nombres ambiguos como `update` o `event` | Usar nombres jerárquicos con espacio de nombres que expresen dominio, entidad y evento; el ejemplo incluye `agent.{id}.token`. |
| Cargas útiles demasiado grandes o poco especificadas | Mantener cargas útiles mínimas y tipadas. |
| Manejadores que asumen que un evento se entregará una sola vez | Hacerlos idempotentes; la fuente sugiere rastrear IDs de eventos e ignorar duplicados. |
| Descartar en silencio eventos que no se pueden procesar | Publicarlos en un tema de mensajes muertos para inspección, depuración y posible reprocesamiento. |

La idempotencia se explica como producir el mismo efecto al procesar un evento repetidamente que al procesarlo una sola vez. La recomendación del tema de mensajes muertos evita ocultar cargas malformadas o versiones desconocidas. [P:3]

## 4. IA en tiempo real con dos canales

### 4.1 Separar salida y control

El flujo de IA combina dos conexiones con responsabilidades distintas:

- **Salida:** SSE o streaming HTTP transmite tokens del servidor al cliente.
- **Control:** WebSocket lleva señales del cliente al servidor, por ejemplo `{ "type": "stop" }`.

El servidor puede abortar la generación al recibir el comando y confirmar por SSE con un evento `stopped`. SSE por sí solo no lleva la señal de vuelta porque el flujo descrito es unidireccional. Las actualizaciones de progreso pueden viajar como eventos SSE o mediante Pub/Sub cuando varios sistemas deban reaccionar. [A:0–2]

### 4.2 Ejercicio `streamWithInterrupt`

La práctica solicita implementar `streamWithInterrupt(rawStream, stopAfterTokens)`. El flujo crudo contiene eventos SSE `token` y termina en `stopped`. La función debe dividirlo en bloques separados por líneas en blanco, leer `event` y `data`, concatenar el `data` de cada token, contar tokens, llamar a `sendStop(tokenCount)` una sola vez al llegar al umbral y devolver el texto acumulado junto con un indicador `stopped`. [A:3]

El material prueba cinco fragmentos (`Hello`, `,`, `world`, `!`, `How`) y un evento `stopped`. Con `stopAfterTokens` en `3`, el resultado esperado es `{ text: 'Hello,world!How', stopped: true }` y las llamadas registradas son `[3]`. El texto contiene los fragmentos tal como llegan, sin añadir espacios. [A:3]

```javascript
const RAW_STREAM = `event: token\ndata: Hello\n\nevent: token\ndata: ,\n\nevent: token\ndata: world\n\nevent: token\ndata: !\n\nevent: token\ndata: How\n\nevent: stopped\ndata: Stream stopped by user\n`;
const stopCalls = [];

function sendStop(tokensSoFar) {
  stopCalls.push(tokensSoFar);
}

function streamWithInterrupt(rawStream, stopAfterTokens) {
  // La fuente entrega esta función como ejercicio con TODO.
  // Requisitos: analizar bloques SSE, acumular tokens y solicitar parada una vez.
  return { text: '', stopped: false };
}

const result = streamWithInterrupt(RAW_STREAM, 3);
console.log(result);
console.log('stop calls:', stopCalls);
```

El código anterior conserva el esqueleto incompleto del ejercicio, no una solución ejecutable. El contrato y el resultado esperado son los datos disponibles en la fuente; no se infiere una implementación ausente. [A:3]

## 5. Flujos agentivos en tiempo real con LangGraph

### 5.1 Modos de streaming

La fuente distingue `graph.invoke(...)`, que devuelve el estado final una vez, de `graph.stream(...)`, que produce datos a medida que el grafo avanza. Los modos descritos son: [G:1]

| Modo | Qué emite | Uso indicado |
| --- | --- | --- |
| `values` | Estado completo en cada paso | Renderizar o consultar una instantánea completa. |
| `updates` | Solo los cambios desde la actualización anterior | Mostrar qué cambió en cada paso. |
| `messages` | Tokens y metadatos de los mensajes generados | Renderizar generación incremental de mensajes. |
| `custom` | Eventos definidos por el desarrollador | Enviar señales específicas del dominio. |

La tarjeta explica que son los modos relevantes cuando una interfaz necesita mostrar datos vivos; cada modo lleva una forma diferente de información. [G:1]

### 5.2 Interrupción y canal de retorno

`interrupt()` pausa la ejecución en un punto crítico y el checkpoint guarda el estado para que el grafo pueda reanudarse. Esos mecanismos definen dónde detenerse y cómo recuperar la ejecución, pero no entregan por sí mismos la solicitud a una persona ni hacen volver su decisión en tiempo real. [G:2]

El flujo descrito añade un canal bidireccional, como WebSocket: el grafo activa la interrupción; la carga útil llega al panel humano; la persona envía su aprobación o rechazo por el mismo canal; el grafo recibe la decisión y reanuda desde el checkpoint con el comando correspondiente. El ejemplo del curso es una transferencia que espera revisión humana. [G:2]

### 5.3 Estado compartido como intermediario Pub/Sub

En la analogía de la fuente, el estado compartido del grafo funciona como broker. Un nodo publica escribiendo en claves de estado; los nodos aguas abajo se suscriben leyendo las claves que declaran como dependencias. Un nodo puede ser publicador, suscriptor o ambos. [G:3]

La disciplina recomendada para cada nodo es declarar sus claves de salida, escribir solo en esas claves, declarar explícitamente sus dependencias de entrada y leer solo las claves declaradas. El ejemplo describe un nodo `planificador` que publica `plan_steps` y nodos `investigador` y `escritor` que consumen ese plan. Leer claves no declaradas introduce acoplamiento oculto. [G:3]

## 6. Cómo relacionar las piezas

| Necesidad | Mecanismo que presenta el material | Razón |
| --- | --- | --- |
| Recibir tokens de IA mientras se generan | SSE o streaming HTTP | Canal de salida servidor → cliente. |
| Detener generación desde la interfaz | WebSocket como canal de control | El cliente debe enviar una señal de vuelta. |
| Notificar a varios consumidores independientes | Pub/Sub | Productor y suscriptores no se conocen entre sí. |
| Mostrar estado o cambios de un grafo en vivo | Modo de streaming de LangGraph | `values`, `updates`, `messages` y `custom` exponen distintas formas de datos. |
| Solicitar revisión humana y reanudar un grafo | `interrupt()` + checkpoint + canal bidireccional | La interrupción guarda el punto de pausa y el canal lleva la solicitud y la respuesta humana. |

Esta tabla relaciona las necesidades descritas por los cursos; no afirma que todas deban implementarse juntas ni prescribe una arquitectura adicional. [W:0–2; P:0–3; A:0–3; G:1–3]

## 7. Glosario de consulta

- **Broker:** intermediario que mantiene suscriptores por tema y distribuye a sus manejadores los eventos publicados. [P:1–2]
- **Checkpoint:** estado guardado del grafo que permite reanudarlo después de una interrupción. [G:2]
- **Heartbeat:** señal periódica usada para detectar o mantener una conexión persistente. [W:3]
- **Idempotencia:** procesar el mismo evento más de una vez produce el mismo efecto que procesarlo una vez. [P:3]
- **Pub/Sub:** patrón en el que publicadores anuncian eventos en temas y suscriptores reaccionan sin que ambos se conozcan directamente. [P:1]
- **WebSocket:** protocolo persistente y bidireccional que se negocia mediante una actualización desde HTTP. [W:1]

## Límites de uso

Este dossier reorganiza y resume el contenido de los cuatro JSON; no incorpora documentación externa. Las estructuras, tablas y relaciones son editoriales. Las prácticas de W:4 y P:4 carecen de soluciones completas en la extracción, y el esqueleto de A:3 permanece deliberadamente incompleto. No hay comandos de terminal ni prompts de OpenClaw en las fuentes de esta clase.