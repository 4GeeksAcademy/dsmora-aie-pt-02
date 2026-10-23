# Dossier ampliado para NotebookLM: patrón evaluador-optimizador con LangGraph

## Alcance y procedencia

Este documento organiza y amplía para consulta el contenido de `the_evaluator_optimizer_pattern.json`. La fuente técnica es exclusivamente ese JSON. La estructura, las tablas comparativas, las preguntas de repaso y las explicaciones del recorrido son organización editorial; no incorporan bibliografía, conceptos técnicos ni ejemplos externos.

| Referencia | Tarjeta del JSON | Contenido principal |
| --- | --- | --- |
| [0] | Bienvenido al patrón evaluador-optimizador | Problema, motivación, ejemplos y arco del curso |
| [1] | El patrón evaluador-optimizador | Generador, evaluador, bucle y condiciones de parada |
| [2] | Por qué un evaluador | Feedback accionable, coste y criterios de uso |
| [3] | Construyendo el bucle en LangGraph | Estado, nodos, ruta, grafo y ejemplo de código |
| [4] | Construir un bucle evaluador-optimizador | Enunciado y resultado esperado de la práctica |

### Calidad de la extracción

Se capturaron siete tarjetas. Los índices 5 y 6 repiten el contenido de la práctica del índice 4, por lo que no representan lecciones nuevas. El código de la práctica aparece concatenado y truncado en la tarjeta; sus instrucciones y resultado esperado sí son legibles. [4–6]

El tutorial presenta un generador que empieza con un borrador fijo en español; la práctica presenta otro que utiliza `topic` para formar un titular inicial en inglés. Son dos ejemplos distintos del JSON, no una sola implementación original. [3–4]

La fuente menciona ejecutar `app.py`, pero no proporciona un comando literal de terminal, instalación ni configuración del entorno. Tampoco incluye prompts de OpenClaw. No se completan esos vacíos con instrucciones externas. [3–4]

## 1. Problema que aborda el patrón

Los primeros resultados de un modelo pueden parecer plausibles y aun así quedar demasiado largos, poco claros o incumplir algún criterio. El material presenta como ejemplos una función que no pasa pruebas, una traducción poco fluida y campos incompletos extraídos de una factura. La propuesta es no aceptar automáticamente el primer resultado: se genera una candidata, se evalúa y se refina con la retroalimentación obtenida. [0]

Ejemplos mencionados en la introducción:

- Una herramienta de marketing redacta un titular, lo evalúa por longitud y claridad, y lo revisa.
- Un asistente de programación escribe una función, ejecuta pruebas y la reescribe si fallan.
- Un sistema de traducción evalúa fluidez y vuelve a intentar las oraciones débiles.
- Un parser de facturas extrae campos, comprueba si están completos y vuelve a extraer los que faltan. [0]

En todos estos ejemplos, la iteración es dirigida por algún criterio de evaluación. El patrón no equivale simplemente a pedir otro intento sin explicar qué debe cambiar. [0–2]

## 2. Componentes y ciclo de retroalimentación

El patrón tiene tres componentes: [1]

| Componente | Responsabilidad según la fuente |
| --- | --- |
| Generador | Produce una salida candidata o un borrador. |
| Evaluador | Compara la candidata con criterios explícitos y devuelve un veredicto estructurado y feedback. |
| Bucle | Devuelve la retroalimentación al generador y controla si se refina o se termina. |

El recorrido conceptual es:

1. El generador produce una candidata.
2. El evaluador determina si cumple los criterios y comunica el resultado.
3. Si la candidata se rechaza, el generador recibe el feedback y produce otra versión.
4. El proceso termina al aceptar la salida o al alcanzar el máximo de iteraciones. [1]

La evaluación es el mecanismo que convierte la repetición en un refinamiento orientado a criterios consistentes y medibles. El material presenta dos guardas de terminación: aceptación y máximo predefinido de iteraciones. [1]

Al alcanzar el máximo, el flujo termina aunque la salida no haya sido aceptada. Por tanto, la guarda garantiza que el ciclo pare; el enunciado no dice que el máximo convierta una salida rechazada en aceptada. [1,3–4]

## 3. Qué significa feedback accionable

El evaluador debe indicar qué no cumplió la candidata y por qué. La fuente contrasta una petición vaga como «Mejóralo» con mensajes estructurados: [2]

```json
{"accepted": false, "feedback": "Prueba fallida: falta la instrucción return"}
```

```json
{"accepted": false, "feedback": "Título demasiado largo: 60 caracteres, el límite es 50"}
```

En estos ejemplos, `accepted` expresa el veredicto y `feedback` comunica el motivo del rechazo. En el segundo caso, el mensaje incluye la medida observada y el límite. La salida no es una frase ambigua de reintento, sino una indicación que puede guiar el siguiente intento. [2]

La lección de LangGraph muestra también la forma de aceptación del evaluador: `accepted: True` con `feedback` vacío cuando la candidata cumple; si no, `accepted: False` con una explicación breve. [3]

## 4. Cuándo considerar el patrón

La evaluación agrega pasos, latencia y coste. La fuente sugiere considerar el patrón cuando evaluar sea barato en comparación con generar y cuando la calidad importe y deba verificarse de forma confiable. [2]

La fuente indica que puede no convenir cuando: [2]

- La primera salida suele ser suficientemente buena.
- La evaluación es costosa o no está disponible.
- Bastan comprobaciones simples basadas en reglas o reintentos.

Ejemplos de tareas mencionadas para el patrón incluyen redactar el asunto de un correo y revisar longitud y claridad; generar una consulta SQL y comprobar las columnas esperadas; o producir un resumen y verificar un límite de longitud. [1]

La decisión importante no es «iterar siempre», sino definir un criterio de evaluación que justifique el coste de volver a generar. Esta formulación resume los criterios y advertencias de [1–2]; no añade una regla técnica distinta.

## 5. Estado del bucle en LangGraph

El estado guarda la información que los nodos necesitan entre pasadas. En la tarjeta de implementación se define con `TypedDict` y tiene cuatro campos: [3]

| Campo | Tipo | Uso descrito |
| --- | --- | --- |
| `draft` | `str` | Borrador candidato actual. |
| `feedback` | `str` | Retroalimentación del evaluador. |
| `iterations` | `int` | Contador de ciclos de refinamiento. |
| `accepted` | `bool` | Indica si el borrador fue aceptado. |

El fragmento de la fuente es:

```python
from typing_extensions import TypedDict

class State(TypedDict):
    draft: str
    feedback: str
    iterations: int
    accepted: bool
```

El estado es compartido entre nodos: cada uno puede leer los campos necesarios y devolver actualizaciones. En la práctica se añade `topic`, porque el generador de ese ejercicio lo utiliza para construir el titular inicial. [3–4]

## 6. Nodos y sus contratos

### 6.1 Generador del tutorial

El ejemplo de la tarjeta 3 recibe `State` y devuelve un diccionario con el borrador y el contador actualizado. Si todavía no hay borrador, empieza con una frase fija; en las pasadas posteriores elimina una palabra del final: [3]

```python
def generator(state: State) -> dict:
    if not state.get("draft"):
        draft = "Un rápido zorro marrón salta sobre el perro viejo, perezoso y dormido"
    else:
        draft = " ".join(state["draft"].split()[:-1])
    return {"draft": draft, "iterations": state.get("iterations", 0) + 1}
```

En este ejemplo concreto el generador recorta una palabra por pasada. El código no usa `state["feedback"]` para decidir cómo recortar; el texto de la tarjeta describe el refinamiento de forma general, pero esta implementación lo simula con la operación de quitar la última palabra. [3]

### 6.2 Evaluador del tutorial

El evaluador cuenta las palabras con `split()`. Si el total excede `TARGET_WORDS`, rechaza y devuelve feedback; en caso contrario, acepta con feedback vacío. Su salida actualiza `accepted` y `feedback`. [3]

```python
def evaluator(state: State) -> dict:
    if len(state["draft"].split()) > TARGET_WORDS:
        return {"accepted": False, "feedback": "Demasiado largo, elimina una palabra"}
    return {"accepted": True, "feedback": ""}
```

La comparación es estrictamente `>`: una candidata con exactamente `TARGET_WORDS` palabras no cae en la rama de rechazo. La práctica concreta fija `TARGET_WORDS = 5`. [3–4]

### 6.3 Ruta de salida

La función `route(state)` devuelve `END` si el evaluador marcó aceptación o si el contador alcanzó el límite. Si ninguna condición se cumple, devuelve el nombre del generador para continuar el ciclo. [3–4]

```python
def route(state: State) -> str:
    if state["accepted"] or state["iterations"] >= MAX_ITERATIONS:
        return END
    return "generator"
```

El ejercicio solicita exactamente estas condiciones y fija `MAX_ITERATIONS = 10`. [4]

## 7. Conexión del flujo

El grafo encadena generador y evaluador, y usa una arista condicional para repetir o terminar: [3]

```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("generator", generator)
builder.add_node("evaluator", evaluator)
builder.add_edge(START, "generator")
builder.add_edge("generator", "evaluator")
builder.add_conditional_edges(
    "evaluator", route, {"generator": "generator", END: END}
)
graph = builder.compile()
```

Lectura de la estructura:

- `StateGraph(State)` crea un constructor de grafo asociado al esquema `State`.
- `add_node` registra los nodos `generator` y `evaluator` con sus funciones.
- `add_edge` conecta el inicio con el generador y el generador con el evaluador.
- `add_conditional_edges` ejecuta `route` desde el evaluador y asigna cada resultado a un destino: `"generator"` vuelve a generar y `END` finaliza.
- `compile()` construye el grafo compilado. [3]

El flujo completo puede representarse así:

```text
START -> generator -> evaluator -> route
                                |-> "generator": repetir
                                |-> END: terminar
```

La práctica expresa el mismo mapa de destinos, con una condición explícita de terminación por aceptación o por máximo de iteraciones. [4]

## 8. Práctica: completar un bucle de titulares

La tarjeta 4 plantea conectar en `app.py` un bucle que refina un titular provisional hasta que tenga como máximo el número objetivo de palabras o alcance un límite de seguridad. [4]

### Tareas del ejercicio

1. Completar `evaluator` para contar las palabras de `state["draft"]`. Si el total es menor o igual a `TARGET_WORDS`, devolver `accepted: True` y feedback vacío. Si lo supera, devolver `accepted: False` y un feedback breve y accionable.
2. Escribir `route(state)`. Devolver `END` si el borrador fue aceptado o si `iterations` alcanzó `MAX_ITERATIONS`; devolver `"generator"` en otro caso.
3. Conectar la salida del evaluador con `add_conditional_edges`, usando el mapa `"generator"` a generador y `END` a `END`. [4]

El ejercicio fija `TARGET_WORDS = 5` y `MAX_ITERATIONS = 10`. Su generador usa `topic` para crear el primer titular y luego elimina una palabra del borrador en cada pasada. El resultado esperado es que `app.py` refine una palabra por vez, se detenga al aceptar o al alcanzar el máximo y muestre el borrador final junto al número de iteraciones. [4]

### Separación entre consigna y solución reconstruida

La consigna de la fuente define las condiciones y el cableado, pero el editor del ejercicio está concatenado y no conserva una solución completa legible. El código de la sección 6 reproduce el evaluador y la ruta que especifica el texto de la consigna, junto con ejemplos equivalentes de la tarjeta 3; no debe confundirse con una captura literal de la solución terminada. [3–4]

La fuente no muestra la invocación exacta del grafo ni un comando de terminal. Por eso el dossier no inventa una entrada concreta para `graph.invoke(...)`, un comando como `python app.py`, ni dependencias o pasos de instalación. El criterio de salida documentado es el texto que `app.py` debería imprimir, no una ejecución verificada en este entorno. [4]

## 9. Qué se puede concluir del ejercicio

- Con cinco palabras exactas, el evaluador acepta, porque rechaza solo cuando el conteo supera `TARGET_WORDS`. [3–4]
- Con más de cinco palabras, el evaluador rechaza y devuelve feedback sobre la longitud. [3–4]
- Si el evaluador rechaza y `iterations` sigue por debajo de diez, la ruta devuelve `"generator"`. [3–4]
- Si `accepted` es verdadero, la ruta devuelve `END`. [3]
- Si `iterations` llega a diez, la ruta devuelve `END` incluso si `accepted` es falso. [3–4]
- El generador del ejercicio elimina una palabra por pasada después de producir el borrador inicial. [4]

La última condición impone un límite al proceso; no garantiza por sí misma que la salida final cumpla el criterio. La fuente describe impresión del borrador final y el número de iteraciones, pero no afirma que la salida siempre se acepte antes del máximo. [1,3–4]

## 10. Vocabulario de consulta

| Término | Significado en este material |
| --- | --- |
| Candidata / borrador | Salida actual producida por el generador. |
| Criterio explícito | Condición usada para juzgar la candidata; en la práctica, el máximo de palabras. |
| Veredicto | Resultado de aceptación o rechazo del evaluador. |
| Feedback | Explicación del rechazo que orienta el siguiente intento. |
| Iteración | Pasada en la que el generador produce o refina el borrador y actualiza su contador. |
| Guardia de máximo | Condición que termina el bucle al alcanzar `MAX_ITERATIONS`. |
| Arista condicional | Conexión cuyo destino se elige usando el resultado de `route`. |

Estos términos condensan las definiciones de las tarjetas 1–4; no describen capacidades adicionales del framework. [1–4]

## 11. Límites técnicos y de evidencia

- Los ejemplos de titulares, pruebas, traducción, facturas, correo, SQL y resúmenes ilustran el patrón; no son integraciones completas. [0–2]
- El evaluador de código de la tarjeta 3 compara el conteo de palabras con `TARGET_WORDS`; no evalúa otros atributos del texto. [3]
- El generador de ejemplo recorta una palabra; no demuestra una mejora semántica ni una utilización efectiva del campo `feedback`. [3]
- La tarjeta 4 describe una práctica de completar el evaluador, la ruta y el borde condicional; el código capturado está incompleto. [4]
- La fuente no da instalación, configuración de entorno, comando de terminal exacto, entrada literal de ejecución ni salida concreta para la práctica. [3–4]
- No hay prompts de OpenClaw en el JSON. Los ejemplos de feedback estructurado son datos ilustrativos; las plantillas de LangGraph del tutorial son prompts de código, no instrucciones de OpenClaw. [2–4]

## Mapa de referencias

- `[0]` Introducción: problema de los primeros resultados, motivos para iterar, ejemplos y recorrido del curso.
- `[1]` Patrón: roles, ciclo de retroalimentación, aceptación, máximo y ejemplos de tareas.
- `[2]` Evaluador: razón de separarlo, feedback vago frente a estructurado, coste y condiciones de uso.
- `[3]` LangGraph: esquema `State`, generador, evaluador, ruta, aristas y compilación.
- `[4]` Práctica: valores de las constantes, titular con `topic`, objetivos de implementación y resultado esperado.
- `[5–6]` Repeticiones de la práctica; no contienen lecciones técnicas distintas de `[4]`.