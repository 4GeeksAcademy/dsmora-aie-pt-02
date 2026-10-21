# Dossier ampliado para NotebookLM: Sistemas multiagente con LangGraph

## Alcance y procedencia

Este documento es una fuente de consulta en español, no un guion con tiempos ni un cuaderno ejecutable. Integra y desarrolla únicamente lo extraído de los cinco tutoriales de la clase 66. Las explicaciones, ejemplos, nombres de APIs y resultados esperados proceden de sus JSON. Los encabezados, la secuencia comparativa, las preguntas y la organización de consulta son elaboración editorial.

La ampliación consiste en relacionar lo que las fuentes ya contienen: decisión de separar agentes, formas del flujo, comunicación, contratos, contexto mínimo, ejecución de herramientas, enrutamiento y trabajo paralelo dinámico. No incorpora bibliografía externa, otras clases, soluciones inventadas ni prácticas de producción que las capturas no desarrollan.

### Convención de referencias

| Código | Archivo fuente | Contenido distinto disponible |
| --- | --- | --- |
| I | `introduction_to_multi_agent_systems.json` | Índices 0–5: fundamentos, patrones, selección y evaluación |
| L | `orchestrating_a_multi_agent_system_in_langgraph.json` | Índices 0–4: workflows, patrones, ToolNode y ejercicio |
| C | `communication_and_state_in_multi_agent_systems.json` | Índices 0–7: comunicación, pizarra, contratos, contexto y evaluación |
| R | `the_router_pattern.json` | Índices 0–5: clasificación, ruta condicional y ejercicio |
| W | `building_orchestrator_worker_agents.json` | Índices 0–6: roles, Send, reductor, grafo completo y ejercicio |

Una referencia como `[C:4]` corresponde al campo `index` del JSON. No indica la posición visual de una tarjeta ni una celda de notebook.

### Calidad de la extracción

Se capturaron 44 tarjetas y 32 cuerpos de contenido distintos. Las siguientes tarjetas no aportan una lección independiente:

- I:6 contiene de nuevo la evaluación I:5.
- L:5, L:6, L:7 y L:8 repiten la práctica L:4.
- C:8 repite la evaluación C:7.
- R:6, R:7 y R:8 repiten la práctica R:5.
- W:7, W:8 y W:9 repiten la práctica W:6.

Por tanto, no se reconstruyen lecciones de lectura de estado desde herramientas a partir de los títulos repetidos de L, ni lecciones de router u orquestador-trabajador en producción a partir de R:6 o W:7. El acceso a estado con `ToolRuntime` sí aparece en C:5–6 y se explica desde esa fuente.

Los editores de las prácticas aparecen como texto concatenado y con código incompleto. Se pueden recuperar sus objetivos y algunos fragmentos, pero no se afirma que contengan soluciones terminadas. W:5 sí contiene un ejemplo completo de grafo. Conservar el código de la fuente tampoco demuestra que se haya ejecutado: las capturas no proporcionan instalación, credenciales ni comprobación de disponibilidad del modelo.

## 1. El problema que motiva varios agentes

Un agente generalista puede manejar tareas coherentes con un grupo pequeño de herramientas relacionadas. La dificultad aparece cuando debe mantener instrucciones heterogéneas, planificar, ejecutar y verificar al mismo tiempo, o cubrir varias especialidades. I:0 identifica cuatro señales: sobrecarga de contexto, mezcla de tareas, falta de separación y desviación del objetivo en tareas largas. [I:0; L:1]

El ejemplo de programación reparte el trabajo entre planificador, editor y tester. El de soporte separa facturación y devoluciones. El de investigación distribuye fuentes entre trabajadores y recoge hallazgos. Lo común no es el nombre de los agentes, sino una responsabilidad delimitada y una forma explícita de colaboración. [I:0–2]

Un sistema multiagente es una colección de agentes especializados que colaboran y transfieren trabajo para lograr un objetivo que un solo agente no resolvería de manera suficientemente confiable. Añadir herramientas o repetir dos veces el mismo agente no expresa por sí solo esa separación de roles y estado. La evaluación de la fuente destaca como rasgo definitorio los roles distintos y nombrados que colaboran y transfieren estado. [I:0,2,5]

### 1.1 Qué significa orquestar

Orquestar es decidir quién hace qué, en qué orden y con qué información. La definición incluye tres dimensiones: delegación de subtareas, secuenciación de las actuaciones y gestión del flujo de información. El coordinador conserva el objetivo, divide el trabajo, selecciona responsables, recoge resultados y decide los siguientes pasos. [I:1]

En el ejemplo de vacaciones, se buscan vuelos, se utiliza esa información para buscar hoteles y después se prepara un itinerario. La coordinación mantiene la relación entre las etapas; no se trata de producir respuestas aisladas que luego casualmente coincidan. [I:1]

### 1.2 Beneficios y costes

La división puede aportar especialización, contextos más pequeños y verificación independiente. Cada agente trabaja en un rol más estrecho y otro puede comprobar su salida. Pero también aparecen llamadas adicionales, consumo de tokens, latencia y más puntos donde un traspaso puede perder o corromper datos. [I:1,4]

La recomendación del material es empezar con un agente y añadir otros ante un límite real. Procesar cincuenta documentos presenta trabajo paralelizable. En cambio, separar un resumen sencillo entre lector, resumidor y formateador que solo intercambian texto es el ejemplo de sobreorquestación: aumenta coordinación sin aclarar ni verificar mejor el trabajo. [I:4–5]

La decisión no es «más agentes equivale a mejor resultado». Es comprobar si la separación corresponde a especialidades distintas, instrucciones incompatibles o piezas verdaderamente independientes. [I:4; L:1]

## 2. Workflow y control del flujo

Un workflow de agentes conecta modelos de lenguaje y herramientas mediante un proceso definido para cumplir una tarea. L:1 plantea una pregunta central: quién controla la secuencia de acciones.

En un extremo, el desarrollador codifica las rutas y el modelo produce contenido dentro de ellas. En el otro, el modelo elige herramientas o agentes en puntos de decisión, dentro de opciones predefinidas. La fuente indica que muchos sistemas combinan estructura predecible y decisiones guiadas por el modelo. [L:1]

Los principios de separación son un propósito por agente, interfaces explícitas y tipadas, reemplazabilidad y un orquestador que delega sin ejecutar la lógica de dominio. «Sin estado» en este contexto no significa que el grafo no conserve datos: el orquestador sigue leyendo el tema y escribiendo el plan en el ejemplo completo. La regla se formula respecto a no absorber el trabajo de los especialistas. [L:0–1; W:1,5]

La reemplazabilidad depende de mantener el contrato de entrada y salida. Si otro trabajador cumple la misma responsabilidad con la misma interfaz, la coordinación no necesita cambiar por sus detalles internos. [L:1; W:2]

## 3. Patrones y criterios de elección

Las fuentes presentan dos catálogos relacionados, pero no idénticos. I:3 enumera supervisor/enrutador, pipeline secuencial, despliegue paralelo/recolección y jerarquía. L:2 enumera encadenamiento, paralelización, enrutamiento, orquestador-trabajador y evaluador-optimizador. Conviene conservar esa diferencia y no atribuir a una lección la lista de la otra.

### 3.1 Secuencia

Cada etapa recibe el resultado anterior. Encaja cuando hay dependencias y orden claro. Los ejemplos son investigación → redacción → edición, o extracción de datos de factura → validación → registro contable. No son piezas independientes que puedan tratarse indistintamente. [I:3; L:2]

### 3.2 Paralelización y recolección

Varios trabajadores procesan piezas independientes al mismo tiempo y después se combinan resultados. Las fuentes utilizan el análisis de competidores y el resumen simultáneo de artículos. La condición importante es la independencia de las subtareas, no simplemente que existan varios agentes. [I:3; L:2]

### 3.3 Enrutamiento

El modelo clasifica una entrada y el grafo elige exactamente una rama. Un ticket de facturación se dirige al especialista correspondiente; no se divide el ticket entre todos los especialistas. La pregunta es quién debe manejar esa solicitud completa. [L:2; R:1–2]

### 3.4 Orquestador-trabajador

El orquestador descompone una tarea en varias piezas, delega cada una y recoge resultados para sintetizarlos. L:2 describe esta forma de manera general; W desarrolla el caso de subtareas independientes, paralelas y en cantidad variable conocida durante la ejecución. El informe con secciones variables es el ejemplo completo. [L:2; W:0–1,5]

### 3.5 Evaluador-optimizador

Un generador produce un resultado y un evaluador lo juzga; el proceso se repite hasta cumplir los estándares de calidad. El ejemplo es redactar y revisar un documento. La captura lo presenta como patrón conceptual, sin desarrollar aquí un grafo completo ni criterios de parada concretos. [L:2]

### 3.6 Jerarquía

Un coordinador organiza subagentes que, a su vez, pueden coordinar equipos. El ejemplo de lanzamiento de producto separa marketing, ingeniería y logística. La fuente lo propone para problemas que necesitan descomposición recursiva. No proporciona código de esa jerarquía. [I:3]

### 3.7 Seleccionar no es descomponer

«Orquestación» tiene un sentido amplio en I:1: coordinar agentes, orden e información. En la comparación específica de R:2 y W:1, se usa para contraponer descomposición de trabajo con selección de una sola rama. Así, un router es parte del catálogo general de coordinación, pero no equivale al patrón orquestador-trabajador.

| Pregunta sobre la tarea | Enfoque de las fuentes |
| --- | --- |
| ¿Un agente puede resolverla claramente y de forma verificable? | Mantener un agente |
| ¿Las etapas dependen de la salida anterior? | Secuencia |
| ¿Hay piezas independientes que reunir? | Paralelización |
| ¿Hay que elegir un solo especialista? | Router |
| ¿El número de piezas se descubre en ejecución? | Orquestador-trabajador con Send |

Base de la selección: I:4, L:2 y W:1,4. Los patrones pueden combinarse; I:3 contempla un supervisor que delega en un especialista que luego usa una secuencia o un despliegue paralelo.

## 4. Comunicación: dónde falla un sistema de agentes competentes

La comunicación puede romper el conjunto aunque cada agente funcione correctamente por separado. C:0 muestra tres problemas: un editor recibe una instrucción vaga sobre autenticación y pruebas; un especialista de facturación recibe «el cliente está molesto» sin identificadores ni categoría; un investigador recibe toda la conversación y procesa información irrelevante.

Son fallos diferentes pero relacionados: intención ambigua, datos ausentes y contexto excesivo. El diseño de comunicación debe declarar qué se delega, qué información se comparte y qué porción necesita cada receptor. [C:0–1,5–6]

### 4.1 Paso de mensajes

Un mensaje de tarea es un paquete discreto y autónomo con el encargo y los insumos necesarios. C:1 presenta:

```json
{
  "category": "refund",
  "order_id": 1044,
  "amount": 39.90
}
```

La transferencia es explícita y rastreable. Su rigidez aparece cuando el receptor necesita datos que no estaban previstos: hay que cambiar el formato. También se vuelve repetitivo reenviar información solapada a muchos agentes. [C:1]

### 4.2 Pizarra compartida

La pizarra es un objeto de estado común donde los agentes publican y leen hechos de coordinación. En LangGraph corresponde al estado del grafo, frecuentemente declarado mediante `TypedDict`. El investigador escribe fuentes; el escritor las lee y produce un borrador; el revisor añade notas. [C:1–2]

Su flexibilidad permite que nuevos agentes lean datos existentes sin exigir que el productor reenvíe cada paquete. A cambio, requiere controlar las claves de escritura y respetar el momento del flujo: un escritor no debería usar fuentes todavía ausentes o desactualizadas. [C:1–2]

La recomendación de la fuente combina los modelos: pizarra para hechos compartidos, mensajes para delegaciones. No plantea que haya que elegir uno y prohibir el otro. [C:1–2,7]

## 5. Contratos de estado y propiedad de escritura

C:2 define un estado de investigación y propietarios de sus claves. Este bloque reproduce el código con formato normalizado y sin los comentarios editoriales:

```python
from typing_extensions import TypedDict

class ResearchState(TypedDict):
    sources: list[str]
    draft: str
    review_notes: str

write_owners = {
    "sources": "researcher_agent",
    "draft": "writer_agent",
    "review_notes": "reviewer_agent",
}

def write_to_blackboard(state: ResearchState, key: str, value, agent_id: str):
    if write_owners.get(key) != agent_id:
        raise PermissionError(f"El agente {agent_id} no puede escribir en {key}")
    state[key] = value
```

La función recibe estado, clave, valor y agente. Consulta el propietario en `write_owners`; si no coincide, lanza `PermissionError`. Si coincide, modifica la clave. No devuelve explícitamente otro estado ni valida el tipo de `value` en este fragmento. La comprobación mostrada es de propiedad de escritura. [C:2]

La fuente advierte que dos agentes escribiendo simultáneamente `draft` sin coordinación pueden sobrescribirse y perder información. La existencia de un estado tipado no sustituye las reglas de quién escribe ni el conocimiento de cuándo están listas las entradas. [C:2]

Más adelante, el ejemplo de trabajadores utiliza otra regla explícita para una clave compartida: agregar listas mediante un reductor. No es escritura concurrente sin control, sino una forma declarada de combinar contribuciones. [W:4–5]

## 6. Transferencias estructuradas y evolución del esquema

El lenguaje libre obliga al receptor a interpretar intención y reconstruir datos. La frase «El cliente está bastante molesto por un cargo en su pedido reciente, ¿puedes solucionarlo?» no identifica pedido, cargo, acción ni monto. En varios saltos, las interpretaciones pueden acumular errores. [C:3]

El equivalente estructurado de la fuente hace explícitos esos datos:

```json
{
  "task": "issue_refund",
  "order_id": 1044,
  "charge_id": "ch_88f2a",
  "amount": 39.90,
  "reason": "duplicate_charge"
}
```

Esto es un ejemplo de comunicación entre agentes, no una implementación de herramienta de reembolsos. La captura no muestra que enviar este objeto ejecute una acción. [C:3]

### 6.1 Entrada y salida declaradas

C:4 propone un contrato con `task`, `inputs` y `expected_output_schema`, acompañado de `schema_version`:

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

El receptor sabe qué resumir y el consumidor sabe que debe recibir resumen, puntuación y temas. Si el trabajador omite `key_topics` o cambia su tipo, el siguiente agente ya no puede interpretar la salida según el contrato previsto. El ejemplo describe los tipos mediante cadenas; no incluye un motor que los valide automáticamente. [C:4]

### 6.2 Versionado

Los agentes pueden evolucionar por separado. Renombrar un campo rompe consumidores que todavía esperan el anterior. C:4 muestra esta comprobación, que presupone una variable `expected_version` definida por el consumidor:

```python
if handoff["schema_version"] != expected_version:
    raise ValueError("Desajuste de versión de esquema")
```

El resultado es una detección explícita de incompatibilidad, no una migración automática. La fuente no aporta un sistema completo de negociación de versiones. El principio respaldado es declarar la versión y comprobarla antes de interpretar una respuesta con expectativas antiguas. [C:4]

## 7. Contexto acotado: diseñar desde la decisión

Pasar el estado entero a cada agente puede parecer una forma de no olvidar nada, pero las fuentes lo presentan como sobrecarga: añade tokens irrelevantes, latencia, coste y ruido al razonamiento. El objetivo es dar exactamente lo que el rol necesita, no dejarlo sin información ni enviársela toda. [C:5–6; W:2]

El método de C:6 parte de la decisión y retrocede hacia los datos:

1. Nombrar la decisión: para el verificador de citas, si cada afirmación del borrador tiene una fuente.
2. Derivar las claves mínimas: `draft` y `sources`.
3. Declararlas en una proyección que será la entrada de ese agente.

El ejemplo completo de esa proyección en C:6 es:

```python
from typing_extensions import TypedDict
from langgraph.graph import MessagesState

class ResearchState(MessagesState):
    sources: list[str]
    draft: str
    review_notes: str
    outline: str

def scope_for_citation_checker(state: ResearchState) -> dict:
    return {
        "draft": state["draft"],
        "sources": state["sources"]
    }
```

La función recibe el estado compartido y devuelve solo dos claves. Los mensajes, las notas de revisión y el esquema general permanecen en el estado, pero no forman parte de esta entrada. Este bloque es otro ejemplo independiente del `ResearchState` de la sección 5: allí la base es `TypedDict`; aquí la fuente usa `MessagesState`. [C:2,6]

### 7.1 Herramientas que leen solo su dependencia

El mismo criterio se aplica a herramientas. C:5–6 proporciona:

```python
from langchain.tools import tool, ToolRuntime

@tool
def list_open_tickets(runtime: ToolRuntime) -> str:
    """Devuelve solo los tickets asignados a este agente."""
    return f"Tickets abiertos: {runtime.state['assigned_tickets']}"
```

La herramienta recibe `ToolRuntime`, accede a `assigned_tickets` y devuelve una cadena. No consulta todo el historial ni contiene en este ejemplo una búsqueda en una base de datos. La clave debe formar parte del estado que recibe el runtime; la captura no incluye un grafo completo de esta herramienta. [C:5–6]

## 8. ToolNode: herramientas y estado común

Antes de ToolNode, el despacho manual exige inspeccionar las llamadas solicitadas por el modelo, localizar la herramienta, ejecutarla, manejar errores y añadir resultados a la conversación. L:3 presenta `ToolNode` como una pieza reutilizable que reúne ese trabajo.

El recorrido descrito es modelo → estado compartido → ToolNode → estado compartido → modelo. ToolNode recibe una lista de herramientas, lee el último mensaje del modelo, ejecuta sus llamadas y escribe resultados estructurados. Los nodos coordinan mediante el estado del grafo, no llamándose directamente entre ellos. [L:3]

### 8.1 Práctica capturada: clima

El ejercicio L:4 solicita construir un `StateGraph` sobre `MessagesState`, registrar `model` con `call_model`, registrar `tools` con un `ToolNode` para `get_weather`, conectar `START` al modelo, usar `tools_condition` como condición de salida y devolver el flujo desde las herramientas al modelo. Después pide compilar e invocar con una pregunta sobre clima.

La herramienta capturada recibe `city: str` y devuelve `f"It is 22°C and sunny in {city}."`. Es un resultado fijo de demostración. La pregunta documentada «¿Clima en París?» debería llevar a la llamada y a una respuesta final que incluya ese clima; no demuestra una consulta meteorológica externa. [L:4]

El arranque utiliza `ChatAnthropic(model="claude-sonnet-5")` y `bind_tools([get_weather])`, pero su función `call_model` solo devuelve `{"messages": state["messages"]}` como placeholder. No hay una solución completa capturada del bucle. Tampoco se recuperaron como lecciones distintas las tarjetas posteriores sobre herramientas y estado: repiten este ejercicio. [L:4–8]

## 9. Router: separar clasificación, ruta y trabajo

El patrón router asigna tres responsabilidades diferentes. El LLM determina una categoría. La función de ruta obtiene esa etiqueta del estado. El grafo sigue la arista correspondiente y el manejador especializado realiza el trabajo. La solicitud completa sigue exactamente una rama. [R:0–4]

Entre los ejemplos conceptuales están un asistente de correo que distingue reunión, factura y boletín, y un asistente de código que clasifica sintaxis, diseño y uso de biblioteca. La práctica concreta utiliza soporte con `billing`, `technical` y `general`. [R:1,5]

### 9.1 Salida estructurada del clasificador

El esquema `Route` de la práctica es un `TypedDict` con `category: Literal["billing", "technical", "general"]`. `with_structured_output(Route)` prepara el clasificador para devolver una etiqueta de ese conjunto en lugar de una explicación libre. `State` contiene `message`, `category` y `response`. [R:3,5]

El material pide pasar al clasificador solo el mensaje relevante, no toda la pizarra. La etiqueta es un contrato de interfaz para el flujo posterior. El clasificador no debe resolver un cargo ni reparar un problema técnico: solo clasifica y delega. [R:2–3]

### 9.2 Aristas condicionales

Fragmento de R:4, normalizado y sin comentarios:

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

`route` no llama a un modelo: devuelve el dato que el clasificador ya escribió. `add_conditional_edges` recibe el nombre del origen, la función de ruta y el mapa de etiquetas a destinos; el grafo usa ese resultado para elegir la arista. El fragmento presupone `builder` y los manejadores previamente registrados. [R:4]

La práctica R:5 añade la conexión de cada manejador a `END` y solicita que `classify` invoque `router_llm` sobre `state["message"]` para guardar `category`. Los resultados esperados son facturación hacia `billing`, técnico hacia `technical` y el resto hacia `general`. No se recuperó el cuerpo completo de los manejadores ni un programa final resuelto. [R:5]

### 9.3 Extensibilidad y límites

Cada manejador conserva una responsabilidad limitada y puede reemplazarse independientemente. R:4 ilustra añadir una categoría como `refund` incorporando su nodo y actualizando el mapa. El principio es mantener la decisión de ruta separada de la lógica de dominio. [R:1,4]

Un router no es el mecanismo para distribuir un informe entre varios redactores. Forzar esa descomposición en una rama única crea un cuello de botella y contradice la forma del problema. Para ese caso, W desarrolla otro patrón. [R:2; W:1]

## 10. Orquestador-trabajador: piezas variables e independientes

El patrón es útil cuando no se conoce de antemano el número de piezas. La fuente muestra informes con distinto número de secciones y revisiones con distinto número de archivos. También menciona contratos divididos en cláusulas y traducciones por párrafos como situaciones de aplicación. [W:0,4]

El reparto consta de tres roles:

- **Orquestador:** lee el trabajo, produce una lista de subtareas y delega; no realiza el trabajo de cada una.
- **Trabajador:** procesa una subtarea independiente con el contexto necesario y una interfaz clara.
- **Sintetizador:** recibe resultados estructurados y forma una salida coherente.

Fuente: W:1–3. Si las etapas dependen estrictamente unas de otras o la tarea ya es una unidad coherente, W:1 indica que un agente o una secuencia pueden ser más simples.

### 10.1 Trabajadores delimitados

Cada trabajador tiene un propósito. En revisión, recibe un archivo, no toda la solicitud ni el historial de conversación. La fuente distingue trabajador ciego, al que le faltan datos, de trabajador sobrecargado, que recibe información innecesaria. Ambos contradicen la idea de contexto justo. [W:2]

### 10.2 Send y expansión dinámica

En una ruta convencional puede devolverse un nombre de nodo. Para repartir subtareas, la función condicional devuelve una lista de objetos `Send`. Cada objeto indica qué nodo ejecutar y qué datos recibe esa ejecución. [W:4]

La asignación por secciones de la fuente es:

```python
from langgraph.types import Send

def assign_workers(state):
    return [Send("worker", {"section": section}) for section in state["sections"]]
```

Solo se desarrolla el nombre local `s` de la fuente como `section`. La cantidad de envíos coincide con las secciones del plan; todos usan el nodo trabajador registrado, cada uno con su porción de contexto. El grafo no necesita declarar de antemano un nodo con nombre distinto por cada sección posible. [W:4–5]

### 10.3 Reductor: agregar en vez de sobrescribir

W:4 declara `drafts: Annotated[list, operator.add]`. Los trabajadores devuelven listas de un elemento bajo `drafts`, y el reductor agrega esas contribuciones en una lista común. Así se evita que un borrador reemplace a otro por una escritura no coordinada.

Esta regla explícita de acumulación explica por qué varias ejecuciones pueden contribuir al mismo campo sin reproducir el problema de sobrescritura de la pizarra. La fuente demuestra agregación de listas; no desarrolla una política de orden editorial de secciones ni otro mecanismo de sincronización adicional. [C:2; W:4–5]

### 10.4 Sintetizador: conocer la forma de lo recibido

Si cada trabajador devuelve `{"drafts": [...]}`, el sintetizador sabe dónde están los textos. En W:3 y W:5 devuelve `{"report": "\n\n".join(state["drafts"])}`. No analiza prosa para descubrir campos y no invoca a otro modelo: concatena los borradores con dos saltos de línea.

La fuente advierte contra salidas libres y esquemas que cambian sin coordinarse con el consumidor. Unificar formatos y versionarlos mantiene compatible la fusión. El código completo utiliza estructuras declaradas, pero no implementa la comprobación de `schema_version` del ejemplo de comunicación; son ejemplos relacionados, no una única implementación integrada. [C:4; W:3,5]

## 11. Grafo completo de la fuente

El ejemplo W:5 planifica y redacta un informe sobre «El Futuro de la IA». Este bloque conserva código, prompts y lógica de la captura con formato legible, comentarios omitidos y el nombre local de la comprensión desarrollado como `section`.

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

### 11.1 Lectura de datos y APIs

`Section` define `name` y `focus`; `Field(description=...)` describe lo que representa cada uno. `Plan` contiene una lista de secciones. El modelo configurado con `with_structured_output(Plan)` es el planificador utilizado por `orchestrator`. [W:5]

`ReportState` separa tema, plan, borradores e informe. `orchestrator` recibe el estado, utiliza su `topic` en el prompt de planificación y devuelve las secciones del plan. `assign_workers` las transforma en envíos con solo la clave `section`. `worker` recibe una de esas secciones, toma su nombre y enfoque para pedir la redacción y devuelve el texto como una lista de un elemento. [W:5]

`drafts` es la clave de acumulación. `synthesizer` recibe el conjunto de borradores en el estado y devuelve el informe unido. Los resultados parciales no se guardan como prosa en una conversación para que otro agente adivine su significado: tienen una clave conocida y una forma de combinación. [W:4–5]

`StateGraph(ReportState)` prepara el grafo con ese esquema. `add_node` registra nombres y funciones. `add_edge` fija conexiones; `START` y `END` marcan entrada y terminación. `add_conditional_edges` conecta el orquestador con la función que genera los envíos hacia `worker`. `compile()` produce el grafo que se invoca con el estado inicial; `result["report"]` es el campo que el ejemplo imprime. [W:5]

### 11.2 Prompts exactos

El planificador recibe esta plantilla:

```text
Planifica las secciones para un informe sobre: 
{state['topic']}
```

El trabajador recibe esta otra:

```text
Escribe la sección '{section.name}': 
{section.focus}
```

Las expresiones entre llaves son las sustituciones de las f-strings del ejemplo, no instrucciones adicionales para NotebookLM ni prompts de OpenClaw. [W:5]

### 11.3 Qué demuestra y qué no demuestra

El recorrido muestra plan tipado, reparto dinámico con contexto acotado, acumulación de listas y síntesis. El resultado esperado es un informe compuesto por los borradores. No hay una salida textual fija ni un número de secciones garantizado para ese tema en la captura. [W:4–5]

El ejemplo conserva `claude-sonnet-5` porque es el identificador extraído, no porque aquí se haya comprobado que está disponible. Tampoco contiene instalación, credenciales, comandos shell, límites de concurrencia configurables, reintentos, evaluación de calidad ni mecanismos de ordenación añadidos. No se atribuyen esas funciones al código. La evidencia es el ejemplo fuente, no una ejecución verificada. [W:5]

## 12. Las tres prácticas: tareas y evidencia disponible

### 12.1 Bucle de herramientas

La práctica L:4 pide registrar modelo y herramientas, conectar la condición de herramientas y el retorno al modelo, compilar e invocar con la pregunta de París. Se espera que el modelo utilice `get_weather` y produzca después una respuesta con el clima. Su arranque conserva un `call_model` placeholder y no un programa terminado.

### 12.2 Enrutador de soporte

La práctica R:5 pide invocar el clasificador sobre `message`, guardar `category`, devolverla en `route`, mapear las tres categorías y conectar cada manejador a `END`. Se espera una sola rama correspondiente al mensaje. El esquema y el inicio del código están visibles; no lo están todos los cuerpos de manejadores ni una solución final completa.

### 12.3 Revisión de archivos

La práctica W:6 pide terminar un grafo de revisión. Su estado declara `files`, `notes: Annotated[list, operator.add]` y `report`. El orquestador del arranque devuelve `{"notes": []}` porque los archivos ya están en el estado. El trabajador visible devuelve `{"notes": [f"reviewed {state['file']}"]}`: esta nota simula la contribución por archivo, no inspecciona su contenido.

Los pasos del enunciado son generar un `Send` por archivo hacia `reviewer`, conectar la expansión desde `orchestrator`, añadir las conexiones de entrada y síntesis, compilar en `graph` e invocar con la lista del ejercicio. Se espera una nota por archivo, acumulada por el reductor, antes del informe combinado. La captura termina antes de mostrar la lista completa de ejemplo y el cuerpo del sintetizador. No se completan aquí esos datos ausentes. [W:6]

## 13. Fallos y decisiones de diseño relacionadas

| Fallo presentado | Por qué importa | Respuesta descrita en las fuentes |
| --- | --- | --- |
| Agente generalista sobrecargado | Mezcla instrucciones y responsabilidades | Separar roles cuando exista un límite observable [I:0,4] |
| Sobreorquestación | Añade coste sin aclarar el trabajo | Mantener simple lo que puede resolver un agente [I:4] |
| Mensaje vago | Obliga a adivinar datos y acción | Campos nombrados y contrato de tarea [C:3–4] |
| Escrituras sin coordinación | Pueden sobrescribir aportes | Propiedad de claves o acumulación declarada en el ejemplo paralelo [C:2; W:4] |
| Cambio de salida sin versión | Rompe a consumidores posteriores | Declarar y comprobar `schema_version` [C:4] |
| Contexto completo en cada llamada | Añade ruido, latencia y coste | Proyectar los datos mínimos según la decisión [C:5–6] |
| Trabajador ciego | No tiene datos suficientes para su responsabilidad | Entrada acotada pero suficiente [W:2] |
| Orquestador que hace el trabajo | Absorbe responsabilidades y se vuelve cuello de botella | Separar plan, ejecución y síntesis [W:1–3] |
| Router usado para repartir piezas | Una rama concentra un problema multipartes | Descomposición con trabajadores [R:2; W:1] |
| Salida libre del trabajador | El sintetizador debe adivinar cómo combinar | Salidas estructuradas con interfaz conocida [W:3] |

Estas respuestas son los mecanismos que el material describe. La tabla no supone que todos estén integrados o validados en el grafo completo de W:5.

## 14. Glosario relacionado

- **Agente especializado:** rol delimitado dentro del objetivo común. Su distinción importa por lo que decide y entrega. [I:2]
- **Orquestación:** coordinación de responsables, orden e información; en el patrón específico, planificación y delegación de subtareas. [I:1; W:1]
- **Workflow:** proceso que conecta modelos y herramientas para resolver una tarea. [L:1]
- **Pizarra:** estado común con datos de coordinación, claves conocidas y escrituras controladas. [C:1–2]
- **Transferencia estructurada:** encargo con tarea, entradas, salida esperada y versión del contrato. [C:4]
- **Contexto acotado:** proyección de las claves necesarias para una decisión concreta. [C:5–6]
- **ToolNode:** nodo que ejecuta las llamadas a herramientas del modelo y devuelve resultados al estado compartido. [L:3]
- **Clasificador:** nodo que produce una categoría del conjunto tipado permitido. [R:3]
- **Función de ruta:** obtiene la categoría del estado y la entrega a la selección de arista. [R:4]
- **Send:** describe una ejecución de un nodo trabajador y la porción de datos que recibe. [W:4]
- **Reductor:** regla de combinación de actualizaciones; en el ejemplo, `operator.add` agrega listas de borradores. [W:4–5]
- **Sintetizador:** combina los resultados parciales según su interfaz; en el ejemplo completo, une cadenas. [W:3,5]

## 15. Preguntas de recuperación con respuestas

Las preguntas siguientes reorganizan conceptos y evaluaciones presentes en I:5 y C:7 y explicaciones de L, R y W. No prescriben un proyecto nuevo.

**¿Qué define la orquestación?** Decidir quién hace qué, en qué orden y con qué información para un objetivo común. [I:1,5]

**¿Cuándo no conviene añadir agentes?** Cuando uno resuelve una tarea coherente de forma clara y verificable, o cuando la división solo añade pasos de comunicación. [I:4–5; L:1]

**¿Cómo se distingue un pipeline de la paralelización?** En el primero hay dependencia de la salida anterior; en la segunda hay subtareas independientes y recolección. [I:3; L:2]

**¿El router reparte trabajo entre todos sus manejadores?** No: clasifica y selecciona exactamente una rama. [R:1–2]

**¿En qué se diferencia del orquestador-trabajador?** Este último divide un trabajo en varias subtareas, delega y sintetiza; en W su cantidad se decide durante la ejecución. [W:1,4]

**¿Por qué combinar pizarra y mensajes?** La pizarra contiene hechos compartidos y los mensajes expresan encargos explícitos; cumplen funciones distintas. [C:1–2,7]

**¿Por qué no usar prosa libre como protocolo?** Cada salto reinterpreta la intención y puede amplificar ambigüedades. Los campos estructurados reducen esas conjeturas. [C:3,7]

**¿Qué falta si una delegación declara tarea y entradas pero no salida?** El consumidor no tiene un contrato explícito sobre la forma del resultado y puede interpretarlo incorrectamente. [C:4,7]

**¿Qué aporta la versión?** Permite detectar que el formato cambió antes de usar una salida con expectativas incompatibles. [C:4]

**¿Qué necesita el verificador de citas?** Borrador y fuentes; esa es la proyección del estado que utiliza el ejemplo. [C:5–6]

**¿Cómo se relacionan ToolNode y el estado?** El modelo escribe una petición; ToolNode la lee, ejecuta herramientas y escribe resultados para la siguiente actuación del modelo. [L:3]

**¿Cómo se crean tantos trabajadores como secciones?** `assign_workers` devuelve un `Send` por sección del plan, cada uno con su contexto. [W:4–5]

**¿Qué evita que un borrador borre otro?** La clave `drafts` usa un reductor que agrega las listas devueltas. [W:4–5]

**¿El sintetizador completo vuelve a llamar al LLM?** No; el código mostrado une los borradores con `"\n\n".join(...)`. [W:5]

## Síntesis final

Las cinco fuentes conectan tres decisiones: si dividir el trabajo, cómo organizar el flujo y qué información se transfiere. La especialización no elimina la necesidad de coordinación; hace más importante definir entradas, salidas y responsabilidades. La pizarra conserva datos comunes, los mensajes estructurados delegan y el contexto acotado evita tanto la ceguera como la sobrecarga. [I:1–4; C:1–6]

LangGraph aparece como la realización concreta de esas ideas: ToolNode centraliza ejecución de herramientas sobre estado, las aristas condicionales conectan una categoría con un único manejador y `Send` distribuye una cantidad variable de piezas hacia trabajadores. En el ejemplo completo, un reductor agrega borradores y un sintetizador los concatena. La elección sigue partiendo de la forma del problema, no de la cantidad de agentes disponibles. [L:3–4; R:4–5; W:4–5]