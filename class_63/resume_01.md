# Lectura de estudio — Clase 63: MCP, clientes y servidores

> Síntesis técnica basada en las lecciones capturadas en `introduction_to_mcps.json`, `building_an_mcp_client.json` y `building_an_mcp_server.json`. Se mantienen los nombres y ejemplos técnicos de los JSON. La secuencia expositiva es editorial; las afirmaciones técnicas siguientes corresponden a la fuente capturada.

## 1. Qué es MCP y qué problema aborda

El Model Context Protocol (MCP) se presenta como un protocolo común entre agentes/hosts y servidores que exponen herramientas, datos y prompts. El curso lo presenta como una solución al problema de construir integraciones particulares entre múltiples agentes y múltiples herramientas: agentes compatibles pueden usar servidores compatibles sin código personalizado para cada integración. El material lo describe como complementario a las llamadas a funciones, no como reemplazo.

El material presenta MCP como el protocolo que define la comunicación entre los componentes descritos en los cursos.

## 2. Host, cliente y servidor

Los cursos describen tres roles:

- **Host:** la aplicación con la que interactúa el usuario. Posee el modelo y la conversación, y gestiona la experiencia del usuario. El curso de introducción lo ilustra con aplicaciones como un IDE o una aplicación de chat.
- **Cliente MCP:** conector dentro del host que habla MCP, gestiona la conexión y permite descubrir capacidades. Cada cliente mantiene una conexión uno a uno con un servidor; si un host conecta varios servidores, usa clientes para esas conexiones.
- **Servidor MCP:** programa externo que expone capacidades —herramientas, recursos o prompts— y responde a solicitudes del cliente. El cliente inicia la conexión. La introducción indica también que el servidor puede enviar notificaciones sobre cambios de estado o actualizaciones de recursos.

En el flujo descrito, el agente/host decide que necesita una capacidad; el cliente envía una solicitud MCP al servidor; el servidor proporciona el recurso o ejecuta la herramienta y devuelve el resultado; el host incorpora el resultado a la conversación o al contexto del agente.

## 3. Herramientas, recursos y prompts

El curso de arquitectura distingue tres tipos de capacidad:

- **Herramienta (tool):** acción invocable, por ejemplo leer o escribir archivos, crear un ticket o ejecutar una consulta. El curso del servidor señala que las herramientas ejecutan código y pueden cambiar datos o el estado del sistema.
- **Recurso (resource):** datos que el servidor ofrece para lectura y uso como contexto; por ejemplo contenido de un archivo o registro. El ejercicio de FastMCP expone un recurso con URI `uri://reports/yesterday-sales` que devuelve un total y una moneda.
- **Prompt:** plantilla de instrucciones reutilizable. El ejemplo FastMCP `summarize_conversation` devuelve instrucciones para resumir los puntos clave y los próximos pasos.

La elección depende de la capacidad que se desea exponer: una acción, datos de lectura o una plantilla de instrucciones.

## 4. Descubrir y llamar herramientas desde un cliente

Una vez conectado, el cliente puede descubrir herramientas con `client.listTools()`. Para ejecutar una, el ejemplo del curso llama `client.callTool({ name: toolName, arguments: args })`. El ciclo conceptual presentado es descubrir las herramientas, decidir cuál se necesita, llamar la herramienta con nombre y argumentos y devolver el resultado al host.

El material del cliente muestra el consentimiento explícito como parte de este ciclo. En su ejemplo, `getUserConsent(toolName, args)` representa una función de interfaz pendiente de implementar; si no hay consentimiento, la función retorna sin llamar la herramienta. La introducción especifica que el host debe pedir siempre consentimiento explícito antes de ejecutar una herramienta y mostrar la operación y sus parámetros.

Fragmento representativo de la fuente:

```typescript
const { tools } = await client.listTools();
const consent = await getUserConsent(toolName, args); // Implementar prompt UI
if (!consent) return null;
const result = await client.callTool({ name: toolName, arguments: args });
```

El curso de cliente presenta un cliente TypeScript importando `Client` desde `@modelcontextprotocol/sdk/client/index.js` y `StdioClientTransport` desde `@modelcontextprotocol/sdk/client/stdio.js`. El cliente se crea con nombre y versión, se conecta mediante `client.connect(transport)`, puede descubrir y llamar herramientas y se cierra con `client.close()`. La lección de conexión incluye un ejercicio con un servidor MCP local y transporte stdio.

## 5. Transportes presentados

La lección «Transportes» del curso de introducción describe dos opciones:

- **stdio:** la fuente lo caracteriza como local y rápido: el servidor se ejecuta como proceso hijo de la aplicación host y la comunicación usa stdin/stdout. No hay red, no se requiere autenticación y soporta una única conexión de cliente. La lección de uso responsable aclara que aun así se requiere consentimiento explícito, porque opera con los privilegios de la máquina.
- **HTTP Streamable:** la fuente lo describe para servicios remotos y compartidos: admite múltiples clientes y requiere autenticación y autorización. La división local/remoto es el caso común, no una regla estricta; la lección dice que HTTP Streamable también puede ejecutarse contra un servidor en la misma máquina.

El curso de FastMCP presenta ejecución local con stdio. El ejemplo del cliente TypeScript también emplea `StdioClientTransport`; no es un ejemplo de cliente HTTP Streamable.

## 6. Servidor con FastMCP

El curso de servidor muestra FastMCP en Python. La instrucción de instalación que aparece es `uv add fastmcp`. Después se instancia el servidor con un nombre:

```python
from fastmcp import FastMCP

mcp = FastMCP("Mi Servidor")
```

Se exponen capacidades mediante decoradores:

```python
@mcp.tool
def add(a: int, b: int) -> int:
    return a + b
```

La fuente presenta además `@mcp.resource("uri://reports/yesterday-sales")` para exponer el recurso de ventas, y `@mcp.prompt` para una instrucción de resumen de conversación. Para ejecutar el servidor, la lección indica `mcp.run()` y señala stdio como transporte predeterminado del ejemplo.

Los fragmentos ilustran la declaración y ejecución local descritas por el tutorial; el curso del cliente TypeScript y el del servidor FastMCP son cursos/ejercicios separados, no un proyecto integrado único.

## 7. Uso responsable y seguridad

El curso de introducción presenta tres hábitos: consentimiento explícito, mínimos privilegios y desconfianza hacia servidores desconocidos. En las preguntas de evaluación recomienda que el host pida consentimiento explícito mostrando los argumentos reales, y que solo otorgue al servidor los privilegios necesarios para su trabajo. Añade que servidores stdio locales aún requieren diálogos de consentimiento explícito porque operan con los privilegios de la máquina. El curso del cliente destaca también el consentimiento explícito y el principio de menor privilegio.

El curso del servidor indica que las herramientas pueden tener consecuencias porque ejecutan código y pueden alterar datos o estado; por eso requieren validación estricta de entradas y medidas de seguridad. La lección de servidor también aborda seguridad y límites de herramientas. No se añade aquí una implementación concreta de esos controles que no esté presente en los JSON.

## 8. Recorrido conceptual

1. El host contiene el modelo y la conversación.
2. El host utiliza un cliente MCP conectado al servidor pertinente.
3. El cliente descubre capacidades disponibles, por ejemplo con `listTools()`.
4. Para una herramienta, el host solicita consentimiento explícito y muestra la operación y sus argumentos, de acuerdo con la recomendación del curso.
5. El cliente envía la llamada; el servidor ejecuta la herramienta o devuelve el recurso solicitado.
6. El cliente entrega el resultado al host, que puede continuar la interacción del agente.

El curso enfatiza que el protocolo estandariza la integración, pero el uso responsable de las capacidades sigue requiriendo los hábitos de seguridad descritos arriba.

## 9. Referencia a los JSON y límites de captura

- `introduction_to_mcps.json`: definición de MCP, roles, arquitectura, herramientas/recursos/prompts, transportes y uso responsable.
- `building_an_mcp_client.json`: rol del cliente, descubrimiento y llamada de herramientas, consentimiento y cliente TypeScript.
- `building_an_mcp_server.json`: herramientas, recursos y prompts; FastMCP, seguridad y límites.

En los archivos scrapeados, algunas lecciones de evaluación/cierre repiten material anterior; en el curso del servidor también se repite el ejercicio que busca productos por `phone`. Esas repeticiones no se tratan como contenido técnico adicional.
