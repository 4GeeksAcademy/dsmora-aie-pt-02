# Clase 63 — MCP: protocolo, clientes y servidores

## Datos de la sesión

**Tema:** Model Context Protocol (MCP): comprender el protocolo y construir conceptualmente clientes y servidores.
**Duración sugerida:** 75 minutos (adaptable a 60).
**Material base:** `introduction_to_mcps.json`, `building_an_mcp_client.json` y `building_an_mcp_server.json`.

## Propósito

Comprender cómo MCP proporciona un protocolo común para la comunicación entre hosts y servidores, y distinguir host, cliente MCP y servidor MCP. Aplicar esa distinción a herramientas, recursos y prompts, junto con las recomendaciones de seguridad descritas en los cursos.

## Resultados de aprendizaje

Al finalizar la clase, el estudiante podrá:

1. Explicar el problema de integrar cada aplicación con cada herramienta mediante conexiones particulares y la propuesta de un protocolo común.
2. Dibujar el flujo `host ↔ cliente MCP ↔ servidor MCP` y describir qué hace cada componente.
3. Distinguir herramientas (acciones), recursos (datos) y prompts (instrucciones reutilizables).
4. Describir el descubrimiento de herramientas, la aprobación de una llamada y el retorno de su resultado.
5. Reconocer los ejemplos TypeScript con `Client`/`StdioClientTransport` y Python con FastMCP.
6. Identificar las recomendaciones de seguridad descritas: consentimiento explícito, mínimo privilegio, cautela con servidores desconocidos y validación de entradas de herramientas.

## Agenda

| Tiempo | Actividad |
|---|---|
| 0–7 min | Motivación: integraciones y protocolo común |
| 7–20 min | Roles: host, cliente y servidor |
| 20–31 min | Herramientas, recursos y prompts |
| 31–44 min | Descubrimiento, consentimiento y llamada desde el cliente |
| 44–58 min | Declarar capacidades con FastMCP |
| 58–68 min | Seguridad y límites |
| 68–75 min | Repaso y evaluación oral |

## Ideas esenciales

- **MCP** se presenta en el curso como un protocolo común que facilita que agentes compatibles utilicen servidores compatibles sin código personalizado para cada integración. El curso lo describe como complementario a las llamadas a funciones, no como reemplazo.
- **Host:** aplicación con la que interactúa el usuario; contiene el agente/modelo y la conversación y gestiona la experiencia del usuario.
- **Cliente MCP:** conector dentro del host que habla el protocolo y conecta el host con exactamente un servidor. Un host que necesita varios servidores suele tener varios clientes.
- **Servidor MCP:** programa externo que expone herramientas, recursos y prompts. El cliente se conecta y descubre las capacidades anunciadas.
- **Tool:** acción ejecutable, como crear un ticket o sumar dos valores.
- **Resource:** información que se ofrece para lectura como contexto.
- **Prompt:** plantilla/instrucción reutilizable.
- **Consentimiento y uso responsable:** los cursos recomiendan consentimiento explícito antes de usar herramientas, mínimo privilegio y cautela con servidores desconocidos. La introducción dice que el host siempre debe pedir consentimiento explícito y mostrar operación y parámetros.
- **Transportes:** la unidad de introducción presenta stdio como local, proceso hijo del host, comunicación por stdin/stdout, una única conexión de cliente y sin autenticación porque no hay red. HTTP Streamable se describe como remoto y multi-cliente, con autenticación y autorización requeridas. La fuente aclara que local/remoto es el caso común, no una regla estricta: HTTP Streamable también puede usarse con un servidor en la misma máquina. La unidad de uso responsable dice que stdio aún requiere diálogo de consentimiento explícito, pues opera con los privilegios de la máquina.
- **Seguridad:** el material recomienda consentimiento explícito, mínimo privilegio y cautela con servidores desconocidos; las herramientas requieren validación estricta de entradas y medidas de seguridad. La fuente no dice que el protocolo sustituya esos hábitos.

## Ejemplos de los cursos

Cliente TypeScript: el curso muestra la creación de un `Client`, un `StdioClientTransport`, la conexión, el descubrimiento con `listTools()`, la llamada con `callTool()` y el cierre con `close()`. Servidor Python FastMCP: el tutorial indica instalar con `uv add fastmcp`, inicializar `FastMCP("Mi Servidor")` y declarar una herramienta con `@mcp.tool`, por ejemplo `add(a: int, b: int) -> int`. También se muestran `@mcp.resource` y `@mcp.prompt`; el ejemplo FastMCP utiliza stdio por defecto.

Estos fragmentos ilustran APIs y patrones; no forman por sí solos un proyecto integrado entre los tres cursos.

## Preguntas para comprobar comprensión

1. ¿Qué componente inicia la conexión MCP? — El cliente.
2. ¿Qué diferencia una herramienta de un recurso? — La herramienta ejecuta una acción; el recurso expone datos.
3. ¿MCP es un modelo? — No, es un protocolo.
4. ¿Qué debe mostrar el host para pedir consentimiento explícito? — La operación exacta y sus parámetros.
5. ¿Qué hábitos de seguridad enumera la introducción? — Consentimiento explícito, mínimo privilegio y desconfianza hacia servidores desconocidos.

## Recursos de clase

- `resume_01.md`: lectura de estudio de los tres cursos.
- `resume_02.md`: guía docente con secuencia, actividades y evaluación.
- Los tres JSON de tutoriales scrapeados sirven como trazabilidad del material original.

> Nota de scraping: algunas unidades de evaluación y cierre repiten texto previo. Se consideran duplicados, no contenido nuevo.