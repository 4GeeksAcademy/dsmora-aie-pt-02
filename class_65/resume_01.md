# Guía docente — Clase 65: Guardrails e ingeniería de harness

> Duración base: 70 minutos. Fuentes técnicas: `guardrails.json`, `harness_engineering.json` e `implementing_a_harness_in_langgraph.json`. La secuencia, los tiempos y las preguntas son estructura docente; los conceptos, ejemplos y resultados técnicos proceden de esos JSON.

## Continuidad y objetivo

La clase 64 trabajó qué información conserva un agente y cómo se organiza su memoria. Esta sesión amplía el foco: cómo el sistema que rodea al modelo controla sus herramientas, verifica sus acciones, limita riesgos y registra su comportamiento. Frase de transición: «Ya pensamos qué contexto necesita el agente; ahora veremos qué controles hacen que actuar con ese contexto sea confiable».

Al finalizar, el estudiante podrá:

- Explicar la ecuación `Agente = Modelo + Harness` y nombrar las cinco capas del harness descritas en el material.
- Distinguir fallos estructurales, de contenido y de seguridad, y asociarlos con controles apropiados.
- Explicar dónde se conectan las verificaciones de llamadas a herramientas y de respuestas en un grafo.
- Describir una lista permitida, una regla de argumentos y un límite de pasos usando el ejemplo de soporte de la clase.

## Preparación del profesor

- Tener abiertos los tres JSON y preparar en pantalla los fragmentos de esquema y `check_call` incluidos en esta guía.
- Para la práctica documentada, el comando de la fuente es `python app.py`. La fuente no especifica comandos de instalación ni el entorno requerido; no añadas pasos de configuración no incluidos en el material.
- No se capturó ningún prompt de OpenClaw en los JSON. No se incluye uno para evitar inventar instrucciones.
- El scraper repitió el contenido de la práctica de descuentos en las tarjetas posteriores de LangGraph; la tarjeta de evaluación también repite contenido anterior en los otros dos tutoriales. Usa las tarjetas únicas identificadas en esta guía y no presentes esas repeticiones como lecciones distintas.

## Agenda de 70 minutos

- **0–5 min | Caso de apertura:** conectar un error de agente con una acción de impacto real.
- **5–12 min | Modelo y harness:** definir qué aporta cada uno y repasar las cinco capas.
- **12–22 min | Taxonomía de fallos:** clasificar estructura, contenido y seguridad.
- **22–34 min | Controles en capas:** validar estructura, filtrar contenido y controlar acciones.
- **34–43 min | WAT y orquestación:** ubicar workflow, agent y tools; ordenar llamadas y manejo de errores.
- **43–55 min | Puntos de verificación en LangGraph:** proteger llamadas y respuestas; recorrer las reglas del ejemplo.
- **55–65 min | Práctica y evaluación:** probar los casos de descuento y justificar cada bloqueo.
- **65–70 min | Cierre:** recuperar el principio de diseño y comprobar comprensión.

## Guion de clase

### 0–5 min: abrir con el riesgo

**Qué decir (literal):** «Un agente de soporte reembolsó 400 dólares en un pedido de 40 porque nadie comprobó el importe. El modelo produjo una acción plausible; lo que faltó fue código alrededor que decidiera si esa acción estaba permitida».

Presentar los otros ejemplos del material: ofrecer un descuento del 90 % porque el cliente insistió, anunciar un reembolso de 45 dólares para un pedido de 40 y repetir una consulta a una herramienta sin llegar a responder.

**Pregunta:** «¿En qué se diferencia el error de un chatbot que responde mal del error de un agente que ejecuta una acción incorrecta?»

**Respuesta esperada:** el agente puede afectar sistemas, datos o personas; por eso el error puede tener consecuencias financieras, de privacidad o de seguridad.

### 5–12 min: el harness alrededor del modelo

**Qué decir (literal):** «La ecuación de esta clase es `Agente = Modelo + Harness`. El modelo aporta capacidad para entender y generar; el harness es el sistema, las herramientas, los controles y las salvaguardas que lo vuelven confiable en un escenario real».

Enumerar las cinco capas de producción que aparecen en el JSON: orquestación de herramientas, bucles de verificación, contexto y memoria, guardrails y observabilidad. El harness determina qué herramientas se llaman y en qué orden, qué contexto recibe el modelo, qué se verifica y qué comportamiento queda registrado.

Recuperar la mentalidad de ingeniería del material: cada error debe convertirse en una solución para que ese error no vuelva a ocurrir, normalmente mejorando el harness y no esperando que un modelo distinto lo resuelva.

**Pregunta de chequeo:** «Si el agente entrega código defectuoso porque nunca ejecuta pruebas, ¿qué parte del sistema conviene mejorar?»

**Respuesta esperada:** el harness, añadiendo un bucle que verifique el trabajo antes de entregarlo.

### 12–22 min: tres clases de fallo

**Qué decir (literal):** «No hay una sola clase de error. El material separa fallos estructurales, de contenido y de seguridad; como son distintos, requieren verificaciones distintas».

- **Estructural:** la forma no cumple el contrato esperado. Ejemplo del curso: `{"refund": "yes"}` no satisface un campo booleano; `{"refund": true}` sí expresa un booleano.
- **Contenido:** la estructura puede ser correcta y aun así incluir algo falso o dañino. El ejemplo del curso es afirmar una garantía de igualación de precio de 30 días que la empresa nunca ofreció.
- **Seguridad:** la acción o el contenido expone información sensible o permite una acción no autorizada. El material usa la filtración de información personal y las herramientas no permitidas como ejemplos.

**Qué preguntar después:** «Un JSON válido que contiene una política inventada, ¿es un fallo estructural o de contenido?» y «¿Qué tipo de fallo hay si el agente intenta usar `delete_account` aunque esa herramienta no está permitida?»

**Respuestas esperadas:** contenido; seguridad.

### 22–34 min: controles concretos y defensa en capas

**Qué decir (literal):** «Un guardrail es una comprobación programática alrededor de entradas, salidas o acciones. No es solo una instrucción amable en el prompt: es una regla que el sistema puede comprobar».

Explicar la separación que describe el curso:

- La validación de entradas comprueba y sanitiza lo que llega al agente.
- La validación de salidas comprueba la respuesta antes de entregarla o procesarla.
- Los controles de acciones verifican lo que el agente intenta hacer.

Para el fallo estructural, presentar el esquema JSON de reembolsos del material. La forma requiere `refund` booleano y `amount` numérico, y no permite campos adicionales. El curso menciona AJV para validar la salida contra el esquema; si falla, se rechaza o se solicita una corrección antes de continuar.

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

**Qué decir (literal):** «Este esquema no decide si el reembolso es justo. Comprueba la forma: que `refund` sea booleano, que `amount` sea numérico, que ambos estén presentes y que no aparezcan otros campos».

Para fallos de contenido, el material propone filtros y clasificadores; para seguridad, validaciones de entrada y controles de las acciones. Reforzar el principio «un guardrail nunca es suficiente»: estructura, contenido y seguridad son fallos diferentes, por lo que se superponen verificaciones en lugar de confiar en una única barrera.

**Pregunta de chequeo:** «¿El esquema anterior impediría por sí solo que se solicite un reembolso mayor que el total del pedido?»

**Respuesta esperada:** no; la forma puede ser válida y el importe seguir siendo incorrecto. Hace falta una regla de acción que compare el importe con el pedido.

### 34–43 min: WAT y orquestación de herramientas

**Qué decir (literal):** «WAT separa el workflow, el agent y las tools. El workflow establece el orden, las condiciones, los límites y las verificaciones; el agent decide el siguiente paso; cada tool realiza una acción concreta y devuelve datos o un error claro».

Mapearlo al LangGraph descrito en la fuente: el `StateGraph`, sus nodos y aristas implementan el workflow; el nodo que llama al modelo implementa el agent; las funciones decoradas con `@tool` son las tools. El agente accede a las herramientas a través del workflow.

En la orquestación, señalar las prácticas explícitas del material: definir esquemas de entrada y salidas esperadas, devolver errores claros como «Ruta inválida» o «Permiso denegado», secuenciar llamadas con verificaciones después de cada paso, y usar valores predeterminados y validación de entradas.

**Pregunta:** «¿Por qué conviene que una herramienta devuelva un error detallado en vez de fallar silenciosamente?»

**Respuesta esperada:** el agente y el workflow pueden detectar el problema y responder o recuperarse de forma adecuada.

### 43–55 min: dos puntos de conexión para verificar

**Qué decir (literal):** «El nodo agent produce una solicitud de herramienta o una respuesta final. El harness tiene dos bordes claros donde comprobar esas dos salidas».

En el grafo del curso:

1. **Antes de ejecutar la herramienta:** el borde entre `agent` y `tools` pasa por `guard`. Aquí se restringe la acción. Si se bloquea, se devuelve al agente la razón para que pueda corregirse.
2. **Antes de mostrar la respuesta:** el borde entre `agent` y `END` pasa por `verify`. Aquí se valida la respuesta final. Si se rechaza, se devuelve la razón al agente.

Ambas comprobaciones tienen una salida `fallback`; el grafo limita los pasos y los rechazos para que no repita indefinidamente y siempre termine. La fuente describe los nombres de nodos y el flujo, pero las tarjetas posteriores que desarrollarían la verificación de respuestas fueron capturadas con contenido duplicado; no añadir una implementación que no aparece en los JSON.

**Qué preguntar después:** «¿Dónde pondrías la regla que impide una herramienta desconocida: antes de ejecutarla o después?» y «¿Dónde comprobarías que el texto final no afirma un reembolso incorrecto?»

**Respuestas esperadas:** antes de ejecutar la herramienta, en `guard`; antes de entregar la respuesta, en `verify`.

### 55–65 min: práctica guiada de descuentos

Presentar el caso del curso: el agente puede usar `lookup_order` y `apply_discount`; el descuento no debe superar `MAX_PERCENT = 30`. La función `check_call(call)` recibe una llamada a herramienta y devuelve una razón breve (cadena) si debe bloquearse, o `None` si se puede ejecutar. `guard(state)` inspecciona las llamadas del último mensaje; si no hay bloqueos devuelve una actualización vacía, y si los hay devuelve mensajes de herramienta con las razones y las enumera bajo `blocks`.

**Qué decir (literal):** «Vamos a probar tres casos sin cambiar de modelo: una llamada permitida, un porcentaje fuera del límite y una herramienta que no está en la lista. El comportamiento esperado lo determina el guard».

El material propone ejecutar el archivo del ejercicio con este comando:

```bash
python app.py
```

Resultados esperados documentados por la fuente, en ese orden:

```text
{}
['percent debe ser un número entero del 1 al 30']
["herramienta 'delete_account' no está permitida"]
```

El primer resultado corresponde al descuento del 10 %, el segundo al 90 % y el tercero a la herramienta no permitida `delete_account`. El JSON proporciona el enunciado y esos resultados, pero no el archivo `app.py`; presenta el comando como la instrucción de ejecución del ejercicio, no como algo que se pueda ejecutar desde esta carpeta sin preparar el proyecto del curso.

**Preguntas para el grupo:**

- «¿Qué comprueba el límite del porcentaje y en qué punto del flujo debe aplicarse?»
- «¿Por qué el caso de `delete_account` se clasifica como seguridad?»
- «¿Qué debería ocurrir con la llamada antes de que `apply_discount` llegue a ejecutarse?»

**Respuestas esperadas:** la regla valida el argumento antes de ejecutar la herramienta; `delete_account` no está en la lista permitida; el guard la bloquea y comunica una razón.

### 65–70 min: cierre

**Cierre sugerido (literal):** «La confiabilidad no depende de pedirle al modelo que tenga cuidado. Diseñamos el workflow para controlar herramientas, verificar resultados, limitar repeticiones y hacer explícitas las reglas. Cuando aparece un fallo, añadimos al harness la comprobación que lo evita la próxima vez».

Comprobar que cada estudiante puede nombrar los tres tipos de fallo, elegir un control para cada uno y ubicar una verificación antes de la herramienta y otra antes de la respuesta final.

## Variantes de duración

- **Para 60 minutos:** reducir el caso de apertura a 3 minutos, la explicación de WAT a 6 minutos y la práctica a 7 minutos; conservar la clasificación de fallos y los dos puntos de verificación.
- **Para 75 minutos:** dedicar 5 minutos adicionales a que los estudiantes clasifiquen los tres resultados de la práctica y 5 minutos a que propongan una verificación para cada clase de fallo.

## Checklist de salida

- ¿El estudiante distingue formato inválido, contenido falso y acción no autorizada?
- ¿Puede explicar qué capa del harness controla el orden, los argumentos y los límites?
- ¿Puede ubicar `guard` antes de `tools` y `verify` antes de `END`?
- ¿Puede explicar por qué una instrucción del prompt no reemplaza una comprobación programática?