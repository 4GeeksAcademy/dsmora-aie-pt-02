# Guía docente: Clase 71 - Seguridad de servidores y aplicaciones

Duración base: 70 minutos, adaptable a 60 o 75. Guía autosuficiente para el profesor.

## Fuentes y límites

Las fuentes técnicas son los tres JSON de esta carpeta. Referencias: `[S:N]` = `essential_server_security.json`; `[W:N]` = `owasp_web_application_security_risks.json`; `[L:N]` = `owasp_top_10_for_llm_applications_2026.json`. El número corresponde al campo `index`.

Se extrajeron 34 tarjetas con 31 cuerpos distintos. S:5–6, W:11–12 y L:12–13 son pares de tarjetas con contenido idéntico; no contarlos como prácticas independientes. Las evaluaciones contienen preguntas de repaso. No se extrajeron prompts de OpenClaw. Los comandos de esta guía son únicamente los que aparecen en la unidad de seguridad de servidores; no se atribuyen comandos a los módulos web o LLM. La clase presenta los riesgos y controles incluidos en estas lecciones, no una cobertura completa de todos los riesgos OWASP.

## Continuidad y objetivos

La clase 70 trabajó comunicación en tiempo real y flujos agentivos. Esta sesión cambia el foco desde cómo se conectan esos componentes hacia cómo reducir riesgos en el servidor y en las aplicaciones web y LLM que se construyen.

**Qué decir (literal):** «En la clase anterior nos enfocamos en cómo viajan los mensajes y cómo se coordinan los flujos. Hoy vamos a revisar qué decisiones de acceso, configuración y tratamiento de datos pueden dejar expuesto un servidor o una aplicación».

Al terminar, el estudiante podrá:

- Explicar por qué SSH, cuentas, permisos y puertos son superficies que se deben restringir. [S:0–4]
- Reconocer riesgos web del material, como control de acceso roto, configuración incorrecta, inyección y fallos de autenticación. [W:1–10]
- Distinguir riesgos específicos de aplicaciones LLM: inyección de prompt, exposición de contexto, salida no confiable y agencia excesiva, entre otros. [L:1–11]
- Proponer una revisión defensiva basada en permisos mínimos, validaciones del lado del servidor y controles sobre entradas, salidas y datos sensibles. [S:1–4; W:2–10; L:2–11]

## Preparación y contingencia

- Tener a mano esta guía. Los comandos se recorren como ejemplo de la lección; no aplicarlos a un servidor real durante la sesión.
- Si se muestra la configuración SSH, recalcar primero la advertencia de la fuente: confirmar que la clave funciona en una segunda sesión antes de deshabilitar la autenticación por contraseña. [S:1]
- La extracción no proporciona prompts de OpenClaw ni comandos para auditar una aplicación web o LLM. No improvisarlos como si fueran parte del material.
- Si no hay terminal disponible, recorrer los comandos en pantalla o pizarra y centrar la práctica en clasificar los escenarios de las lecciones.

## Agenda base: 70 minutos

| Minutos | Bloque |
| --- | --- |
| 0–5 | Continuidad: de la arquitectura al control de acceso |
| 5–19 | Endurecimiento básico del servidor |
| 19–37 | Riesgos de aplicaciones web |
| 37–56 | Riesgos de aplicaciones LLM |
| 56–65 | Repaso transversal con escenarios |
| 65–70 | Preguntas de chequeo y cierre |

## 0–5 min: de la arquitectura al control

**Qué decir (literal):** «Un sistema puede transmitir datos correctamente y aun así permitir accesos que no corresponden. Vamos a mirar las decisiones que limitan quién entra, qué puede hacer y qué información puede alcanzar».

La introducción del curso de servidores organiza la revisión en cuatro puertas: acceso SSH, cuentas, permisos de archivos y servicios expuestos a internet. [S:0]

**Pregunta:** «¿Qué cuatro áreas propone revisar el módulo de seguridad del servidor?»

**Respuesta esperada:** cómo se inicia sesión por SSH, qué cuentas se usan, qué archivos y directorios se pueden leer o modificar y qué servicios están expuestos por red. [S:0]

## 5–19 min: reducir la exposición del servidor

**Qué decir (literal):** «El objetivo no es conceder más permisos de los necesarios. La lección combina una forma de acceso controlada, cuentas atribuibles, permisos deliberados y una política de red que solo abre lo necesario».

### SSH y cuentas

La lección recomienda autenticación SSH mediante claves, deshabilitar el acceso directo como root y utilizar una cuenta regular con `sudo` para las tareas administrativas. También advierte verificar la clave en una segunda sesión antes de desactivar las contraseñas, para evitar quedarse sin acceso. Cambiar el puerto puede reducir ruido de escaneos oportunistas, pero la propia lección aclara que no sustituye la autenticación por clave. [S:1–2]

Configuración citada en el material: [S:1]

```text
PasswordAuthentication no
PermitRootLogin no
```

Comandos de la práctica para crear una cuenta y comprobar `sudo`: [S:2]

```bash
sudo adduser alice
sudo usermod -aG sudo alice
su - alice
sudo whoami
```

El resultado esperado del último comando es `root`, después de solicitar la contraseña de `alice`. Explicar que la cuenta de trabajo sigue siendo la cuenta regular y que `sudo` eleva la acción administrativa. [S:2]

### Permisos y firewall

El modelo de permisos separa propietario, grupo y otros, y combina lectura (4), escritura (2) y ejecución (1). `755` permite al propietario leer, escribir y ejecutar; grupo y otros pueden leer y ejecutar. `777` permite esas tres acciones a todos y la lección lo presenta como un riesgo, especialmente para un directorio de cargas. [S:3]

La unidad de firewall propone denegar por defecto las conexiones entrantes y permitir explícitamente los puertos necesarios. Este ejemplo conserva los puertos de la fuente —SSH en `2222`, HTTP en `80` y HTTPS en `443`— y enlaza PostgreSQL a `127.0.0.1` cuando solo necesita acceso local. [S:4]

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

```text
listen_addresses = '127.0.0.1'
```

**Qué preguntar después:** «¿Qué diferencia hay entre denegar por defecto y permitir por defecto? ¿Por qué `777` no es una solución prudente para una carpeta de cargas?»

**Respuesta esperada:** denegar por defecto bloquea conexiones entrantes salvo las permitidas explícitamente; `777` deja que cualquier usuario o proceso escriba, lo que puede convertir una aplicación comprometida en un riesgo mayor. [S:3–4]

## 19–37 min: riesgos de aplicaciones web

**Qué decir (literal):** «En los ejemplos del módulo, muchos fallos no dependen de una técnica exótica: aparecen cuando el servidor confía en un dato del cliente o cuando una configuración deja algo expuesto».

El módulo presenta el OWASP Top 10 como una clasificación construida con datos de aplicaciones reales y encuestas a profesionales. Las lecciones extraídas cubren estos riesgos: [W:1–10]

| Riesgo | Idea que debe quedar clara |
| --- | --- |
| Control de acceso roto | El servidor debe comprobar que el usuario puede acceder al objeto solicitado; cambiar el ID de una factura no debe revelar datos ajenos. [W:2] |
| Configuración incorrecta | Un ajuste permisivo o una credencial predeterminada puede exponer funciones o datos aunque el código esté bien escrito. [W:3] |
| Cadena de suministro e integridad | Dependencias, registros de paquetes, pipelines e imágenes base también forman parte de lo que se debe revisar. [W:4] |
| Fallos criptográficos | Proteger datos sensibles en tránsito y en reposo; no almacenar datos que no sea necesario conservar. [W:5] |
| Inyección | Ocurre cuando una entrada no confiable es interpretada como instrucciones por un intérprete. [W:6] |
| Diseño inseguro | La debilidad nace de una especificación o arquitectura defectuosa y no se resuelve solo corrigiendo una línea de código. [W:7] |
| Fallos de autenticación | Credenciales débiles o filtradas y una gestión deficiente de sesiones pueden facilitar el acceso no autorizado. [W:8] |
| Registro y alertas insuficientes | Sin eventos útiles ni alertas, una brecha puede pasar inadvertida. [W:9] |
| Manejo incorrecto de excepciones | Los errores y condiciones límite pueden filtrar información o dejar el sistema en un estado inseguro. [W:10] |

### Escenario de repaso

El cuestionario describe un endpoint `/api/invoices/1043` que devuelve una factura a cualquier usuario autenticado que cambie el número. Pida identificar la categoría y la comprobación que falta: es control de acceso roto; el servidor no verificó la propiedad de la factura para esa solicitud. [W:11]

**Qué preguntar después:** «¿Dónde debe ocurrir la comprobación de propiedad: solo en la interfaz o también en el servidor?»

**Respuesta esperada:** en el servidor; el material señala que confiar en el identificador enviado por el cliente deja el acceso sin verificar. [W:2,11]

## 37–56 min: riesgos de aplicaciones LLM

**Qué decir (literal):** «En una aplicación con LLM no basta con proteger la entrada del usuario. También hay que decidir qué contexto recibe el modelo, qué herramientas puede usar y cómo se manejan sus respuestas».

La introducción explica que instrucciones y datos llegan al modelo como un flujo de tokens sin una separación de confianza que el modelo pueda hacer cumplir de forma fiable. Por eso el módulo presenta riesgos tanto en la entrada como en el contexto, la salida y las acciones automatizadas. [L:0–2]

Recorrer los riesgos cubiertos, agrupándolos para mantener el ritmo: [L:2–11]

- **Entrada y contexto:** inyección de prompt; divulgación de información sensible; exposición de contexto oculto, como instrucciones o esquemas que el usuario no ve. [L:2–4]
- **Respuesta y confianza:** manejo inadecuado de salida cuando el texto del modelo llega a un destino sensible; desinformación cuando una respuesta incorrecta se acepta y desencadena decisiones o acciones. [L:5–6]
- **Acciones y recursos:** agencia excesiva por funcionalidad, permisos o autonomía de más; consumo ilimitado por solicitudes que disparan uso de recursos sin control. [L:7–8]
- **Componentes y datos:** cadena de suministro de modelos, adaptadores, conjuntos de datos y servicios; envenenamiento de datos/modelos; debilidades de vectores y embeddings, incluidas posibles fugas entre inquilinos. [L:9–11]

**Qué decir (literal):** «La revisión no termina en el prompt. Preguntemos también qué datos se recuperan, qué permisos tiene la herramienta y qué ocurre si la respuesta del modelo es incorrecta».

### Preguntas de clasificación

1. «Un documento recuperado contiene instrucciones ocultas que intentan cambiar el comportamiento del asistente: ¿qué riesgo del módulo debemos considerar?» Inyección indirecta de prompt. [L:2,12]
2. «La respuesta del modelo se inserta directamente en una parte sensible de la aplicación: ¿qué tratamiento recomienda el tema de salida?» Tratar la salida como entrada no confiable y no dejarla llegar sin control al destino. [L:5]
3. «Una herramienta de lectura también puede borrar archivos: ¿qué dimensión de agencia excesiva aparece?» Funcionalidad excesiva. [L:7]

## 56–65 min: repaso transversal

Pida que clasifiquen cada situación y expliquen el principio de control que falta:

- El directorio de cargas permite escritura a todos: permisos demasiado amplios. [S:3]
- Un usuario cambia el identificador de una factura y obtiene datos de otra persona: control de acceso roto. [W:2]
- Un sistema acepta como confiable cualquier salida del LLM y la usa en una operación sensible: manejo inadecuado de salida. [L:5]

**Qué decir (literal):** «En los tres casos, el control falla en un límite distinto: permisos del sistema, autorización de la solicitud y tratamiento de la salida generada».

## 65–70 min: cierre

Preguntas de chequeo:

- ¿Qué comprobarías antes de deshabilitar el acceso SSH por contraseña? [S:1]
- ¿Qué valida el servidor cuando recibe el ID de un recurso? [W:2]
- ¿Por qué el contexto oculto no debe contener secretos que necesiten permanecer confidenciales? [L:4]
- ¿Qué diferencia hay entre agencia excesiva y consumo ilimitado? [L:7–8]

**Cierre sugerido (literal):** «La seguridad se revisa en capas: acceso al servidor, permisos y red; autorización y configuración de la aplicación; y límites sobre contexto, salida y acciones del LLM. Para cada riesgo, debemos poder señalar qué control lo contiene».

## Ajustes de duración

- **Versión de 60 minutos:** reducir el bloque de servidor a SSH y firewall; recorrer la tabla web sin detenerse en cada categoría; conservar el bloque de riesgos LLM y el repaso final.
- **Versión de 75 minutos:** añadir cinco minutos para que el grupo justifique qué información o permiso debe limitarse en cada escenario, sin introducir herramientas o comandos que no estén en el material.

## Límites de demostración

No hay un ejemplo de implementación de una aplicación ni prompts de OpenClaw en estos JSON. Los comandos y fragmentos de configuración de esta guía proceden de [S:1–4]. Los escenarios y preguntas se usan para clasificar y explicar los riesgos descritos; no son instrucciones para explotar sistemas.