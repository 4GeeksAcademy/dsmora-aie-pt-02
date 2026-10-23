# Guía docente: Clase 67 - Patrón evaluador-optimizador

Duración base: 70 minutos, adaptable a 60 o 75. Guía autosuficiente para el profesor.

## Fuentes y límites

La única fuente técnica de esta guía es `the_evaluator_optimizer_pattern.json`. La notación `[índice N]` se refiere al campo `index` de ese JSON.

La extracción capturó 7 tarjetas y 5 contenidos distintos. Los índices 5 y 6 repiten íntegramente la práctica del índice 4; no se cuentan como lecciones adicionales. Los bloques de código de la práctica aparecen concatenados en la captura, por lo que el código de abajo se reconstruye solo con las instrucciones de la práctica y los ejemplos de la lección. [índices 3–6]

La clase 66 presentó el patrón entre otros flujos de trabajo multiagente; esta sesión se concentra en explicarlo y construir su bucle en LangGraph. [Clase 66, resume_01; índice 0]

La fuente menciona ejecutar `app.py`, pero no proporciona un comando de terminal literal, instalación o configuración del entorno. Tampoco contiene prompts de OpenClaw. No se añaden comandos o prompts externos. [índices 3–4]

## Continuidad y objetivos

**Qué decir (literal):** «En la clase anterior vimos el patrón evaluador-optimizador dentro de un conjunto de formas de coordinar el trabajo. Hoy vamos a aislarlo: veremos qué aporta la evaluación y cómo se conecta el ciclo para que termine al aceptar el borrador o al alcanzar un límite».

Al finalizar, el estudiante podrá:

- Describir los roles de generador, evaluador y bucle. [índice 1]
- Distinguir retroalimentación vaga de retroalimentación estructurada y accionable. [índice 2]
- Explicar el estado compartido y las aristas condicionales del grafo. [índice 3]
- Completar el evaluador y la ruta de salida de la práctica. [índice 4]

## Preparación y contingencia

- Tener disponible esta guía y el JSON extraído; no hace falta abrir las tarjetas durante la clase.
- La práctica pide completar `app.py`, pero la captura no incluye una forma ejecutable completa ni instrucciones de instalación. No prometer una ejecución en un entorno sin verificar sus dependencias.
- Si no se puede ejecutar la práctica, recorrer el código y simular el flujo: borrador, evaluación, decisión de ruta y parada por aceptación o máximo de iteraciones.
- No hay comandos shell exactos ni prompts de OpenClaw en la fuente. El único resultado de ejecución especificado es que `app.py` imprime el borrador final y el número de iteraciones. [índices 3–4]

## Agenda base: 70 minutos

| Minutos | Bloque |
| --- | --- |
| 0–7 | El problema de los primeros borradores |
| 7–18 | Componentes y condiciones de parada |
| 18–28 | Por qué hace falta un evaluador |
| 28–48 | Recorrer el grafo de LangGraph |
| 48–64 | Completar y analizar la práctica |
| 64–70 | Chequeo y cierre |

## 0–7 min: el problema de los primeros borradores

**Qué decir (literal):** «Una salida puede parecer plausible y aun así no cumplir lo que pedimos. El patrón no confía en que un segundo intento sea mejor por casualidad: genera, comprueba contra criterios y usa esa comprobación para refinar».

La fuente plantea el ejemplo de un titular que puede ser demasiado largo o poco claro. El mismo problema aparece en una función que no pasa pruebas, una traducción poco fluida o datos de factura incompletos. El ciclo es generar, evaluar y refinar. [índice 0]

**Pregunta:** «¿Qué información necesita el segundo intento para mejorar de forma dirigida?»

**Respuesta esperada:** criterios explícitos y retroalimentación concreta sobre qué falló. [índices 0–2]

## 7–18 min: componentes y condiciones de parada

**Qué decir (literal):** «Hay tres piezas. El generador propone una candidata. El evaluador la juzga con criterios explícitos y devuelve un veredicto estructurado. El bucle lleva esa retroalimentación de vuelta al generador. No repetimos indefinidamente: aceptamos o alcanzamos el máximo de iteraciones».

Explicar el ciclo en este orden: el generador produce una candidata; el evaluador indica aceptada o rechazada y aporta retroalimentación; el generador prepara el siguiente intento. Hay dos salidas del ciclo: aceptación o límite máximo. [índice 1]

La evaluación debe ser consistente y medible para que el refinamiento no sea una sucesión de intentos a ciegas. La condición de máximo evita que el flujo continúe sin límite. [índice 1]

**Preguntas:** «¿Qué dos condiciones terminan el bucle?» y «¿Qué ocurre si la salida no se acepta a tiempo?»

**Respuestas esperadas:** aceptación o máximo de iteraciones; el flujo termina de manera ordenada al alcanzar ese máximo. [índice 1]

## 18–28 min: por qué hace falta un evaluador

**Qué decir (literal):** «Pedir “mejóralo” no identifica el problema. El evaluador convierte el fallo en una instrucción para el siguiente intento».

Comparar los ejemplos capturados:

```json
{"accepted": false, "feedback": "Prueba fallida: falta la instrucción return"}
```

```json
{"accepted": false, "feedback": "Título demasiado largo: 60 caracteres, el límite es 50"}
```

En ambos casos `accepted` expresa el veredicto y `feedback` comunica el motivo. El primer mensaje señala una prueba fallida y el segundo cuantifica el exceso frente al límite. La guía no presenta estos objetos como llamadas a una API; son ejemplos del formato de retroalimentación. [índice 2]

El patrón puede valer la pena cuando evaluar cuesta poco en comparación con generar, y cuando la calidad importa y debe comprobarse de manera confiable. Conviene evitarlo si el primer resultado suele bastar, la evaluación es cara o no está disponible, o alcanzan verificaciones simples basadas en reglas o reintentos. La fuente identifica como coste adicional la latencia y los pasos de evaluación. [índice 2]

**Pregunta:** «¿En cuál de los dos ejemplos puede el generador actuar con más precisión que con “inténtalo otra vez”?»

**Respuesta esperada:** en ambos, porque el feedback identifica el error o el criterio incumplido. [índice 2]

## 28–48 min: recorrer el grafo de LangGraph

**Qué decir (literal):** «El estado es la memoria que viaja entre nodos. El generador y el evaluador no necesitan llamarse directamente: cada nodo devuelve cambios al estado y las aristas del grafo controlan el recorrido».

El estado documentado contiene `draft` (borrador), `feedback` (retroalimentación), `iterations` (contador) y `accepted` (bandera de aceptación). `TypedDict` declara esa forma en Python. [índice 3]

La función `generator(state)` crea el primer borrador si aún no hay uno; en las pasadas siguientes, el ejemplo reduce el borrador quitando una palabra y aumenta `iterations`. Devuelve un diccionario con `draft` e `iterations`. La función `evaluator(state)` cuenta las palabras con `split()`: si el conteo supera `TARGET_WORDS`, devuelve rechazo y feedback; de lo contrario, devuelve aceptación y feedback vacío. [índice 3]

La función `route(state)` devuelve `END` si `accepted` es verdadero o si `iterations` alcanzó `MAX_ITERATIONS`; de lo contrario devuelve el nombre del nodo `generator`. `add_conditional_edges` utiliza esa decisión: `generator` vuelve al nodo generador y `END` finaliza el grafo. [índice 3]

### Código de referencia para la práctica

Este ejemplo combina el flujo descrito en la lección con los valores y el generador especificados por la práctica. `TARGET_WORDS` vale 5 y `MAX_ITERATIONS` vale 10. La función `evaluator`, la función `route` y el borde condicional completan las tareas del ejercicio. [índices 3–4]

```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

MAX_ITERATIONS = 10
TARGET_WORDS = 5


class State(TypedDict):
    topic: str
    draft: str
    feedback: str
    accepted: bool
    iterations: int


def generator(state: State) -> dict:
    if not state.get("draft"):
        draft = f"A wordy first draft headline about {state['topic']}"
    else:
        draft = " ".join(state["draft"].split()[:-1])
    return {"draft": draft, "iterations": state.get("iterations", 0) + 1}


def evaluator(state: State) -> dict:
    if len(state["draft"].split()) > TARGET_WORDS:
        return {"accepted": False, "feedback": "Demasiado largo, elimina una palabra"}
    return {"accepted": True, "feedback": ""}


def route(state: State) -> str:
    if state["accepted"] or state["iterations"] >= MAX_ITERATIONS:
        return END
    return "generator"


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

El bloque define y compila el grafo. La captura de la práctica no incluye la entrada inicial ni una invocación literal del grafo; por eso no se agrega un ejemplo de ejecución inventado. El resultado esperado que sí declara la fuente es refinar el titular una palabra por pasada hasta aceptación o máximo y mostrar el borrador final junto al número de iteraciones. [índice 4]

**Pizarra de recorrido:**

1. `START` pasa a `generator`.
2. `generator` produce o recorta el borrador e incrementa `iterations`.
3. `evaluator` cuenta las palabras y actualiza `accepted` y `feedback`.
4. `route` devuelve `generator` para repetir o `END` para parar.

**Preguntas:** «¿Qué evita que el bucle sea infinito?» y «¿Qué devuelve `route` cuando el borrador no se acepta y todavía quedan iteraciones?»

**Respuestas esperadas:** `MAX_ITERATIONS`; devuelve `"generator"` mientras siga sin aceptarse y no se haya alcanzado el máximo. [índices 3–4]

## 48–64 min: completar y analizar la práctica

**Qué decir (literal):** «Ahora vamos a traducir el enunciado en tres decisiones verificables: qué significa aceptar, cuándo repetir y qué conexión del grafo usa esa decisión».

La práctica pide completar `evaluator`, escribir `route` y conectar el nodo evaluador con `add_conditional_edges`. Para acompañar la resolución, pide a la clase identificar primero las condiciones en el enunciado:

1. Aceptar si el borrador tiene `TARGET_WORDS` palabras o menos; en caso contrario, rechazar con feedback breve y accionable.
2. Devolver `END` si el borrador fue aceptado o si `iterations` alcanzó `MAX_ITERATIONS`; en cualquier otro caso devolver `"generator"`.
3. En el mapa del borde condicional, conectar `"generator"` de vuelta al generador y `END` con `END`.

El ejercicio fija `TARGET_WORDS = 5` y `MAX_ITERATIONS = 10`. El generador de la práctica crea un titular inicial desde `topic`; en cada pasada posterior elimina una palabra y aumenta el contador. Si llega al límite sin cumplir el criterio, el flujo igualmente termina. [índice 4]

**Qué preguntar después:** «¿Por qué la ruta comprueba tanto `accepted` como `iterations`?»

**Respuesta esperada:** para terminar cuando el borrador satisface el criterio o, aunque no lo satisfaga, para impedir que el grafo itere más allá del límite. [índices 3–4]

**Qué preguntar después:** «¿Qué debería ocurrir si el borrador tiene exactamente cinco palabras?»

**Respuesta esperada:** el evaluador lo acepta, porque la condición de rechazo es tener más de `TARGET_WORDS` palabras. [índices 3–4]

El criterio de resultado de la práctica es que `app.py` refine el borrador una palabra por iteración hasta aceptarlo o alcanzar el límite, y después imprima el borrador final y el número de iteraciones. No se prescribe aquí un comando de ejecución porque la fuente no lo especifica. [índice 4]

## 64–70 min: chequeo y cierre

**Qué decir (literal):** «La mejora no viene de repetir por repetir. Viene de tener un criterio, convertir el resultado de la evaluación en feedback útil y garantizar una condición de salida».

Preguntas de comprobación:

- «¿Qué devuelve el generador?» Respuesta: una candidata y el contador actualizado. [índice 3]
- «¿Qué contiene la respuesta del evaluador?» Respuesta: `accepted` y `feedback`. [índice 3]
- «¿Qué función decide la siguiente arista?» Respuesta: `route`, usada por `add_conditional_edges`. [índice 3]
- «¿Cuáles son las dos formas de terminar?» Respuesta: aceptación o máximo de iteraciones. [índice 1]
- «¿Cuándo puede no convenir este patrón?» Respuesta: cuando el primer resultado suele ser suficiente, evaluar es costoso o no está disponible, o bastan reglas simples. [índice 2]

**Cierre sugerido (literal):** «Antes de añadir un bucle a un flujo, definan qué significa aceptar, qué feedback permite corregir y cuál es el límite que garantiza que el proceso termine».

## Variantes de duración

- **60 minutos:** acortar a 4 minutos la introducción y a 7 minutos el contraste de feedback. Dedicar 18 minutos al grafo y 14 a completar la práctica; conservar el cierre y las preguntas de comprobación.
- **70 minutos:** seguir la agenda base.
- **75 minutos:** añadir 5 minutos para que parejas revisen las tres condiciones de la práctica y expliquen una ruta de repetición y una de terminación. Usar únicamente el caso del borrador, el límite de cinco palabras y el máximo de iteraciones descritos en la fuente.

## Control final

- Objetivos, agenda y guion literal incluidos.
- Se explican el estado, los nodos, las funciones y el enrutamiento con el ejemplo extraído.
- La práctica incluye criterios de aceptación, límite de iteraciones y resultado esperado.
- Se incluyen preguntas de comprobación, cierre y variantes de 60, 70 y 75 minutos.
- No se agregan comandos shell ni prompts de OpenClaw que no estén en la fuente.