# Guía docente: Clase 66 - Sistemas multiagente con LangGraph

Duración base: 70 minutos, adaptable a 60 o 75. Documento autosuficiente para el profesor.

## Fuentes y límites

Solo se utiliza el contenido de los cinco JSON de esta carpeta. Los tiempos, la secuencia, las preguntas y el guion literal son organización pedagógica; no son nuevas fuentes técnicas.

| Referencia | JSON | Índices utilizados |
| --- | --- | --- |
| I | `introduction_to_multi_agent_systems.json` | 0–5 |
| L | `orchestrating_a_multi_agent_system_in_langgraph.json` | 0–4 |
| C | `communication_and_state_in_multi_agent_systems.json` | 0–7 |
| R | `the_router_pattern.json` | 0–5 |
| W | `building_orchestrator_worker_agents.json` | 0–6 |

La notación `[W:5]` identifica el campo `index` del JSON, no el número que aparece en el título de la tarjeta.

**Límite de la captura:** hay 44 tarjetas y 32 contenidos distintos. I:6 repite I:5; L:5–8 repiten L:4; C:8 repite C:7; R:6–8 repiten R:5; W:7–9 repiten W:6. No se atribuye contenido adicional a esos títulos. Los ejercicios L:4, R:5 y W:6 muestran código de arranque incompleto; sus enunciados sí se capturaron. El ejemplo completo de esta guía procede de W:5.

## Continuidad y objetivos

El hilo docente viene de trabajar con agentes, herramientas y control del flujo. Aquí se conserva esa separación y se amplía a varios roles, interfaces explícitas y estado compartido. La fuente actual permite esta transición sin importar teoría de clases anteriores. [L:0–3]

**Qué decir (literal):** «Hasta aquí podemos pensar en un agente que usa herramientas. Ahora la pregunta es quién debe hacer cada parte del trabajo, qué información recibe y cómo pasa su resultado al siguiente. No vamos a añadir agentes por cantidad: vamos a justificar cada separación».

Al terminar, el estudiante podrá:

- Reconocer roles especializados y transferencias explícitas de estado. [I:2]
- Elegir entre secuencia, paralelización, enrutamiento y orquestador-trabajador según el problema. [I:3–4; L:2]
- Separar pizarra, mensajes de delegación y contexto acotado. [C:1–6]
- Explicar el recorrido de ToolNode y las aristas de un router. [L:3–4; R:3–5]
- Recorrer un grafo completo con `Send`, acumulación de borradores y síntesis. [W:4–5]

## Preparación y contingencia

- Preparar los ejemplos incluidos aquí; no hace falta abrir los JSON durante la explicación.
- El grafo completo conserva `ChatAnthropic(model="claude-sonnet-5")` tal como figura en W:5. La captura no acredita disponibilidad del modelo ni proporciona instalación, credenciales o configuración del entorno. No prometer ejecución sin esas condiciones.
- No hay comandos shell de instalación o ejecución explícitos en estas capturas. No se añaden comandos `pip`, nombres de paquetes instalables ni instrucciones de terminal deducidas.
- No se capturaron prompts de OpenClaw. Los únicos prompts de modelo reproducidos abajo son los del ejemplo W:5.
- Si el entorno no permite la demostración, recorrer el código en pantalla: entrada, plan, envíos, borradores e informe. Esto es una lectura del ejemplo, no una ejecución comprobada.
- No presentar el código de arranque de las prácticas como solución completa. Usar sus pasos de resolución y resultados esperados, incluidos en esta guía.

## Agenda base: 70 minutos

| Minutos | Bloque |
| --- | --- |
| 0–7 | Por qué varios agentes y cuándo no usarlos |
| 7–16 | Elegir la forma del flujo |
| 16–29 | Comunicación, contratos y contexto |
| 29–37 | Del bucle manual a ToolNode |
| 37–47 | Router: clasificar y elegir una sola rama |
| 47–64 | Orquestador-trabajador: código completo |
| 64–70 | Comprobación y cierre |

## 0–7 min: justificar la separación

**Qué decir (literal):** «Un sistema multiagente no es un agente con más herramientas. Son varios roles distintos que colaboran y transfieren estado. Un planificador, un trabajador y un revisor separan decidir, ejecutar y comprobar».

Un agente único puede sufrir sobrecarga de contexto, mezcla de tareas, falta de separación y desviación del objetivo. La orquestación decide quién hace qué, en qué orden y con qué información. Incluye delegación, secuenciación y flujo de datos. [I:0–2]

Empezar con un agente. Añadir otros cuando haya límites observables: instrucciones no relacionadas, responsabilidades mezcladas o partes genuinamente paralelizables. Los beneficios posibles son especialización, contexto más pequeño y verificación independiente. Los costes son latencia, tokens y más puntos de fallo en las transferencias. [I:1,4]

**Ejemplo de la fuente:** dividir «resumir este artículo» entre lector, resumidor y formateador que solo se pasan texto añade coordinación sin hacer el trabajo más claro o verificable. Es sobreorquestación. [I:4–5]

**Pregunta:** «¿Tener diez herramientas ya convierte al agente en multiagente?»

**Respuesta esperada:** no; lo definitorio aquí son varios roles especializados y transferencias explícitas de estado. [I:2,5]

## 7–16 min: elegir la forma del flujo

**Qué decir (literal):** «Primero miramos la forma del problema. Si hay etapas dependientes, usamos secuencia. Si las piezas son independientes, podemos paralelizar. Si hay que escoger un especialista, enrutamos. Si hay que descubrir y repartir varias piezas, usamos un orquestador con trabajadores».

| Patrón | Qué hace | Ejemplo capturado |
| --- | --- | --- |
| Secuencial | La salida de una etapa alimenta la siguiente | Investigación, redacción y edición |
| Paralelización | Procesa piezas independientes y reúne resultados | Resumir varios artículos a la vez |
| Enrutamiento | Clasifica y elige exactamente una rama | Facturación, técnico o general |
| Orquestador-trabajador | Planifica subtareas, delega y sintetiza | Secciones de un informe |
| Evaluador-optimizador | Genera, evalúa y repite hasta cumplir criterios | Redactar y revisar un documento |

Fuente de los cinco patrones: L:2. I:3 también presenta jerarquías: un coordinador organiza subcoordinadores y equipos, como en un lanzamiento de producto. No confundir esa clasificación de cuatro patrones con la lista de cinco de L:2: son dos presentaciones del material, no una lista idéntica.

La orquestación general de I:1 engloba coordinación, orden e información; cuando R:2 contrasta «enrutamiento» con «orquestación», se refiere a elegir una rama frente a descomponer en varias subtareas.

**Pregunta:** «Un ticket necesita un especialista; un informe necesita varias secciones. ¿Es el mismo patrón?»

**Respuesta esperada:** no. El ticket se enruta a un manejador; el informe se descompone y después reúne sus partes. [R:2; W:1]

## 16–29 min: comunicación antes que cantidad de agentes

**Qué decir (literal):** «Aunque cada agente funcione por separado, el sistema puede fallar por lo que se pierde entre ellos. Compartir datos no es lo mismo que delegar una tarea: la pizarra contiene hechos comunes; el mensaje dice qué debe hacerse y qué resultado se espera».

El paso de mensajes envía un paquete autónomo de tarea e insumos. Es explícito y rastreable, pero su formato debe cambiar si faltan datos. La pizarra es un estado compartido, flexible para que varios agentes lean información común, pero requiere controlar las escrituras y el momento de lectura. [C:0–2]

### Un mensaje sin conjeturas

Contrastar la frase de la fuente «El cliente está bastante molesto por un cargo en su pedido reciente, ¿puedes solucionarlo?» con el mensaje estructurado de C:3:

```json
{
  "task": "issue_refund",
  "order_id": 1044,
  "charge_id": "ch_88f2a",
  "amount": 39.90,
  "reason": "duplicate_charge"
}
```

Pedido, cargo, acción e importe están identificados; el receptor no necesita adivinarlos. En varios saltos, la ambigüedad inicial puede acumularse. [C:3]

### Contrato de delegación

La transferencia de C:4 declara tarea, entradas, salida y versión:

```python
handoff = {
    "task": "resumir_tweets",
    "inputs": {"tweet_ids": [12345, 67890]},
    "expected_output_schema": {
        "summary": "str",
        "sentiment_score": "float",
        "key_topics": "list[str]"
    },
    "schema_version": "1.0"
}
```

`task` nombra el trabajo; `inputs` contiene sus datos; `expected_output_schema` declara la forma del resultado; `schema_version` permite detectar cambios incompatibles. La fuente muestra una comprobación que lanza `ValueError` si la versión recibida no coincide con la esperada; no incluye un validador completo de todos los campos. [C:4]

### Contexto mínimo y propiedad de escritura

La pizarra de investigación contiene `sources`, `draft` y `review_notes`: investigador, escritor y revisor son sus respectivos propietarios de escritura. La función de la fuente `write_to_blackboard(state, key, value, agent_id)` comprueba al propietario, lanza `PermissionError` si no corresponde y, si corresponde, asigna `state[key] = value`. No devuelve un resultado explícito. [C:2]

Para comprobar citas no se necesita toda la conversación. C:6 define un estado que también incluye mensajes y `outline`, pero entrega al verificador solo:

```python
def scope_for_citation_checker(state: ResearchState) -> dict:
    return {
        "draft": state["draft"],
        "sources": state["sources"]
    }
```

Es un fragmento de la fuente: presupone la definición de `ResearchState`, no es un programa independiente. Recibe el estado, selecciona dos claves y devuelve ese diccionario. El método de diseño es nombrar la decisión, derivar sus claves mínimas y declarar la proyección. Las herramientas siguen el mismo criterio: el ejemplo `list_open_tickets(runtime: ToolRuntime)` lee solo `runtime.state['assigned_tickets']` y devuelve una cadena con esos tickets. [C:5–6]

**Preguntas:** «¿Qué necesita el verificador de citas?» y «¿Para qué sirve la versión del contrato?»

**Respuestas esperadas:** borrador y fuentes; detectar cambios de esquema antes de que el consumidor interprete datos incompatibles. [C:4,6]

## 29–37 min: del bucle manual a ToolNode

**Qué decir (literal):** «El modelo decide pedir una herramienta. ToolNode ejecuta esa petición y escribe el resultado en el estado. El modelo vuelve a recibir ese estado para continuar. No necesitamos que los nodos se llamen directamente entre sí».

El despacho manual inspecciona llamadas, busca herramientas, las ejecuta, maneja errores y añade resultados. El tutorial presenta `ToolNode` como un nodo reutilizable que recibe herramientas, lee las llamadas del último mensaje del modelo y devuelve resultados estructurados al estado. [L:3]

**Ejercicio capturado, explicado sin completar código externo:** [L:4]

1. Construir `StateGraph(MessagesState)`.
2. Registrar `"model"` con `call_model` y `"tools"` con un `ToolNode` para `get_weather`.
3. Conectar `START` con `"model"`.
4. Conectar la salida condicional de `"model"` usando `tools_condition`.
5. Devolver el flujo de `"tools"` a `"model"`, compilar e invocar.

`get_weather(city: str)` recibe una ciudad y devuelve la cadena fija `It is 22°C and sunny in {city}.`; no consulta un servicio meteorológico real. La entrada documentada es «¿Clima en París?». El resultado esperado es una llamada a la herramienta y una respuesta final que incluya ese clima. El `call_model` capturado es un placeholder que devuelve los mensajes recibidos; no representa la solución funcional del ejercicio. [L:4]

**Pregunta:** «¿Quién ejecuta la herramienta y quién produce después la respuesta final?»

**Respuesta esperada:** ToolNode ejecuta; el nodo modelo retoma el resultado. [L:3–4]

## 37–47 min: router, una sola rama

**Qué decir (literal):** «Clasificar y ejecutar son responsabilidades distintas. El clasificador produce una etiqueta. La función de ruta la lee. El grafo elige un manejador, y ese manejador hace el trabajo».

En la práctica, `State` declara `message`, `category` y `response`. `Route` declara `category: Literal["billing", "technical", "general"]`. `ChatAnthropic(...).with_structured_output(Route)` prepara el clasificador para ese contrato. La etiqueta tipada evita una respuesta libre ambigua; el clasificador recibe solo el mensaje relevante. [R:3,5]

Fragmento de R:4, con formato legible y sin los comentarios de la captura:

```python
from typing_extensions import Literal

def route(state: dict) -> Literal["billing", "technical", "general"]:
    return state["category"]

builder.add_conditional_edges(
    "classify",
    route,
    {
        "billing": "billing",
        "technical": "technical",
        "general": "general"
    }
)
```

`route` recibe el estado y devuelve su categoría. `add_conditional_edges` recibe nodo de origen, función de ruta y mapa etiqueta-destino; registra cómo elegir la siguiente rama después de `classify`. Este fragmento presupone un `builder` y los nodos ya registrados, no es un programa autónomo. [R:4]

**Resolución por pasos de la práctica:** llamar a `router_llm` sobre `state["message"]`, guardar la etiqueta como `category`, devolverla en `route`, registrar el mapa anterior y conectar cada manejador a `END`. El resultado esperado es facturación → `billing`, técnico → `technical` y otros mensajes → `general`. No se inventan mensajes concretos adicionales ni las implementaciones de manejadores no visibles en la captura. [R:5]

**Pregunta:** «¿Un router debería abrir tres ramas a la vez?»

**Respuesta esperada:** no; este patrón selecciona exactamente una. Dividir trabajo requiere otro patrón. [R:1–2]

## 47–64 min: orquestador, trabajadores y sintetizador

**Qué decir (literal):** «Aquí no elegimos un especialista para toda la petición. Primero descubrimos cuántas piezas hay. El orquestador devuelve un plan, cada trabajador recibe una sección, el reductor acumula borradores y el sintetizador los une».

Usar el ejemplo completo de W:5. Se conserva su lógica, modelo, tema y prompts; solo se normaliza el formato y se omiten comentarios.

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_anthropic import ChatAnthropic

class Section(BaseModel):
    name: str = Field(description="Título de esta sección del informe.")
    focus: str = Field(description="Qué debe cubrir esta sección.")

class Plan(BaseModel):
    sections: list[Section]

llm = ChatAnthropic(model="claude-sonnet-5")
planner = llm.with_structured_output(Plan)

class ReportState(TypedDict):
    topic: str
    sections: list
    drafts: Annotated[list, operator.add]
    report: str

def orchestrator(state: ReportState) -> dict:
    plan = planner.invoke(f"Planifica las secciones para un informe sobre: \n{state['topic']}")
    return {"sections": plan.sections}

def assign_workers(state: ReportState):
    return [Send("worker", {"section": section}) for section in state["sections"]]

def worker(state) -> dict:
    section = state["section"]
    text = llm.invoke(f"Escribe la sección '{section.name}': \n{section.focus}").content
    return {"drafts": [f"## {section.name}\n{text}"]}

def synthesizer(state: ReportState) -> dict:
    return {"report": "\n\n".join(state["drafts"])}

builder = StateGraph(ReportState)
builder.add_node("orchestrator", orchestrator)
builder.add_node("worker", worker)
builder.add_node("synthesizer", synthesizer)
builder.add_edge(START, "orchestrator")
builder.add_conditional_edges("orchestrator", assign_workers, ["worker"])
builder.add_edge("worker", "synthesizer")
builder.add_edge("synthesizer", END)

graph = builder.compile()
result = graph.invoke({"topic": "El Futuro de la IA", "sections": [], "drafts": [], "report": ""})
print(result["report"])
```

El nombre local `s` de la comprensión original se desarrolla como `section`; no cambia el envío ni la lógica.

### Cómo explicar las piezas

| Pieza | Recibe | Hace y produce |
| --- | --- | --- |
| `Section`, `Plan` | Declaraciones de campos del plan | Una sección tiene nombre y enfoque; el plan contiene secciones |
| `Field(description=...)` | La descripción del campo | Documenta qué representan `name` y `focus` |
| `with_structured_output(Plan)` | El esquema `Plan` | Prepara `planner`, cuya invocación produce el plan usado por el orquestador |
| `orchestrator` | Estado con `topic` | Invoca al planificador y devuelve `{"sections": plan.sections}` |
| `assign_workers` | Estado con `sections` | Devuelve un `Send("worker", {"section": ...})` por sección |
| `Send` | Nombre del nodo y contexto de esa tarea | Describe cada ejecución trabajadora con su sección acotada |
| `worker` | Una `section` | Solicita su redacción y devuelve una lista de un borrador bajo `drafts` |
| `drafts` con `operator.add` | Listas parciales de trabajadores | Las agrega en vez de sobrescribirlas |
| `synthesizer` | Estado con todos los `drafts` | Devuelve `report`, uniendo textos con dos saltos de línea |
| `StateGraph`, `add_node`, `add_edge` | Esquema, nombres, funciones y conexiones | Definen los nodos y el recorrido del workflow |
| `add_conditional_edges` | Origen, función de envíos y destino trabajador | Conecta la expansión dinámica desde el orquestador |
| `compile`, `invoke` | Grafo definido y estado inicial | Preparan el grafo y lo ejecutan; el ejemplo lee `report` del resultado |

Todo este recorrido procede de W:4–5. El número de trabajadores depende del plan en tiempo de ejecución; el sintetizador de este ejemplo concatena, no hace otra llamada al modelo. El material no fija el texto final ni un número concreto de secciones para «El Futuro de la IA».

### Prompts exactos del ejemplo

Plantillas de W:5; las expresiones entre llaves se sustituyen con los datos del ejemplo:

```text
Planifica las secciones para un informe sobre: 
{state['topic']}
```

```text
Escribe la sección '{section.name}': 
{section.focus}
```

### Práctica alternativa capturada: revisar archivos

En W:6, el ejercicio conecta un trabajador `reviewer` por archivo. El estado contiene `files`, `notes: Annotated[list, operator.add]` y `report`. El orquestador de arranque devuelve `{"notes": []}` porque la lista de archivos ya está en el estado. El trabajador mostrado devuelve `{"notes": [f"reviewed {state['file']}"]}`: es una nota de demostración, no un análisis real del código.

**Pasos de resolución:** producir un `Send` a `reviewer` por cada elemento de `files`, enviar solo su `file`, conectar la expansión con `add_conditional_edges`, añadir `START → orchestrator`, `reviewer → synthesizer` y `synthesizer → END`, compilar en `graph` e invocar con la lista que proporciona la práctica. La captura no muestra esa lista completa ni el código del sintetizador: no se inventan aquí. **Criterio esperado:** una nota por archivo, acumuladas mediante el reductor y fusionadas en el informe. [W:6]

**Preguntas:** «¿Qué rompe si todos sobrescriben `drafts`?» y «¿El orquestador redacta las secciones?»

**Respuestas esperadas:** se pierden aportes; el reductor permite agregarlos. No: el orquestador planifica y delega; los trabajadores redactan. [W:1,4–5]

## 64–70 min: cierre y comprobación

Estas preguntas reformulan conceptos y evaluaciones capturados, no añaden requisitos de proyecto. [I:5; C:7; R:1–2; W:1–5]

1. **¿Qué vuelve multiagente a un sistema?** Roles distintos que colaboran y transfieren estado explícitamente.
2. **¿Qué se guarda en la pizarra y qué se envía como mensaje?** Datos comunes de coordinación frente a delegaciones de tarea.
3. **¿Qué recibe un verificador de citas?** `draft` y `sources`, no todo el historial.
4. **¿Qué diferencia al router del orquestador-trabajador?** Seleccionar un único camino frente a descomponer en varias subtareas y reunir resultados.
5. **¿Qué aporta `Send`?** Un envío por subtarea, con contexto delimitado y cantidad decidida en ejecución.
6. **¿Qué aporta el reductor?** Agrega resultados paralelos sin reemplazar la lista anterior.

**Cierre literal:** «Un sistema multiagente se diseña por sus límites: qué decide cada rol, qué recibe y qué entrega. Si basta un agente, no añadimos más. Si hace falta repartir, elegimos el flujo que corresponda y hacemos explícitas sus transferencias».

## Ajustes de duración

- **60 minutos:** reducir patrones de 9 a 6 minutos; comunicación de 13 a 10; ToolNode de 8 a 6; router de 10 a 8. Se conservan el ejemplo completo, sus contratos y el cierre.
- **75 minutos:** añadir 5 minutos al bloque del grafo completo para recorrer la práctica de revisión de archivos y contrastar `notes` con `drafts`, sin introducir código no capturado.

## Checklist final del profesor

- Se explicó por qué un agente puede ser suficiente y qué cuesta añadir otros.
- Se distinguió selección de rama de descomposición de trabajo.
- Se identificaron entradas, salidas, propietarios de escritura y contexto mínimo.
- Se recorrieron ToolNode, router y el grafo completo sin presentar placeholders como soluciones.
- Se distinguió el resultado esperado de una ejecución realmente comprobada.
- No se añadieron comandos, prompts, modelos alternativos ni teoría externa.