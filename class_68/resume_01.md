# Guía docente: Clase 68 - Control, checkpointing e interrupciones

Duración base: 70 minutos, adaptable a 60 o 75. Documento orientado al profesor.

## Fuentes y límites

Las fuentes técnicas son `controlling_multi_agent_systems.json` y `checkpointing_and_interruptions.json`. La notación `[C:N]` y `[P:N]` señala el campo `index` de esos JSON. La continuidad con las clases 66 y 67 sirve como hilo docente, no como fuente de contenido técnico nuevo.

La extracción de control multiagente contiene 11 tarjetas, pero desde C:4 hasta C:10 repite el cuerpo del ejercicio `guardrail_node` de C:3, aunque los títulos anuncian límites de bucle, arbitraje, trazabilidad, coste, latencia y evaluación. No se presentan esos títulos como lecciones: el JSON no conserva contenido fiable para ellos. La extracción de checkpointing contiene 9 tarjetas; P:7 y P:8 repiten la práctica P:6. Por tanto, el contenido distinto de esta clase es más breve que el número de tarjetas sugiere.

La fuente incluye fragmentos Python y ejercicios, pero no un comando de terminal para ejecutarlos ni prompts de OpenClaw. No se inventan instalaciones, comandos, credenciales o soluciones completas. Cuando el ejemplo es un fragmento, se indica qué partes presupone.

## Continuidad y objetivos

En la clase 66 se trabajó la división de responsabilidades y la comunicación entre agentes; en la 67 se aisló el ciclo evaluador-optimizador. Esta clase completa el hilo desde el lado del control: validar lo que un agente entrega, guardar el estado del flujo y detenerse antes de una acción crítica cuando hace falta aprobación.

**Qué decir (literal):** «En las clases anteriores organizamos el trabajo entre agentes y vimos cómo revisar una salida. Hoy añadimos dos controles alrededor de ese trabajo: una frontera que no deja pasar datos inválidos y una ejecución que puede guardarse, pausarse y reanudarse. La pregunta no es solo si el agente produce una respuesta, sino qué impide que un error se propague y cómo recuperamos el flujo sin repetir una acción crítica».

Al terminar, el estudiante podrá:

- Explicar cómo una salida inválida puede propagar errores a los agentes posteriores. [C:1–2]
- Describir qué valida un nodo de protección y qué devuelve ante éxito o error. [C:2–3]
- Explicar qué conserva un checkpoint, para qué sirve `thread_id` y qué diferencias describe la fuente entre backends. [P:1–3]
- Distinguir una validación automática de una decisión que requiere aprobación humana. [P:0,4]
- Recorrer el ciclo de interrupción, aprobación/rechazo y reanudación, incluyendo el riesgo de ejecutar dos veces el código anterior a `interrupt()`. [P:4–6]

## Preparación y contingencia

- Tener a mano los dos JSON y esta guía; no es necesario abrirlos durante la sesión.
- No prometer ejecución del código: las capturas no documentan instalación ni configuración del entorno.
- Si no se puede ejecutar la práctica, recorrer los estados y decisiones esperados en la pizarra: carga, validación, checkpoint, interrupción, decisión y reanudación.
- La tarjeta P:6 es un ejercicio con código incompleto. Usar el enunciado y el resultado esperado, no presentar una solución reconstruida como si viniera de la fuente.
- La práctica de guardrail aparece repetida en C:4–10. No convertir sus títulos en temas impartidos.

## Agenda base: 70 minutos

| Minutos | Bloque |
| --- | --- |
| 0–7 | Del flujo multiagente al control |
| 7–20 | Errores en cascada y validación de límites |
| 20–30 | Nodo de protección: contrato y práctica |
| 30–41 | Checkpointing y aislamiento por hilo |
| 41–51 | Interrupciones y cuándo pedir aprobación |
| 51–64 | Reanudación segura y práctica HITL |
| 64–70 | Comprobación y cierre |

## 0–7 min: del flujo multiagente al control

**Qué decir (literal):** «Orquestar es coordinar tareas y resultados. Controlar es evitar que el flujo se vuelva poco confiable: detectar fallos antes de que se propaguen, guardar el progreso y saber dónde pausar».

La introducción distingue orquestación —los agentes se reparten tareas y colaboran— de control —hacer que esa colaboración sea confiable, recuperable y transparente—. Identifica como problemas los errores en cascada, los bucles sin fin, los conflictos y la dificultad para depurar. [C:0]

Hilar con lo anterior: la clase 66 definió roles y transferencias; la 67 mostró evaluación y feedback. Ahora la salida evaluada también necesita un límite que la compruebe antes de entregarla a otro agente. El control de calidad no sustituye la orquestación; se coloca alrededor de ella.

**Pregunta:** «Si cada agente parece funcionar por separado, ¿cómo puede fallar el resultado del sistema?»

**Respuesta esperada:** un agente puede producir una salida malformada o inválida y los siguientes pueden confiar en ella, propagando el error. [C:1]

## 7–20 min: error en cascada y validación de límites

**Qué decir (literal):** «Una salida upstream no es válida solo porque el agente la haya producido. Antes de pasarla al siguiente nodo, comprobamos su estructura, sus valores y su formato».

La fuente identifica tres clases de fallo: estructural (campos ausentes o tipo incorrecto), de contenido (valor fuera del rango esperado o formato inválido) y de valor (resultado vacío o marcador de posición tratado como válido). Ejemplo: el agente de extracción devuelve `{"amount": "twenty"}` y el agente de facturación espera un número para hacer operaciones. [C:1]

El sobre de salida se define antes de conectar los agentes. Puede especificar tipos —`amount` como número positivo—, valores permitidos —`currency` en `USD`, `EUR` o `GBP`— y reglas de formato —un `email` debe contener `@`. El nodo de protección se coloca entre agentes, lee la salida upstream y compara cada campo con ese sobre. [C:2]

La fuente describe dos resultados: devolver la carga validada sin cambios si pasa, o un error tipado que identifica el campo y la razón si falla. El error puede permitir que el grafo enrute a recuperación. [C:2]

**Qué preguntar:** «¿Qué problema evita que el nodo simplemente registre una advertencia y deje seguir la carga?»

**Respuesta esperada:** una advertencia no detiene la propagación; el nodo debe pasar una carga válida o devolver un error tipado que el flujo pueda manejar. [C:2–3]

## 20–30 min: nodo de protección

**Qué decir (literal):** «El guardrail no repara ni transforma el dato. Su contrato aquí es pasar intacto lo que cumple las reglas y bloquear con un error explícito lo que no las cumple».

La práctica pide que `guardrail_node(state)` lea `state["draft"]`, un diccionario con `amount`, `currency` y `email`. Valida que `amount` sea positivo y no booleano, que `currency` sea uno de `USD`, `EUR` o `GBP`, y que `email` contenga `@`. En éxito devuelve el borrador validado como actualización de estado tipada; en fallo devuelve un objeto de error tipado con el campo y la razón. El nodo es una comprobación pura: no modifica la carga. [C:3]

Fragmento de arranque capturado por el ejercicio; no es una solución completa:

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

**Guía para dirigir el ejercicio:** pedir que el grupo enumere primero los tres predicados, luego determine qué campo falló y, por último, compare la carga devuelta con la original para comprobar que no se transformó. El resultado esperado es el pase del borrador válido y un error tipado para monto negativo, moneda no permitida o email sin `@`. No completar el código de validación con reglas adicionales que la fuente no indique. [C:3]

**Pregunta:** «¿Un `True` debería aceptarse como monto positivo?»

**Respuesta esperada:** no; la práctica excluye explícitamente los booleanos. [C:3]

## 30–41 min: checkpointing y aislamiento por hilo

**Qué decir (literal):** «El guardrail decide si el dato puede seguir. El checkpointing resuelve otra pregunta: si el flujo se pausa o falla, ¿qué estado y qué posición podemos recuperar?»

Un checkpoint es una instantánea persistente del estado del grafo en un punto de ejecución; incluye mensajes, claves personalizadas y posición actual. Con un checkpointer adjunto, LangGraph guarda automáticamente un checkpoint después de cada paso o superpaso. Esto permite recuperar tras una falla, esperar una aprobación y examinar/reproducir un estado anterior al depurar. [P:1–2]

La fuente presenta tres backends:

| Backend | Uso descrito en la fuente |
| --- | --- |
| `InMemorySaver` | Desarrollo y pruebas; no requiere configuración, pero pierde estado al terminar el proceso. |
| `SqliteSaver` | Persistencia en archivo local; sobrevive a reinicios del proceso en un solo nodo. |
| `PostgresSaver` | Estado compartido duradero y multi-trabajador. |

Cada ejecución independiente usa un `thread_id`; cada hilo mantiene su propia línea de tiempo de checkpoints. Omitirlo o reutilizarlo para ejecuciones concurrentes puede sobrescribir o corromper el estado, según la fuente. [P:3]

Ejemplo de configuración e invocación extraído de la lección; `graph` e `inputs` deben existir previamente:

```python
config = {"configurable": {"thread_id": "usuario-42-sesion-1"}}
result = graph.invoke(inputs, config)
```

**Qué preguntar:** «¿Qué dos ejecuciones deben tener hilos distintos?»

**Respuesta esperada:** ejecuciones independientes, especialmente si se ejecutan concurrentemente; el `thread_id` separa sus timelines de checkpoints. [P:3]

## 41–51 min: interrupciones y aprobación humana

**Qué decir (literal):** «Una validación determinista puede resolverse con un guardrail. Si el paso es crítico, irreversible o ambiguo y requiere juicio humano, hacemos una pausa antes de ejecutarlo».

Una interrupción es una pausa explícita dentro del flujo, colocada antes de un nodo crítico o irreversible. En LangGraph, `interrupt(payload)` presenta al exterior la información y las opciones necesarias, y el grafo espera a que lo reanuden. La interrupción necesita un checkpointer para preservar el estado mientras espera. [P:4]

La fuente diferencia los usos: guardrail para una comprobación automática y determinista; interrupción para una decisión que requiere juicio humano. Recomienda pausar antes de la acción irreversible, no después. [P:4]

Fragmento de la fuente:

```python
from langgraph.types import interrupt

def approval_gate(state):
    decision = interrupt({
        "action": "eliminar 12 registros",
        "options": ["aprobar", "rechazar"]
    })
```

Este fragmento muestra el payload y el punto de pausa, no la lógica completa que ejecuta o cancela la acción. [P:4]

**Pregunta:** «¿Pediríamos aprobación humana para comprobar si un email contiene `@`?»

**Respuesta esperada:** no; la fuente lo clasifica como validación automática. La aprobación se reserva para decisiones ambiguas o de alto riesgo. [P:4]

## 51–64 min: reanudar sin repetir la acción

**Qué decir (literal):** «Al reanudar, el grafo usa el mismo hilo y devuelve la decisión al `interrupt()`. Hay un detalle decisivo: el nodo interrumpido vuelve a empezar desde su primera línea».

La fuente muestra `Command(resume=value)` en el mismo `thread_id`. El valor de reanudación se convierte en el valor de retorno de `interrupt()`. Aunque el grafo continúa desde el punto guardado, la función del nodo interrumpido se vuelve a ejecutar desde el principio: el código anterior a `interrupt()` corre en la ejecución inicial y otra vez al reanudar; el código posterior corre después de recibir la respuesta. [P:5]

Por eso, todo lo anterior a `interrupt()` debe carecer de efectos secundarios, y la acción irreversible debe ir después. La respuesta humana o externa se trata como entrada no confiable: validar que esté entre las opciones esperadas, por ejemplo `approve` o `reject`. [P:5]

Ejemplo de reanudación documentado; presupone un grafo, una entrada y un checkpointer configurados:

```python
from langgraph.types import Command

config = {"configurable": {"thread_id": "transfer-1"}}
paused = graph.invoke(inputs, config)
result = graph.invoke(Command(resume="approve"), config)
```

La práctica pide implementar `approval_gate` para una transferencia irreversible: incluir en el payload la transferencia y las opciones `approve`/`reject`, configurar `InMemorySaver`, invocar hasta la pausa y reanudar con `Command(resume=...)` en el mismo `thread_id`. El resultado esperado es que `approve` complete la transferencia exactamente una vez y `reject` la cancele. La captura no proporciona el código completo de solución. [P:6]

**Qué preguntar:** «¿Qué pasaría si enviar el pago ocurre antes de `interrupt()`?»

**Respuesta esperada:** el nodo se ejecuta nuevamente desde el inicio al reanudar, por lo que el efecto podría ejecutarse dos veces. Debe ir después de la interrupción. [P:5–6]

## 64–70 min: chequeo y cierre

**Qué decir (literal):** «Un flujo controlable valida antes de propagar, persiste antes de esperar y valida la decisión antes de actuar. El checkpoint conserva el proceso; no convierte por sí solo una decisión humana en una decisión segura».

Preguntas de cierre:

- «¿Qué distingue un fallo estructural de uno de valor?» Respuesta: campo/tipo ausente o incorrecto frente a un resultado vacío o marcador tratado como válido. [C:1]
- «¿Qué devuelve un guardrail cuando falla?» Respuesta: un error tipado con campo y razón, no `None` ni una mera advertencia. [C:2–3]
- «¿Qué identifica `thread_id`?» Respuesta: la línea de tiempo de checkpoints de una ejecución independiente. [P:3]
- «¿Qué combinación permite esperar y continuar?» Respuesta: interrupción, checkpoint y reanudación. [P:0–1,4–5]
- «¿Dónde se coloca el efecto irreversible?» Respuesta: después de `interrupt()` y solo tras validar la decisión. [P:5–6]

### Ajuste de duración

- Para 60 minutos, reducir el bloque de checkpointing a 7 minutos y el recorrido de práctica a 8; conservar las distinciones guardrail/interrupción y la reejecución del nodo.
- Para 75 minutos, extender la práctica HITL 5 minutos y hacer que los estudiantes recorran por escrito los estados de pausa, `approve` y `reject`; no añadir requisitos fuera del ejercicio capturado.