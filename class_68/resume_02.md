# Dossier para NotebookLM: control multiagente, checkpoints e interrupciones

## Alcance y procedencia

Este dossier organiza el contenido capturado de `controlling_multi_agent_systems.json` y `checkpointing_and_interruptions.json`. No añade bibliografía, dependencias, comandos de terminal ni detalles de configuración ausentes en esas fuentes. La continuidad mencionada con las clases 66 y 67 es un puente pedagógico; no se usa como fuente de teoría de esta clase.

Las referencias `[C:N]` y `[P:N]` corresponden al campo `index` de cada JSON: `C` es control multiagente y `P` es checkpointing/interrupciones.

### Calidad de la extracción

El primer tutorial produjo 11 tarjetas. C:0–3 contienen el material distinto sobre control, error en cascada, diseño del sobre de salida y la práctica del nodo guardrail. Desde C:4 hasta C:10, la extracción repite el ejercicio de C:3, pese a que los títulos anuncian límites de bucle, arbitraje, trazabilidad, coste/latencia y evaluación. Esos títulos no bastan para reconstruir el contenido que falta, así que no se afirma que la clase enseñe esos temas.

El segundo tutorial produjo 9 tarjetas. P:7 y P:8 repiten la práctica de aprobación humana de P:6. Las tarjetas P:0–6 sí presentan una progresión distinguible. La práctica contiene código incompleto: su enunciado y resultado esperado son fuentes válidas, pero no una solución terminada.

## 1. Orquestación y control

La introducción distingue dos capas. La orquestación permite que los agentes se pasen tareas, produzcan resultados y colaboren. El control busca que esa colaboración sea confiable: detectar errores pronto, prevenir bucles infinitos, resolver conflictos y mantener el sistema transparente y manejable. Sin control, los errores pueden propagarse en silencio, los bucles consumir recursos y la depuración resultar difícil. [C:0]

Este encuadre continúa el hilo pedagógico de las clases anteriores: después de organizar roles y transferencias (clase 66) y estudiar evaluación/optimización (clase 67), la clase 68 pregunta cómo evitar que resultados inválidos avancen y cómo conservar o pausar una ejecución. Esa continuidad es organizativa, no una ampliación de la fuente técnica del curso actual.

## 2. Error en cascada

Un error en cascada ocurre cuando la salida inválida de un agente se transmite a agentes posteriores que confían en ella. Cuanto más lejos llega el error antes de detectarse, más difícil resulta localizar el origen y corregir el resultado final. [C:1]

La fuente agrupa los fallos así:

| Tipo | Descripción de la fuente |
| --- | --- |
| Estructural | Faltan campos o un campo tiene el tipo de dato incorrecto. |
| De contenido | El valor queda fuera del rango esperado o tiene formato inválido. |
| De valor | Se trata un resultado vacío o un marcador de posición como si fuera válido. |

Ejemplo: el agente de extracción devuelve `{"amount": "twenty"}` en lugar de un número. Si el agente de facturación intenta operar con ese valor, falla aguas abajo. La fuente usa el ejemplo para ilustrar por qué confiar ciegamente en una salida upstream es un antipatrón. [C:1]

## 3. Sobre de salida y guardrail

Antes de conectar agentes, se define el sobre válido de salida. Puede expresar:

- Tipo y restricción: `amount` debe ser un número positivo.
- Valores permitidos: `currency` debe ser uno de `USD`, `EUR` o `GBP`.
- Formato: `email` debe contener `@`. [C:2]

El nodo de protección o guardrail se ubica entre agentes. Lee la salida anterior, comprueba cada campo con el sobre y devuelve una de dos alternativas: la carga validada sin cambios o un error tipado que nombra campo y razón. Ese error explícito puede dirigir el flujo a una recuperación. Una advertencia registrada sin bloqueo no cumple ese propósito. [C:2]

### 3.1 Contrato del ejercicio `guardrail_node`

La práctica solicita completar una función que lee `state["draft"]`; el borrador contiene `amount`, `currency` y `email`. Reglas exactas: `amount` debe ser positivo y no booleano; `currency` debe pertenecer al conjunto `USD`, `EUR`, `GBP`; `email` debe contener `@`. Si todo pasa, devuelve el borrador validado como una actualización de estado tipada. Si algo falla, devuelve un error tipado que identifique el campo y explique el motivo. El nodo es una comprobación de límite pura: pasa o bloquea, nunca transforma la carga. [C:3]

La fuente muestra este arranque incompleto:

```python
def guardrail_node(state):
    draft = state.get("draft", {})
    amount = draft.get("amount")
    currency = draft.get("currency")
    email = draft.get("email")
    # TODO: Validate amount, currency, and email
    # Return the draft if valid
    # Return an error dict if invalid
    pass
```

El resultado esperado documentado es que un borrador válido devuelva la misma carga útil y que un monto negativo, una moneda no admitida o un email sin `@` produzca un error tipado que indique el campo. La captura no proporciona solución completa ni una política de prioridad si fallan varios campos. [C:3]

## 4. Qué es un checkpoint

Un checkpoint es una instantánea persistente del estado del grafo en una posición determinada. Incluye mensajes, claves personalizadas y la posición actual en el flujo. Cuando se adjunta un checkpointer, LangGraph guarda automáticamente el checkpoint después de cada paso o superpaso. [P:1]

Esto permite recuperar progreso después de una falla en vez de comenzar de nuevo, mantener contexto mientras se espera una decisión humana y examinar estados intermedios al depurar. La lección de importancia del checkpointing describe incluso volver a un estado guardado y reproducir desde ese punto para encontrar dónde apareció un resultado incorrecto. [P:1–2]

### 4.1 Backends presentados

| Backend | Propiedad descrita | Escenario indicado |
| --- | --- | --- |
| `InMemorySaver` | Guarda en memoria; no requiere configuración; el estado se pierde cuando termina el proceso. | Desarrollo y pruebas. |
| `SqliteSaver` | Persiste en un archivo SQLite local y sobrevive a reinicios del proceso. | Durabilidad local en un solo nodo. |
| `PostgresSaver` | Usa PostgreSQL para un estado compartido duradero y multi-trabajador. | Escenario de producción según la lección. |

Los ejemplos de la tarjeta incluyen estos fragmentos:

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

graph = builder.compile(checkpointer=InMemorySaver())
graph = builder.compile(checkpointer=SqliteSaver("./checkpoints.sqlite"))
pg_saver = PostgresSaver(dsn="postgresql://user:pass@host:port/dbname")
graph = builder.compile(checkpointer=pg_saver)
```

Son ejemplos reproducidos de la fuente, no una receta de instalación o configuración validada en este repositorio. La extracción no da dependencias, preparación de la base de datos ni credenciales reales; el DSN es ilustrativo. [P:3]

## 5. Aislamiento con `thread_id`

Cada ejecución independiente necesita su propio `thread_id`. El identificador determina una línea de tiempo separada de checkpoints dentro del backend compartido y permite cargar el checkpoint correcto al reanudar. La fuente advierte que omitir o reutilizar identificadores en ejecuciones concurrentes puede sobrescribir checkpoints y corromper el estado. También indica que no gestionar limpieza o versionado puede permitir que crezca el almacenamiento. [P:3]

Ejemplo capturado:

```python
config = {"configurable": {"thread_id": "usuario-42-sesion-1"}}
result = graph.invoke(inputs, config)
```

El ejemplo presupone que `graph` e `inputs` existen y que el grafo se compiló con un checkpointer. No constituye un script autónomo. [P:3]

## 6. Interrupción y aprobación humana

Una interrupción es una pausa explícita en el flujo, situada antes de un nodo crítico o irreversible. `interrupt(payload)` entrega al exterior la información que la persona necesita para decidir, por ejemplo los detalles de la acción y las opciones disponibles. Al producirse la interrupción, el grafo se detiene y no continúa hasta que se reanuda. [P:4]

```python
from langgraph.types import interrupt

def approval_gate(state):
    decision = interrupt({
        "action": "eliminar 12 registros",
        "options": ["aprobar", "rechazar"]
    })
```

El checkpoint es requisito de la interrupción: conserva el estado exacto mientras la ejecución espera, incluso si la pausa dura minutos u horas. La interrupción proporciona la pausa; el checkpointer proporciona persistencia para regresar. Sin checkpointer, la fuente indica que no hay estado guardado para reanudar y la ejecución da error. [P:4]

La elección entre pausa y automatización depende del tipo de decisión:

| Mecanismo | Cuándo usarlo según la fuente |
| --- | --- |
| Guardrail | Validación sencilla, determinista y automatizable. |
| Interrupción | Juicio humano para una decisión ambigua, crítica o irreversible. |

La aprobación debe solicitarse antes de la acción irreversible. La revisión posterior no evita que la acción ya haya ocurrido. [P:0,4]

## 7. Reanudar con `Command(resume=...)`

La reanudación utiliza el mismo `thread_id` que la ejecución pausada. Se invoca el grafo con `Command(resume=value)`; la llamada reingresa al nodo interrumpido y hace que `interrupt()` devuelva ese valor. El estado guardado permite continuar sin reiniciar todo el grafo. [P:5]

```python
from langgraph.types import Command

config = {"configurable": {"thread_id": "transfer-1"}}
paused = graph.invoke(inputs, config)
result = graph.invoke(Command(resume="approve"), config)
```

El nodo interrumpido vuelve a ejecutarse desde su primera línea. Por eso, el código previo a `interrupt()` se ejecuta tanto al pausar como al reanudar; el código posterior continúa después de recibir el valor de reanudación. La recomendación de la fuente es mantener el código anterior libre de efectos secundarios y colocar las acciones irreversibles después de `interrupt()`. [P:5]

El valor reanudado puede proceder de una persona o sistema externo. Debe tratarse como dato no confiable, compararse con las opciones esperadas y rechazarse o manejarse de forma segura si no coincide. La fuente da como ejemplo comprobar que la decisión sea `approve` o `reject`. [P:5]

## 8. Práctica de aprobación

La práctica P:6 pide implementar `approval_gate` y el cableado en `app.py` para una transferencia irreversible. Debe llamar a `interrupt(payload)` antes de la acción y presentar las opciones `approve` y `reject`; colocar la acción irreversible después de la interrupción; mantener sin efectos secundarios el código previo a ella; compilar con `InMemorySaver`; pausar con un `thread_id`; y reanudar con `Command(resume=...)` llevando la decisión.

Resultado esperado: la primera invocación se pausa y expone el payload; al reanudar con `approve`, la transferencia se completa exactamente una vez; al reanudar con `reject`, se cancela. Las importaciones visibles incluyen `TypedDict`, `StateGraph`, `START`, `END`, `InMemorySaver`, `Command` e `interrupt`; la implementación de la práctica está truncada, por lo que no se presenta una solución de código reconstruida. [P:6]

## 9. Relaciones entre los mecanismos

Estos mecanismos resuelven problemas distintos y se complementan:

1. El sobre de salida y el guardrail detienen datos que incumplen reglas deterministas antes de que lleguen a otro agente. [C:2–3]
2. El checkpointer conserva estado y posición para recuperar, depurar o esperar una decisión. [P:1–3]
3. La interrupción cede el control cuando hace falta una decisión humana. [P:4]
4. `thread_id` identifica qué ejecución reanudar, y `Command(resume=...)` entrega su decisión al nodo. [P:3,5]
5. La validación de la respuesta humana evita confiar ciegamente en valores externos; los efectos irreversibles quedan después de la pausa. [P:5–6]

## 10. Límites explícitos de esta fuente

- No hay contenido fiable extraído para desarrollar las lecciones tituladas límites de bucle, arbitraje, trazabilidad, coste/latencia o evaluación en el primer tutorial; sus tarjetas repiten el ejercicio del guardrail. [C:4–10]
- No se proporciona la solución completa de `guardrail_node` ni de `approval_gate`; están disponibles el contrato y el resultado esperado. [C:3; P:6]
- No se incluyen comandos de instalación o terminal, ni prompts de OpenClaw.
- Los ejemplos de backends, DSN e invocación se reproducen tal como aparecen y no certifican que el entorno de trabajo esté configurado para ejecutarlos. [P:3–6]