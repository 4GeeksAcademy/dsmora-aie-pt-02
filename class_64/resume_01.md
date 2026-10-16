# Guía docente — Clase 64: Memoria y arquitecturas para agentes de IA

> Duración base: 70 minutos. Fuente técnica exclusiva: `memory_for_ai_agents.json` y `agent_memory_architectures.json`. La secuencia, los tiempos y las preguntas son estructura docente; los conceptos y ejemplos técnicos proceden de esos JSON.

## Continuidad y objetivo

La clase 63 trabajó MCP, clientes y servidores; esta sesión cambia el foco desde las capacidades que el agente puede utilizar hacia la información que necesita recordar. Frase de transición: «Ya vimos cómo conectar un agente con capacidades externas; ahora diseñaremos qué contexto conserva, durante cuánto tiempo y con qué arquitectura».

Al finalizar, el estudiante podrá:

- Clasificar información por alcance temporal y patrón de acceso.
- Diferenciar ventana de contexto, memoria episódica, memoria externa, grafos de conocimiento, memoria paramétrica y memoria auto-mejorable.
- Elegir una arquitectura o combinación y justificar sus compensaciones.
- Explicar por qué la memoria debe gestionarse con operaciones explícitas de lectura y escritura.

## Preparación del profesor

- Tener a mano los dos JSON de esta clase y los fragmentos de código incluidos abajo.
- No se necesita preparar un entorno de ejecución: las fuentes no especifican comandos de instalación ni ejecución para estos ejemplos.
- Las fuentes no contienen prompts de OpenClaw. No se incluye uno para evitar inventar instrucciones ajenas al material; la demostración es de análisis y diseño sobre los casos del curso.

## Agenda de 70 minutos

- **0–5 min | Continuidad y problema:** distinguir un agente sin estado de uno que conserva información útil.
- **5–13 min | Diseñar desde el patrón de acceso:** responder qué recordar, por cuánto tiempo y por qué.
- **13–20 min | Memoria como componente:** separar alcances y operaciones explícitas de lectura/escritura.
- **20–29 min | Contexto y memoria episódica:** contrastar memoria de sesión con persistencia entre sesiones.
- **29–43 min | Memoria externa y grafos:** elegir entre similitud semántica y relaciones explícitas.
- **43–51 min | Memoria paramétrica y auto-mejorable:** distinguir conocimiento estable de mantenimiento de memoria persistente.
- **51–65 min | Taller de selección:** clasificar escenarios, combinar arquitecturas y justificar compensaciones.
- **65–70 min | Cierre:** recapitular el método de diseño y comprobar comprensión.

## Guion de clase

### 0–5 min: el problema

**Qué decir (literal):** «Un agente sin estado puede volver a preguntar quién eres o releer el mismo archivo en cada interacción. La memoria del agente es la información que almacena y recupera deliberadamente para conservar contexto, personalizar respuestas y mantener continuidad».

**Pregunta:** «¿Qué cambia entre recordar algo durante una conversación y poder recuperarlo cuando el usuario regresa otro día?»

Recoger las respuestas y anticipar que el curso separa memoria dentro de una sesión, entre sesiones y conocimiento permanente.

### 5–13 min: requisito primero

**Qué decir (literal):** «No empezamos eligiendo una base de datos. Primero preguntamos: ¿qué debe recordar el agente?, ¿por cuánto tiempo?, ¿y qué decisión o comportamiento debe apoyar esa memoria?»

Presentar la regla del curso: el patrón de acceso es la entrada y la arquitectura es la salida. Clasificar la información según su alcance: efímera/dentro de la sesión, entre sesiones o permanente. Añadir que también importa si se trata de historial/preferencias, conocimiento amplio, relaciones o comportamiento estable.

**Pregunta de chequeo:** «¿Por qué no elegir Redis, una base vectorial o ajuste fino antes de saber qué se necesita recordar?»

**Respuesta esperada:** porque la arquitectura debe responder al requisito y al uso; la herramienta no determina por sí sola el patrón de memoria adecuado.

### 13–20 min: componente de sistema

**Qué decir (literal):** «La memoria no es texto que acumulamos sin control dentro del prompt. El material la presenta como un componente del sistema, con ámbitos y operaciones explícitas de lectura y escritura».

Explicar la separación descrita en el curso: ventana de contexto para datos de la interacción actual; almacén episódico para preferencias e historial entre sesiones; conocimiento externo o paramétrico para información estable o extensa. En vez de concatenarlo todo, el agente puede leer la memoria cuando la necesita y escribir actualizaciones de forma explícita.

La fuente incluye un ejemplo más amplio de estas interfaces y su uso desde el flujo de un agente:

```javascript
// Memoria episódica para preferencias de usuario
class EpisodicMemory {
  constructor(store) {
    this.store = store; // por ejemplo, Redis o base de datos clave-valor
  }

  async saveUserPreference(userId, preference) {
    await this.store.set(`user:${userId}:preference`, JSON.stringify(preference));
  }

  async getUserPreference(userId) {
    const data = await this.store.get(`user:${userId}:preference`);
    return data ? JSON.parse(data) : null;
  }
}

// Operación de lectura de ventana de contexto (efímera, en memoria)
function readCurrentThread(session) {
  return session.currentThreadMessages;
}

// Recuperación semántica de memoria externa
class ExternalMemory {
  constructor(vectorDB) {
    this.vectorDB = vectorDB;
  }

  async searchKnowledgeBase(query) {
    return await this.vectorDB.query(query, { topK: 3 });
  }
}

// Pipeline de procesamiento del agente usando interfaces explícitas de memoria
async function agentProcess(userId, session, query) {
  const episodic = new EpisodicMemory(redisClient);
  const external = new ExternalMemory(vectorDBClient);

  const userPref = await episodic.getUserPreference(userId);
  const currentThread = readCurrentThread(session);
  const kbResults = await external.searchKnowledgeBase(query);

  const prompt = `Preferencias del usuario: ${JSON.stringify(userPref)}\n` +
                 `Conversación hasta ahora: ${currentThread.join('\n')}\n` +
                 `Fragmentos de la base de conocimiento: ${kbResults.map(d => d.text).join('\n')}`;

  const response = await callLLM(prompt);

  if (response.includes('actualización de preferencia')) {
    await episodic.saveUserPreference(userId, extractPreference(response));
  }

  return response;
}
```

`saveUserPreference` serializa y persiste una preferencia; `getUserPreference` la recupera y devuelve el objeto o `null`. `readCurrentThread` devuelve los mensajes de la sesión. `searchKnowledgeBase` consulta la base vectorial con `topK: 3`. `agentProcess` combina esos resultados en el prompt, llama al modelo y guarda una preferencia si la respuesta contiene la frase indicada. El ejemplo fuente no define `redisClient`, `vectorDBClient`, `callLLM` ni `extractPreference`; úsalo para analizar la arquitectura, no como programa listo para ejecutar.

**Pregunta:** «¿Qué se gana al tener operaciones claras para leer y escribir?»

**Respuesta esperada:** claridad y mantenibilidad; además, se puede gestionar cada ámbito de memoria de forma explícita.

### 20–29 min: contexto y episodios

La ventana de contexto contiene lo que el modelo procesa en una llamada: conversación actual, instrucciones del sistema y fragmentos recuperados. Es memoria dentro de la sesión, sin persistencia externa, adecuada cuando toda la tarea cabe en una interacción; el curso da como ejemplos resumir un artículo pegado, una revisión rápida de código con toda la información disponible y una extracción puntual.

La memoria episódica persiste entre sesiones y puede guardar preferencias e historial personalizado. El curso menciona Redis, almacenes clave-valor simples y caché de prompts como opciones de backend. Mostrar el fragmento de Redis sin presentarlo como programa completo:

```javascript
// Guardar preferencias del usuario
redis.set(`user:${userId}:preferences`, JSON.stringify(preferences))
// Recuperar preferencias del usuario
const prefs = JSON.parse(redis.get(`user:${userId}:preferences`))
```

**Qué decir (literal):** «La clave identifica las preferencias del usuario; al guardar se serializan y al recuperar se vuelven a interpretar como JSON. El ejemplo muestra la intención de lectura y escritura; no incluye la configuración de Redis».

Señalar el problema de crecimiento: un historial sin control puede volver la recuperación más lenta y ruidosa. El material propone políticas de expulsión y resumir entradas antiguas cuando se supera un límite:

```javascript
if (userHistory.length > MAX_HISTORY) {
  userHistory = summarize(userHistory) // Comprime entradas antiguas
  redis.set(`user:${userId}:history`, JSON.stringify(userHistory))
}
```

**Pregunta:** «¿Qué arquitectura usarían para resumir un contrato pegado una sola vez? ¿Y para recordar el nombre de un cliente que vuelve?»

**Respuesta esperada:** ventana de contexto para el contrato en una sesión; memoria episódica para preferencias del cliente entre sesiones.

### 29–43 min: conocimiento externo y relaciones

La memoria externa permite recuperar conocimiento alojado fuera de la ventana inmediata. El curso describe bases vectoriales que almacenan embeddings de documentos o fragmentos; la consulta también se convierte en embedding y se recuperan fragmentos semánticamente similares para incorporarlos al contexto. Se recomienda cuando el corpus es demasiado grande para cargarlo entero.

Un grafo de conocimiento representa entidades como nodos y relaciones tipadas como aristas. Es preferible cuando la pregunta depende de dependencias, jerarquías o causalidad, en vez de similitud semántica. Usar el ejemplo de servicios DevOps del JSON:

```cypher
// Crear nodos de servicio
CREATE (auth:Service {name: 'AuthService'})
CREATE (payment:Service {name: 'PaymentService'})

// Definir dependencia: PaymentService depende de AuthService
CREATE (payment)-[:DEPENDS_ON]->(auth)

// Encontrar los servicios que dependen de AuthService
MATCH (s:Service {name: 'AuthService'})<-[:DEPENDS_ON*]-(dependent)
RETURN dependent.name
```

**Qué decir (literal):** «La base vectorial recupera por similitud; el grafo pregunta por una relación explícita. Si preguntamos qué servicios dependen de AuthService, necesitamos recorrer `DEPENDS_ON`, no buscar texto parecido».

**Preguntas:** «¿Qué usarían para buscar en miles de manuales?» y «¿Qué usarían para saber qué componentes se rompen si se apaga AuthService?»

**Respuestas esperadas:** memoria externa/RAG para documentos amplios; grafo de conocimiento para dependencias explícitas.

### 43–51 min: conocimiento incorporado y mantenimiento

La memoria paramétrica incorpora conocimiento o comportamiento en los pesos mediante ajuste fino. Es más apropiada para información estable o estilo/comportamiento que justifique el coste de reentrenar; cambia al volver a entrenar o ajustar el modelo.

La memoria auto-mejorable mantiene un almacén a lo largo del tiempo. Describir el ciclo del material: agrupar recuerdos similares, fusionar duplicados, resumirlos, puntuarlos por relevancia o frescura y eliminar los de poco valor o desactualizados. Antes de confirmar actualizaciones, el curso propone una puerta de revisión humana para aprobarlas o rechazarlas. El ciclo puede activarse por tareas programadas o eventos, y las acciones deben quedar registradas.

El JSON también muestra el control de aprobación en pseudocódigo:

```javascript
function proponerActualizacionMemoria(actualizacion) {
  presentarAlUsuario(actualizacion);
  if (usuarioConfirma()) {
    confirmarActualizacion(actualizacion);
  } else {
    descartarActualizacion(actualizacion);
  }
}
```

La función presenta la actualización, la confirma si el usuario acepta y la descarta en caso contrario; las funciones auxiliares se nombran en el JSON, pero no se implementan allí.

**Qué decir (literal):** «Una arquitectura almacena el comportamiento dentro del modelo; la otra mantiene y depura el almacén de memoria. No son la misma operación».

### 51–65 min: taller de selección

Pedir al grupo que responda para cada caso: qué recordar, por cuánto tiempo, por qué, arquitectura y compensación aceptada.

1. Resumir un contrato pegado en una sesión y no conservarlo después: ventana de contexto.
2. Saludar a clientes recurrentes por su nombre y evitar repetir preguntas: memoria episódica.
3. Consultar un corpus extenso de documentación: memoria externa.
4. Consultar dependencias entre servicios: grafo de conocimiento.
5. Mantener un estilo de respuesta estable que justifique reentrenamiento: memoria paramétrica.
6. Resumir, fusionar y eliminar recuerdos de baja relevancia con una revisión antes de confirmar cambios: memoria auto-mejorable.

Después, presentar las combinaciones del curso: un agente de soporte usa ventana de contexto para el ticket actual, memoria episódica para el perfil del cliente y memoria externa para artículos de ayuda. Un asistente de programación puede usar un grafo para dependencias y memoria externa para documentación.

**Qué preguntar después:** «¿Qué compensación aceptarías y por qué: latencia frente a persistencia, coste frente a frecuencia de actualización, o complejidad frente a precisión?»

**Pistas esperadas:** el contexto es rápido pero efímero; el ajuste fino es costoso y lento de actualizar; los grafos requieren modelado previo y son adecuados para relaciones.

### 65–70 min: cierre

**Cierre sugerido (literal):** «La arquitectura correcta no es la más nueva ni una única solución universal. Primero definimos qué necesita recordar el agente, durante cuánto tiempo y para qué; después elegimos una arquitectura o combinación y explicamos qué compensación aceptamos».

Comprobar que cada estudiante puede distinguir entre similitud semántica y relaciones explícitas, y elegir una arquitectura para un caso indicando el alcance temporal.

## Recorte a 60 o extensión a 75

- **Para 60 minutos:** reducir la explicación inicial a 3 minutos y el bloque paramétrica/auto-mejorable a 6; conservar el taller, pero trabajar cuatro casos: contrato, cliente recurrente, documentación extensa y dependencias.
- **Para 75 minutos:** dedicar 5 minutos adicionales al taller. Cada grupo diseña la memoria por capas para el agente de soporte o el asistente de programación del curso y defiende una compensación.

## Contingencia y límites de la fuente

Si no se ejecuta código, usar los fragmentos como lectura guiada: identificar clave, serialización, persistencia, nodos y relación. No prometer ejecución funcional: los JSON no incluyen configuración de Redis ni comandos de instalación. Tampoco contienen instrucciones o prompts de OpenClaw, por lo que la guía no inventa una demo con esa herramienta.

La primera fuente aporta la definición y motivación de memoria del agente en una lección introductoria; la segunda desarrolla las arquitecturas, sus usos, ejemplos y evaluación. Las demos Redis y Cypher reproducen ejemplos presentes en `agent_memory_architectures.json`.