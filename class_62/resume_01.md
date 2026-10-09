# Guía docente: Clase 62 - Ingeniería agéntica y LangGraph

Sesión online de 70 minutos, ajustable a 60 o 75. Esta guía se construye únicamente con los tres JSON extraídos para `class_62`.

## Objetivos de aprendizaje

Al finalizar, el estudiante podrá:

- Describir un agente como un sistema de modelo, estado, herramientas y bucle de control.
- Explicar cómo el sistema ejecuta una llamada a herramienta y reinserta su resultado antes de continuar.
- Identificar cómo el enrutamiento, los errores y las condiciones de parada hacen más robusto un agente.
- Relacionar estado, nodos, aristas, compilación e invocación en un agente construido con LangGraph.
- Explicar qué aportan los puntos de control, las interrupciones, los rastreos y las evaluaciones.

## Preparación del profesor

- Tener esta guía a la vista y usar los ejemplos incluidos como material de exposición.
- No se necesita instalar ni ejecutar nada para impartir la secuencia conceptual.
- Los ejemplos de LangGraph presuponen que `llm` y `tools` ya existen; los JSON no especifican su configuración, proveedor, instalación ni credenciales. No presentar esos fragmentos como un programa autónomo listo para ejecutar.
- Los JSON no incluyen comandos de terminal para instalar o lanzar el ejemplo, ni prompts de OpenClaw. No añadirlos como pasos de clase.
- Plan de contingencia: si no se puede mostrar código, recorrer el flujo en voz alta con el ejemplo de consultar el clima en Madrid y pedir al grupo que identifique modelo, estado, herramienta, ruta y condición de parada.

:::floating-note
## Puentes con clases anteriores

Ten estas conexiones a mano mientras avanzas por la clase 62:

- **Clase 17 — Introducción a OpenClaw:** ya vimos un agente que puede realizar tareas de varios pasos. El **Gateway** recibe y enruta mensajes, y participa en la ejecución de herramientas. Conecta esa arquitectura con la idea de hoy: el modelo propone una acción, pero el sistema que lo rodea gestiona el flujo.
- **Clase 18 — Tareas simples + Telegram/Composio MCP:** las **skills** describen procedimientos para tareas repetibles; MCP/Composio permite conectar acciones con servicios externos. Relaciónalo con las herramientas de clase 62: funciones con entradas y salidas definidas que el agente solicita y el sistema ejecuta.
- **Clase 23 — Arquitectura avanzada y skills de OpenClaw:** el workspace y archivos como `TOOLS.md` aportan contexto sobre las capacidades del agente; las skills organizan instrucciones reutilizables. En clase 62 daremos el siguiente paso y veremos el ciclo de ejecución: detectar la solicitud estructurada, llamar la herramienta, devolver el resultado al modelo y decidir si continúa o termina.

**Nota para explicar:** una skill de OpenClaw no es exactamente lo mismo que una función/herramienta tipada del ejemplo de clase 62. La conexión es conceptual: ambas ayudan a que el agente realice tareas; hoy nos centraremos en cómo el sistema ejecuta y enruta las llamadas a herramientas.
:::

## Agenda de 70 minutos

| Tiempo | Bloque |
|---|---|
| 0-5 min | Apertura: de una respuesta a un sistema que actúa |
| 5-14 min | Componentes del agente y anatomía del grafo |
| 14-26 min | Bucle agentico y ejecución de herramientas |
| 26-36 min | Evolución por capas, registro, errores y límites |
| 36-55 min | Construcción conceptual de un agente LangGraph |
| 55-64 min | Interrupciones, puntos de control, rastreo y evaluación |
| 64-70 min | Comprobación de conocimientos y cierre |

## Guion para impartir

### 0-5 min | Apertura

**Qué decir (literal):**

> «Hoy vamos a pasar de pensar en una llamada aislada a un modelo a pensar en un sistema que conserva estado, usa herramientas y controla su propio ciclo. Después veremos cómo expresar ese flujo como un grafo explícito con LangGraph.»

Introduce la secuencia de la sesión: qué compone un agente, cómo funciona su bucle, qué problemas aparecen al crecer y cómo LangGraph organiza nodos y transiciones.

**Pregunta de entrada:** «¿Qué puede hacer un sistema que una llamada única a un modelo no hace por sí sola?»

### 5-14 min | Componentes y anatomía

**Qué decir (literal):**

> «Un agente no es solo el LLM. El modelo señala qué hacer; el sistema conserva el estado, ejecuta las herramientas y controla las transiciones hasta obtener una respuesta final.»

Explica los componentes según los materiales:

- **LLM/modelo:** procesa la entrada y señala la siguiente acción; no es el sistema completo.
- **Estado:** información que el agente mantiene entre pasos. En un grafo debe ser explícito y contener lo que necesita el siguiente paso; evitar que crezca sin límites.
- **Herramienta:** función tipada que realiza una acción o consulta datos externos. Debe tener entradas y salidas definidas y una responsabilidad estrecha; conviene que los reintentos no dupliquen efectos y que las llamadas tengan límite de tiempo.
- **Bucle:** el control que envía el contexto al modelo, ejecuta herramientas solicitadas y continúa hasta que el modelo termina.
- **Grafo:** nodos para pasos de trabajo y aristas dirigidas para transiciones. Compilar valida la estructura antes de ejecutar.

Usa el ejemplo del material: para una consulta del clima, el estado puede guardar `location` y `temperature`; un nodo llama al modelo, otro ejecuta la herramienta y una arista condicional decide qué ocurre después.

**Qué preguntar después:** «¿Qué diferencia hay entre un nodo y una arista?» Respuesta esperada: el nodo realiza un paso; la arista conecta y enruta entre pasos.

### 14-26 min | Bucle agentico

**Qué decir (literal):**

> «El modelo solicita una herramienta, pero el sistema es quien la ejecuta. El resultado vuelve al historial y el modelo recibe ese contexto en la siguiente iteración. Si ya no hay una solicitud de herramienta, se devuelve la respuesta final.»

Recorre este orden: enviar historial y prompt del sistema; recibir respuesta; detectar la solicitud mediante señales estructuradas de la API; ejecutar la función solicitada; añadir el resultado vinculado al identificador de la llamada; repetir o terminar.

Ejemplo simplificado del JSON de implementación:

```python
while True:
    response = client.messages.create(
        model="your-model",
        system=system_prompt,
        tools=[get_weather_tool],
        messages=messages,
        temperature=0.1,
        max_tokens=1024,
    )

    if response.stop_reason == "tool_use":
        tool_block = next(block for block in response.content if block.type == "tool_use")
        result = execute_tool(tool_block.name, tool_block.input)
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tool_block.id, "content": str(result)}
        ]})
    else:
        print(response.content[0].text)
        break
```

Explica que `client.messages.create` recibe modelo, prompt del sistema, herramientas, historial y parámetros; devuelve una respuesta. `stop_reason == "tool_use"` y un bloque `tool_use` indican la llamada. `execute_tool` recibe nombre y entrada; su resultado se añade al historial como `tool_result`. Si no hay llamada, se imprime el texto y termina el bucle. El ejemplo usa nombres de modelo y variables de ejemplo tal como aparecen en el material; no aporta configuración de cliente ni definición de herramientas.

Los JSON mencionan `stop_reason` y un bloque `tool_use` para Anthropic, y `finish_reason` con `function_call` para OpenAI. Enfatiza que se usan señales estructuradas, no se busca texto libre para adivinar si hubo llamada.

**Qué preguntar después:** «¿Qué se añade al historial antes de la siguiente vuelta?» Respuesta esperada: la respuesta del asistente y el resultado de herramienta asociado a su llamada.

### 26-36 min | De una herramienta a un agente robusto

**Qué decir (literal):**

> «Construimos por capas: primero verificamos una herramienta aislada, luego dejamos que el modelo decida cuándo usarla y después añadimos el bucle de varios turnos. Solo entonces escalamos a varias herramientas y manejo explícito de fallos.»

Presenta el esquema de herramienta (`name`, `description`, `input_schema`) y el ejemplo `get_weather` con una entrada `city`. Para varias herramientas, el registro asocia nombres con funciones:

```python
tool_registry = {
    "get_weather": get_weather,
    "get_news": get_news
}

result = tool_registry[tool_block.name](**tool_block.input)
```

Describe el patrón: despachar por nombre en vez de añadir una cadena creciente de condiciones. Si la herramienta falla, capturar la excepción y devolver al modelo un error estructurado y claro, no un rastro crudo. Añadir una condición de parada, como un máximo de iteraciones; el material muestra `max_iterations = 10` como ejemplo. El bucle ingenuo es más difícil de extender, mantiene el estado implícito y no conserva progreso ante caídas.

**Qué preguntar después:** «¿Qué problema evita el límite de iteraciones?» Respuesta esperada: que el agente siga ejecutándose indefinidamente.

### 36-55 min | Construcción conceptual con LangGraph

**Qué decir (literal):**

> «LangGraph hace explícitos el estado y el flujo: definimos qué información circula, qué trabajo hace cada nodo y qué arista se toma. La compilación valida el grafo; la invocación lo ejecuta con un estado inicial.»

Explica el ejemplo por etapas, sin presentarlo como script autocontenido: `llm` y `tools` son dependencias que el fragmento da por existentes.

1. El estado es un `TypedDict` con una lista de mensajes. `Annotated` junto con `add_messages` indica cómo acumular actualizaciones.
2. `llm.bind_tools(tools)` vincula las herramientas al modelo. `call_model(state)` invoca el modelo con los mensajes y devuelve el mensaje nuevo. `ToolNode(tools)` ejecuta las llamadas solicitadas.
3. `StateGraph(AgentState)` crea el grafo; `add_node` registra los nodos y `add_edge(START, "agent")` marca el comienzo.
4. `should_continue` mira el último mensaje: si hay `tool_calls`, dirige a `tools`; si no, devuelve `END`. Después de ejecutar herramientas, el grafo vuelve a `agent`.
5. `graph.compile()` valida nodos, aristas y punto de entrada. `app.invoke(initial_state)` ejecuta el grafo y devuelve el estado final.

Fragmento representativo del JSON:

```python
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def should_continue(state: AgentState) -> str:
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END

graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")
app = graph.compile()
```

El estado inicial del ejemplo contiene un `HumanMessage` con «¿Cuál es el clima en Madrid?». La salida documentada es el estado final después de recorrer los nodos; el material no fija un texto concreto de respuesta.

**Qué preguntar después:** «¿Qué decide `should_continue` y dónde se ejecuta la herramienta?» Respuesta esperada: decide entre `tools` y `END` según `tool_calls`; las ejecuta `ToolNode`.

### 55-64 min | Resiliencia y observabilidad

**Qué decir (literal):**

> «Un agente fiable no solo llega a una respuesta: debe poder pausar cuando necesita criterio humano, conservar progreso ante interrupciones y dejar evidencia para entender cómo tomó sus decisiones.»

Resume los mecanismos que aparecen en los fundamentos:

- **Interrupción / human in the loop:** ante ambigüedad, guardar el estado, pedir aclaración y reanudar incorporando la respuesta humana.
- **Yield:** transmitir resultados parciales mientras el agente sigue trabajando.
- **Checkpoint:** guardar el progreso para continuar tras fallos o reinicios. El ejemplo de LangGraph agrega `InMemorySaver` al compilar.
- **Rastreo:** registrar entradas y salidas de nodos, llamadas y resultados de herramientas, instantáneas del estado, transiciones y tiempos.
- **Evaluación:** verificar automáticamente si el comportamiento fue correcto para una entrada. El material conecta rastreos, evaluaciones y aptitud como medios para observar y mejorar el comportamiento.

No añadas configuración de persistencia ni herramientas externas: el contenido solo muestra `graph.compile(checkpointer=InMemorySaver())` como ejemplo de checkpointing en memoria.

**Qué preguntar después:** «¿Qué evidencia buscarías en un rastreo para entender por qué el agente eligió una ruta?» Respuesta esperada: estado, salida del nodo, llamada/resultados de herramientas y transiciones.

### 64-70 min | Comprobación y cierre

Haz una comprobación oral breve:

- ¿Quién ejecuta el flujo: el LLM o el sistema que lo rodea? **El sistema; el LLM señala intención.**
- ¿Qué es un nodo? **Un paso de procesamiento con una responsabilidad clara.**
- ¿Por qué usar un registro de herramientas? **Para mapear nombres de herramientas a funciones y despachar dinámicamente.**
- ¿Qué valida `compile()`? **La estructura del grafo, incluidos nodos, aristas y punto de entrada.**
- ¿Qué evita un checkpoint? **Perder el progreso si el proceso falla a mitad de ejecución.**

**Cierre sugerido (literal):**

> «La idea central es que el LLM forma parte del agente, pero el sistema define el estado, ejecuta herramientas, controla las rutas y decide cuándo terminar. LangGraph expresa ese control mediante un grafo que se puede validar antes de invocar.»

## Ajuste de duración

- **Para 60 minutos:** reducir apertura a 3 min, componentes a 8 min, bucle a 10 min, escalado a 8 min y observabilidad a 5 min. Mantener el recorrido completo de LangGraph y las preguntas de cierre.
- **Para 75 minutos:** añadir 5 min al bloque de LangGraph para que el grupo trace en papel el recorrido `START → agent → tools → agent → END` usando el ejemplo del clima; pedir que justifique cada transición con la condición `tool_calls`.

## Límites del material fuente

Los JSON contienen ejemplos Python, pero no comandos de shell de instalación o ejecución, prompts de OpenClaw, código de configuración de `llm`/`tools` ni credenciales. Por trazabilidad, esta guía no inventa esos pasos ni afirma que los fragmentos sean ejecutables sin esas dependencias. No se proporciona un brief de proyecto para esta clase.

En los tres JSON, la última lección («Qué viene después» / «What comes next») repite exactamente el contenido de la comprobación de conocimientos anterior. Tratarla como duplicado del scraping, no como contenido nuevo.