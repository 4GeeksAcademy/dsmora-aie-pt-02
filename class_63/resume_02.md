# Guía docente: Clase 63 — Introducción a MCP, clientes y servidores

Sesión sugerida de 75 minutos, adaptable a 60. La guía se apoya en los tres cursos almacenados en los JSON de `class_63/`: introducción a MCP, construcción de un cliente MCP y construcción de un servidor MCP con FastMCP. La agenda, las preguntas y las actividades son organización pedagógica; los conceptos y ejemplos técnicos proceden de esos materiales.

## Hilo de continuidad

La clase 62 trató agentes, estado, herramientas y bucles de control. La clase 63 amplía esa idea hacia la integración: ¿cómo pueden agentes compatibles utilizar servidores compatibles sin código personalizado para cada integración? MCP proporciona un protocolo común para esa comunicación.

**Frase de transición:** «En la clase anterior vimos cómo un agente decide solicitar una herramienta y cómo el sistema controla su ejecución. Hoy veremos una forma estándar de conectar ese sistema con capacidades externas: MCP, sus clientes y sus servidores».

## Objetivos de aprendizaje

Al terminar, el estudiante podrá:

- Explicar qué problema de integración busca resolver MCP y cómo se relaciona con las llamadas a funciones.
- Distinguir host, cliente MCP y servidor, incluyendo la relación uno a uno entre una instancia de cliente y su servidor conectado.
- Contrastar herramientas, recursos y prompts según el tipo de capacidad que representan.
- Describir el ciclo de descubrimiento, consentimiento, llamada y retorno de resultado en un cliente.
- Reconocer en los ejemplos el cliente TypeScript con transporte stdio y las capacidades declaradas con FastMCP.
- Enumerar las recomendaciones de uso responsable y seguridad que aparecen en los cursos.

## Agenda sugerida: 75 minutos

| Minutos | Bloque | Resultado esperado |
|---|---|---|
| 0–7 | Apertura y problema M×N | Motivar una integración estandarizada |
| 7–20 | Arquitectura y roles | Trazar host → cliente → servidor y regreso |
| 20–31 | Herramientas, recursos y prompts | Clasificar capacidades |
| 31–44 | Cliente MCP y consentimiento | Explicar descubrimiento y llamada segura |
| 44–58 | Servidor FastMCP | Leer declaraciones de tool, resource y prompt |
| 58–68 | Seguridad y límites | Repasar las recomendaciones de seguridad de las fuentes |
| 68–75 | Evaluación y cierre | Reconstruir el flujo de extremo a extremo |

**Recorte a 60 minutos:** reducir la apertura y el ejemplo de FastMCP; mantener la distinción de roles, las tres capacidades, el ciclo del cliente y el bloque de seguridad.

**Extensión a 90 minutos:** dedicar 15 minutos adicionales a que los equipos tracen sobre papel una solicitud y clasifiquen cada capacidad como herramienta, recurso o prompt. Si se usa el ejemplo FastMCP, la fuente indica `uv add fastmcp` y ejecución local con stdio; el curso del cliente TypeScript es un ejercicio separado que también usa stdio. No combinar ambos como si fueran un único proyecto descrito por los JSON.

## Preparación docente

- Tener disponibles `introduction_to_mcps.json`, `building_an_mcp_client.json` y `building_an_mcp_server.json`.
- Pizarra: dibujar `Agente/Host ↔ Cliente MCP ↔ Servidor MCP` y anotar que el cliente inicia la conexión.
- Preparar tres tarjetas: **acción**, **dato**, **instrucción**. Asociarlas respectivamente con herramienta, recurso y prompt.
- El ejemplo TypeScript usa `@modelcontextprotocol/sdk`, `Client` y `StdioClientTransport`; no presenta un `package.json` ni un proyecto completo.
- El curso de FastMCP indica instalar la dependencia con `uv add fastmcp`. El tutorial presenta la creación del servidor y su ejecución local con stdio. La guía no supone que el ejemplo de FastMCP y el cliente TypeScript formen un mismo proyecto: son lecciones y ejemplos separados.
- El consentimiento del ejemplo se apoya en `getUserConsent(...)`, cuya interfaz se deja explícitamente por implementar.
- Las lecciones finales/evaluaciones de los JSON contienen material repetido. Evitar contabilizar ese contenido duplicado como nuevos temas.

:::floating-note
## Puentes con clases anteriores

- **Clase 62 — Ingeniería agéntica y LangGraph:** el agente puede solicitar una herramienta, pero el sistema que lo rodea controla la ejecución. MCP estandariza el puente hacia servidores que exponen capacidades. MCP no es el bucle del agente ni sustituye su control de flujo.
- **Clase 18 — Tareas simples + Telegram/Composio MCP:** enlaza la familiaridad previa con el nombre MCP. En esta clase se estudian los roles y el protocolo para comprender la integración, no una receta particular de Composio.
- **Clase 23 — Arquitectura avanzada y skills de OpenClaw:** puente pedagógico para conversar sobre capacidades externas y arquitectura de agentes. La distinción de skills y MCP es una comparación docente, no una afirmación derivada de los JSON de la clase 63.
:::

## 0–7 min | Apertura: ¿por qué un protocolo común?

### Qué decir (literal)

«Si cada agente tuviera que integrarse de una manera distinta con cada servicio, volveríamos a construir conexiones particulares una y otra vez. MCP propone un protocolo estándar para que un host pueda comunicarse con servidores que exponen herramientas, datos o prompts».

Presenta la intuición del problema M×N mencionada por el curso: las integraciones particulares crecen con las combinaciones entre aplicaciones y herramientas; con un protocolo común, cada lado implementa una forma estándar de comunicarse. Aclara que es una motivación de arquitectura, no una afirmación de que cualquier servicio se conecte sin trabajo: alguien debe implementar el servidor y el cliente compatibles.

En la lección, MCP se presenta como abierto y agnóstico al modelo. El material lo describe como complementario a las llamadas a funciones, no como reemplazo. Esta frase es una síntesis del contenido de la lección.

**Pregunta:** «¿MCP es el modelo que decide la acción?» → No; es un protocolo de comunicación e integración.

## 7–20 min | Arquitectura y roles

### Qué decir (literal)

«El host contiene la aplicación y al agente. El cliente MCP funciona como conector dentro del host. El servidor MCP es el programa que ofrece las capacidades. El cliente inicia la conexión y habla el protocolo con el servidor».

Dibuja el flujo:

```text
Agente dentro del host
        │ decide solicitar una capacidad
        ▼
Host ── Cliente MCP ── solicitud estándar ──> Servidor MCP
Host <─ Cliente MCP <─ resultado/capacidad ─── Servidor MCP
```

Explica las responsabilidades, siguiendo las definiciones de los cursos:

- **Host:** aplicación con la que interactúa el usuario; posee el modelo y la conversación, y gestiona la experiencia del usuario.
- **Cliente:** conector dentro del host que habla MCP, gestiona la conexión y descubre capacidades. Cada cliente conecta con exactamente un servidor.
- **Servidor:** programa externo que anuncia y expone herramientas, recursos o prompts y responde a las solicitudes.

Un host puede tener distintos clientes para conectar distintos servidores. El curso de introducción añade que el servidor puede enviar notificaciones sobre cambios de estado o actualizaciones de recursos. En el flujo descrito, el servidor ejecuta la herramienta que expone.

**Pregunta de chequeo:** «¿Quién inicia la conexión?» → El cliente.

## 20–31 min | Herramientas, recursos y prompts

### Qué decir (literal)

«Antes de conectar un servidor, clasifiquemos qué está exponiendo. Una herramienta es una acción; un recurso es información disponible para leer; un prompt es una plantilla reutilizable de instrucciones».

Usa los ejemplos de los JSON:

- Crear un ticket o ejecutar una consulta: **herramienta**.
- Leer un archivo, un registro o el recurso `uri://reports/yesterday-sales`: **recurso**.
- Instrucciones para resumir una conversación y listar próximos pasos: **prompt**.

Pide a los estudiantes asignar las tres tarjetas de preparación. Enfatiza que una herramienta puede producir efectos y que no debe confundirse con leer un recurso. La clasificación ayuda al grupo a distinguir los tres tipos de capacidad presentados por el curso.

**Pregunta:** «Si solo necesitamos incorporar el contenido de un documento como contexto, ¿qué capacidad parece adecuada?» → Un recurso. «¿Y si queremos crear un ticket?» → Una herramienta.

## 31–44 min | Cliente: descubrir, consentir, llamar

### Qué decir (literal)

«El cliente puede consultar qué herramientas ofrece el servidor. Descubrir una capacidad no significa ejecutarla: la guía de uso responsable recomienda que el host pida consentimiento explícito mostrando los argumentos reales antes de la llamada».

Lee el ejemplo simplificado del curso:

```typescript
async function discoverTools(client) {
  const { tools } = await client.listTools();
  return tools;
}

async function callToolWithConsent(client, toolName, args) {
  const consent = await getUserConsent(toolName, args);
  if (!consent) return null;
  return await client.callTool({ name: toolName, arguments: args });
}
```

Explica la secuencia: consultar `listTools()`, mostrar o procesar la lista, solicitar consentimiento explícito antes de ejecutar la herramienta, invocar `callTool` con `name` y `arguments`, recibir el resultado. El ejemplo no define cómo se construye la interfaz de consentimiento; esa parte queda marcada como implementación pendiente.

Para conexión en TypeScript, el curso importa `Client` desde `@modelcontextprotocol/sdk/client/index.js` y `StdioClientTransport` desde `@modelcontextprotocol/sdk/client/stdio.js`, crea el cliente con nombre y versión, conecta el transporte y al terminar cierra con `client.close()`. La sección de transportes caracteriza stdio como local (proceso hijo del host, comunicación stdin/stdout, una conexión y sin autenticación porque no hay red); HTTP Streamable como remoto y multi-cliente, con autenticación y autorización. La fuente precisa que HTTP Streamable también puede utilizarse con un servidor en la misma máquina; esa descripción local/remoto es el caso común, no una regla estricta. La unidad de uso responsable señala que incluso stdio requiere consentimiento explícito porque opera con los privilegios de la máquina. El ejemplo TypeScript usa stdio, no es un ejemplo de cliente HTTP remoto.

**Pregunta:** «¿Qué recomienda el curso que se muestre antes de ejecutar una herramienta?» → La operación y sus parámetros.

## 44–58 min | Servidor con FastMCP

### Qué decir (literal)

«En el servidor, las capacidades se implementan y se exponen con contratos claros. FastMCP permite declarar una herramienta con un decorador; también aparecen decoradores para recursos y prompts».

Ejemplo del curso:

```python
from fastmcp import FastMCP

mcp = FastMCP("Mi Servidor")

@mcp.tool
def add(a: int, b: int) -> int:
    return a + b
```

El tipo de las entradas y del retorno hace visible el contrato de `add`. El servidor también puede declarar un recurso identificado por una URI —el ejemplo es un informe de ventas del día anterior— y un prompt que devuelve instrucciones para resumir una conversación.

El curso indica instalar FastMCP con `uv add fastmcp` y describe stdio como transporte predeterminado del servidor FastMCP, útil para desarrollo local y un cliente. Presenta el snippet como patrón de declaración. No mezclarlo con la configuración del cliente TypeScript como si fueran un proyecto integrado.

**Actividad breve:** el grupo señala en el código qué línea crea servidor, cuál publica herramienta y qué información describe la firma de `add`.

## 58–68 min | Seguridad y límites

### Qué decir (literal)

«El curso de servidor advierte que invocar una herramienta puede alterar datos o el estado del sistema; por eso requiere validación estricta de entradas y medidas de seguridad. La introducción recomienda consentimiento explícito, mínimos privilegios y desconfianza hacia servidores desconocidos».

La introducción recomienda consentimiento explícito, mínimos privilegios y desconfianza hacia servidores desconocidos; en su evaluación indica mostrar los argumentos reales y otorgar al servidor solo los privilegios necesarios. También aclara que servidores stdio locales requieren diálogo de consentimiento porque operan con los privilegios de la máquina. El curso del servidor explica que las herramientas ejecutan código y pueden alterar datos o el estado del sistema, por lo que requieren estricta validación de entrada y medidas de seguridad. Para discusión, pide a los grupos que propongan qué revisar en una herramienta; las preguntas numeradas a continuación son propuestas para orientar esa discusión, no requisitos literales adicionales del JSON:

1. ¿La capacidad debe estar expuesta a este host?
2. ¿El nombre y la descripción dejan claro qué hace?
3. ¿Qué argumentos puede aceptar y qué efectos produce?
4. ¿El host necesita pedir consentimiento antes de usarla?
5. ¿La operación debe restringirse o limitarse?

La unidad de transportes caracteriza stdio como local, rápido, sin red, sin autenticación y con una única conexión de cliente; HTTP Streamable se describe como remoto y multi-cliente, con autenticación y autorización. Aclara también que la división local/remoto es el caso común y no una regla estricta: HTTP Streamable puede ejecutarse contra un servidor de la misma máquina. La unidad de uso responsable añade que stdio también requiere consentimiento explícito porque opera con los privilegios de la máquina. No generalizar estos detalles a otros escenarios. Las lecciones repetidas del servidor no aportan una especificación técnica adicional de límites.

**Pregunta:** «¿Qué hábitos de uso responsable se destacan en el curso?» → Consentimiento explícito, mínimos privilegios y desconfianza hacia servidores desconocidos; para herramientas del servidor, estricta validación de entrada y medidas de seguridad.

## 68–75 min | Evaluación y cierre

Pide a parejas que reconstruyan verbalmente esta secuencia: el agente necesita información → host usa cliente → cliente descubre o selecciona capacidad → si se va a ejecutar una herramienta, el host solicita consentimiento explícito y muestra operación y parámetros → solicitud al servidor → servidor ejecuta la herramienta o responde con el recurso solicitado → resultado al host.

Chequeo oral:

- ¿Qué componente aloja al agente? **Host.**
- ¿Cuál habla el protocolo y conecta con un servidor? **Cliente MCP.**
- ¿Dónde se implementa la capacidad expuesta? **Servidor MCP.**
- ¿Acción, dato, instrucciones reutilizables? **Herramienta, recurso, prompt.**
- ¿MCP reemplaza function calling? **No; lo complementa estandarizando el acceso a capacidades externas.**
- ¿Qué diferencia de transporte describe la fuente? **stdio es local, sin red, de conexión única y sin autenticación; HTTP Streamable es multi-cliente y requiere autenticación/autorización. La fuente dice que HTTP Streamable también puede usarse en la misma máquina.**

### Cierre sugerido (literal)

«MCP define un protocolo común entre un host y los servidores que ofrecen capacidades. El cliente conecta, descubre y llama; el servidor ofrece herramientas, recursos o prompts. Los cursos recomiendan consentimiento explícito, mínimos privilegios y cautela con servidores desconocidos; para las herramientas, el curso de servidor destaca validación estricta de entradas y medidas de seguridad».

## Límites y notas de trazabilidad

- Los tres cursos fueron capturados desde los enlaces entregados y los archivos resultantes están en `class_63/`.
- Las lecciones de evaluación/cierre repiten partes de las evaluaciones de conocimiento. En el curso de servidor hay texto repetido del ejercicio de búsqueda de productos. Esta guía no los presenta como teoría nueva.
- Los ejemplos TypeScript y FastMCP muestran componentes y patrones, no un proyecto integrado que conecte los tres cursos.
- El material no desarrolla una política general de autorización ni configura un despliegue remoto completo. No inferir mecanismos adicionales a los descritos para el consentimiento, el principio de menor privilegio, la desconfianza de servidores desconocidos y los transportes. Algunas lecciones de evaluación/cierre repiten contenido previo; en el curso del servidor se repite también el ejercicio de búsqueda `phone`.
