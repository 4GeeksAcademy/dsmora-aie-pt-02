# Dossier de referencia — Guardrails e ingeniería de harness

## Propósito y alcance

Este documento organiza los contenidos de `guardrails.json`, `harness_engineering.json` e `implementing_a_harness_in_langgraph.json` para servir como fuente de consulta en NotebookLM. Integra los conceptos comunes, explica la relación entre las capas de un harness y la implementación de guardrails en LangGraph, e incluye ejemplos de los JSON. No es un guion de clase ni una transcripción literal. Las afirmaciones técnicas y los ejemplos se limitan al material extraído; cuando una captura se repite o no contiene una implementación completa, se indica expresamente.

Los dos primeros tutoriales cubren qué es un harness, los tipos de fallos que previenen los guardrails, la orquestación de herramientas, los bucles de verificación, el contexto y la memoria, y la observabilidad. El tercer tutorial lleva esas ideas a un agente de soporte implementado con un grafo: presenta WAT, ubica dos puntos de verificación y desarrolla restricciones sobre llamadas a herramientas. Varias tarjetas de LangGraph posteriores a la práctica de descuentos contienen la misma captura repetida, por lo que este dossier no las trata como implementaciones independientes de verificación de respuestas.

## 1. Por qué el agente necesita un harness

El material distingue al chatbot que produce texto de un agente que además puede actuar sobre sistemas, datos o personas. Una respuesta incorrecta puede ser confusa; una acción incorrecta puede producir consecuencias financieras, exponer datos privados o afectar otros sistemas. Entre los casos de riesgo presentados están un reembolso no autorizado, una respuesta con información personal sensible y un descuento excesivo.

La ecuación central es:

> **Agente = Modelo + Harness**

El **modelo** aporta capacidad de comprensión, generación y razonamiento. El **harness** es el sistema que lo rodea: herramientas y su gestión, contexto y memoria, controles de seguridad, verificaciones y observabilidad. El harness convierte capacidades del modelo en un agente que puede operar con límites y comprobaciones explícitas.

La mentalidad de ingeniería propuesta por las fuentes es tratar cada error como información de diseño: cuando el agente falla, se añade o mejora la comprobación del harness que evita ese fallo en el futuro, en lugar de confiar únicamente en que el modelo se comporte mejor.

## 2. Cinco capas del harness de producción

El tutorial de ingeniería de harness enumera cinco capas que trabajan en conjunto:

1. **Orquestación de herramientas:** define qué herramientas están disponibles, sus parámetros y resultados, el orden de las llamadas y el manejo de errores.
2. **Bucles de verificación:** revisan el trabajo del agente y permiten corregirlo antes de entregar el resultado.
3. **Contexto y memoria:** deciden qué información relevante recibe el modelo en una llamada.
4. **Guardrails:** validan entradas, salidas y acciones para impedir comportamientos que incumplen reglas.
5. **Observabilidad:** registra y expone el comportamiento del agente para poder seguirlo y diagnosticarlo.

Estas capas no sustituyen al modelo: controlan el flujo que lleva de una decisión del modelo a una herramienta o a una respuesta final. La fuente señala que un agente de codificación puede ejecutar pruebas sobre su propio código antes de entregarlo, que un agente de soporte puede retirar información sensible de sus respuestas y que un agente de datos puede registrar sus pasos para facilitar el diagnóstico.

### 2.1 Contexto y observabilidad

El harness debe proporcionar solo los documentos o fragmentos pertinentes para la tarea, en vez de incluir indiscriminadamente toda la información disponible. El ejemplo de soporte al cliente es seleccionar los tickets recientes relevantes y las preguntas frecuentes, no entregar al agente toda la base de datos de la empresa. El material atribuye a este contexto enfocado respuestas más centradas, menor sobrecarga de información y un uso más eficiente del procesamiento.

La observabilidad consiste en rastrear y registrar el comportamiento del agente. Es una de las cinco capas identificadas; las capturas disponibles no desarrollan una API o implementación concreta de logging, así que no se prescribe aquí una herramienta o formato de trazas.

## 3. WAT: responsabilidades separadas

La implementación de LangGraph utiliza el marco **WAT** para separar el workflow, el agent y las tools:

- **Workflow:** qué ocurre, en qué orden y bajo qué condiciones. Posee la secuencia, los límites y las verificaciones. En LangGraph corresponde al `StateGraph`, sus nodos y sus aristas.
- **Agent:** la parte que razona y decide el siguiente paso usando el contexto recibido. En LangGraph corresponde al nodo que llama al modelo.
- **Tool:** una capacidad acotada que el agent puede solicitar. Realiza una acción específica y devuelve datos o un error claro. En LangGraph corresponde a funciones decoradas con `@tool`.

El agente está dentro del workflow y accede a las herramientas a través de él. El ejemplo de estructura de archivos que aparece en la fuente separa `workflow.py`, `agent.py` y `tools.py` para reflejar esas responsabilidades. Esta separación permite localizar si un problema viene del orden de ejecución, de una decisión del modelo o de una herramienta.

## 4. Tres clases de fallo y sus comprobaciones

Las fuentes distinguen tres clases de fallo. No conviene tratarlas como un único problema, porque requieren controles diferentes.

### 4.1 Fallos estructurales

La salida no cumple el formato o esquema esperado. Puede contener información que parece correcta, pero su estructura rompe a los sistemas posteriores. El ejemplo de reembolso contrasta:

```json
{"refund": "yes"}
```

con:

```json
{"refund": true}
```

Si `refund` debe ser booleano, el primer valor es una cadena y no satisface el contrato; el segundo sí es booleano. El material propone validación de esquema y rechazar la salida o pedir una corrección si no coincide.

El tutorial muestra este esquema para un objeto con `refund` booleano y `amount` numérico:

```javascript
const refundSchema = {
  type: "object",
  properties: {
    refund: { type: "boolean" },
    amount: { type: "number" }
  },
  required: ["refund", "amount"],
  additionalProperties: false
};
```

`required` exige ambos campos y `additionalProperties: false` prohíbe otros campos. La fuente menciona AJV para comprobar la salida contra el esquema. La validación estructural comprueba la forma; por sí sola no determina si el importe del reembolso es correcto respecto del pedido.

### 4.2 Fallos de contenido

La estructura puede ser válida y el contenido incorrecto o dañino. Un ejemplo es afirmar con seguridad una garantía de igualación de precio de 30 días que la empresa nunca ofreció. El material también identifica alucinaciones y afirmaciones falsas con confianza como fallos de contenido. Para esta clase menciona filtros y clasificadores; no presenta un único filtro que resuelva todos los casos.

### 4.3 Fallos de seguridad

Una acción no autorizada o una fuga de información sensible constituye un fallo de seguridad. La fuente incluye el uso de una herramienta que el agente no debería tocar y la exposición de PII como ejemplos. Una lista permitida de herramientas es una comprobación concreta: cualquier nombre que no pertenezca al conjunto autorizado se bloquea antes de llegar a la herramienta.

### 4.4 Defensa en capas

El principio que las fuentes recalcan es que un guardrail no basta para todos los fallos. Una salida puede pasar el esquema y contener una afirmación falsa; una respuesta correcta puede acompañarse de una acción no autorizada. Por tanto, el harness combina controles sobre entradas, estructura de salidas, contenido y acciones.

## 5. Orquestación de herramientas y verificación

La orquestación administra qué herramienta se llama, en qué orden y cómo se manejan errores. El tutorial recomienda:

- Esquemas de entrada claros y salidas esperadas para cada herramienta.
- Errores detallados y predecibles, en vez de fallos silenciosos o ambiguos.
- Secuenciación lógica de llamadas y comprobaciones después de cada paso.
- Valores predeterminados sensatos y validación de entradas.

Una herramienta de escritura de archivos, por ejemplo, debería poder indicar «Ruta inválida» o «Permiso denegado» para que el agente pueda reaccionar. La fuente presenta los bucles de verificación como una capa que comprueba el trabajo y, cuando hace falta, conduce a una corrección antes de presentar el resultado.

El curso de LangGraph sitúa las verificaciones en dos bordes porque el nodo agente produce una de dos cosas: una solicitud para llamar a una herramienta o una respuesta final.

### 5.1 Antes de ejecutar una herramienta: restricción

El borde de `agent` hacia `tools` pasa por el nodo `guard`. Esta comprobación impide que una llamada inválida llegue a ejecutarse. Si bloquea una llamada, devuelve al agente una razón para que pueda corregirla. Este guard controla restricciones como el nombre permitido de la herramienta y la validez de sus argumentos.

### 5.2 Antes de entregar la respuesta: validación

El borde de `agent` hacia `END` pasa por el nodo `verify`. Esta verificación revisa la respuesta final antes de que llegue al usuario. Si la rechaza, el flujo puede devolver la razón al agente para intentar corregirla.

El grafo descrito también incluye un `fallback` y límites de pasos y rechazos. Esos límites evitan que los rechazos generen un ciclo sin fin y ofrecen una salida para que el grafo termine. En los JSON capturados, las tarjetas tituladas “Verificando la respuesta”, “Construyendo el bucle de verificación” y “Rechazar una respuesta no verificada” repiten la práctica de descuentos en vez de proporcionar su implementación. Por eso el nodo `verify` se describe aquí al nivel del flujo que sí aparece, sin inventar una regla de validación, una función o código para ese nodo.

## 6. Restricciones: reglas aplicables antes de la acción

El curso contrasta una instrucción de prompt con una restricción. “Nunca reembolsar más que el total del pedido” es una petición al modelo; no garantiza que la llamada no ocurra. Una restricción es código en el camino hacia la herramienta: la llamada no llega a ejecutarse sin pasar por esa comprobación.

El curso de LangGraph enumera tres restricciones asociadas a errores distintos:

- **Lista blanca de herramientas:** elimina llamadas a nombres que el agente no debe poder usar.
- **Reglas de argumentos:** validan estructura y valores, como un importe positivo o un porcentaje dentro del rango permitido.
- **Límite de pasos:** impide que el agente siga llamando herramientas repetidamente sin terminar.

En el ejemplo de reembolsos del nodo guardián, el material configura `ALLOWED_TOOLS` con `lookup_order` e `issue_refund` y `MAX_STEPS` con `6`. La función `check_call(call)` devuelve `None` si la llamada pasa las comprobaciones o una categoría de fallo y una razón si se debe bloquear. Para `issue_refund`, comprueba que `amount` sea un número positivo, que exista el pedido indicado en `ORDERS` y que el importe no supere el total del pedido. Una herramienta desconocida se clasifica como seguridad; un argumento mal formado, como estructural; un pedido inexistente o un importe que excede el total, como contenido, según el ejemplo.

El fragmento fuente es ilustrativo: depende de `ORDERS`, que no se define en ese extracto. No constituye por sí solo una aplicación ejecutable.

## 7. Práctica documentada: proteger descuentos

La actividad propone añadir `apply_discount` a un agente de soporte. La lista permitida es `lookup_order` y `apply_discount`, y `MAX_PERCENT` vale `30`. El objetivo es bloquear llamadas antes de ejecutar una herramienta cuando el porcentaje no es un entero dentro del rango permitido o cuando se solicita una herramienta ajena a la lista.

La función `check_call(call: dict) -> str | None` debe devolver una razón breve cuando la llamada se bloquea y `None` cuando puede continuar. El nodo `guard(state)` lee las llamadas de herramienta del último mensaje. Si ninguna debe bloquearse, devuelve una actualización vacía; si encuentra bloqueos, responde a las llamadas mediante `ToolMessage` con la razón y lista esas razones bajo `blocks`.

Los resultados que la lección indica para el archivo de ejercicio `app.py` son:

```text
{}
['percent debe ser un número entero del 1 al 30']
["herramienta 'delete_account' no está permitida"]
```

Corresponden, en ese orden, a un descuento del 10 %, uno del 90 % y una llamada a `delete_account`. El comando de ejecución indicado por la propia lección es:

```bash
python app.py
```

La captura incluye el enunciado, el contrato de las funciones y esos resultados esperados, pero el código completo de `check_call` y `guard` aparece concatenado y truncado. El archivo `app.py` no forma parte de los JSON ni de esta carpeta de clase; por tanto, no se debe asumir que el comando se pueda ejecutar aquí sin los archivos del ejercicio.

## 8. Flujo conceptual de extremo a extremo

El flujo descrito puede resumirse así, sin añadir pasos de implementación que no aparezcan en las fuentes:

1. El `workflow` define el grafo, sus límites y sus verificaciones.
2. El nodo `agent` recibe contexto y decide si solicita una herramienta o produce una respuesta final.
3. Si solicita una herramienta, `guard` valida nombre y argumentos antes de la ejecución.
4. Si la llamada está permitida, el nodo de herramientas la ejecuta y devuelve datos o un error claro.
5. El agente puede usar ese resultado para decidir el siguiente paso; el workflow aplica sus límites.
6. Si el agente produce una respuesta final, `verify` la revisa antes de `END`.
7. Una corrección vuelve al agente con la razón; un `fallback` y los límites permiten terminar el flujo.
8. La observabilidad registra el comportamiento del agente para poder seguirlo y diagnosticarlo.

La descripción de los nodos de restricción y validación es de nivel de flujo, no una implementación completa del grafo. Las fuentes no proporcionan aquí un programa ejecutable integrado con todas las funciones auxiliares y dependencias definidas.

## 9. Ejemplos y resultados para consulta

### Clasificación rápida de fallos

| Situación de las fuentes | Clase de fallo | Comprobación que corresponde al material |
|---|---|---|
| Falta un campo requerido o `refund` viene como cadena en vez de booleano | Estructural | Validar el esquema; rechazar o pedir corrección |
| El agente afirma una garantía de 30 días inexistente | Contenido | Filtros o clasificadores de contenido |
| El agente llama `delete_account` sin estar permitida | Seguridad | Lista blanca en `guard`, antes de ejecutar la herramienta |
| El agente pide 90 % cuando `MAX_PERCENT` es 30 | Argumento/regla de negocio del ejemplo | Bloquear la llamada antes de ejecutar `apply_discount` |
| El agente intenta reembolsar más que el total del pedido | Contenido en la clasificación del ejemplo de `check_call` | Comparar el importe solicitado con el total del pedido |

### Preguntas de evaluación recuperables de los tutoriales

- ¿Qué expresa `Agente = Modelo + Harness`? Que al modelo en bruto se agregan herramientas, verificación, contexto, guardrails y observabilidad.
- ¿Qué tipo de fallo es un JSON con un campo requerido ausente? Estructural.
- ¿Qué tipo de fallo es afirmar una política de devoluciones inexistente? Contenido.
- ¿Qué comprueba una lista permitida? Que el nombre de herramienta solicitado esté autorizado.
- ¿En qué puntos se conecta el harness? Antes de ejecutar una herramienta y antes de entregar una respuesta final.
- ¿Por qué una regla escrita solo en el prompt no es una restricción? Porque solicita un comportamiento, pero no impide programáticamente que la llamada alcance la herramienta.

## 10. Límites de los contenidos capturados

- En los tutoriales de guardrails e ingeniería de harness, la tarjeta final de conclusión repite el contenido de la evaluación anterior.
- En el tutorial de implementación con LangGraph, las cinco tarjetas posteriores a la actividad de descuentos repiten el contenido de esa actividad. No contienen las lecciones anunciadas sobre verificación de respuestas, construcción del bucle, rechazo, evaluación y conclusión.
- Algunos fragmentos de código aparecen concatenados con el texto o truncados. En los casos anteriores se han descrito los contratos y resultados visibles, no se han reconstruido líneas ausentes.
- Las capturas no incluyen un `app.py` completo ni una aplicación integrada. El comando `python app.py` y los resultados se reproducen como instrucciones y expectativas escritas en el tutorial, no como una validación de ejecución local.
- Los conceptos técnicos de este dossier proceden únicamente de los tres JSON. La organización, las tablas y los resúmenes son estructura editorial para facilitar la consulta en NotebookLM.
