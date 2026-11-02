# Dossier ampliado para NotebookLM: seguridad de servidores, aplicaciones web y aplicaciones LLM

## Alcance y procedencia

Este documento organiza las tres extracciones LearnPack de `class_71`. Las únicas fuentes técnicas son los JSON indicados en la tabla. Las referencias `[S:N]`, `[W:N]` y `[L:N]` apuntan al campo `index` de cada JSON.

| Código | JSON | Tarjetas extraídas | Cuerpos distintos |
| --- | --- | ---: | ---: |
| S | `essential_server_security.json` | 7 | 6 |
| W | `owasp_web_application_security_risks.json` | 13 | 12 |
| L | `owasp_top_10_for_llm_applications_2026.json` | 14 | 13 |

En total hay 34 tarjetas y 31 cuerpos distintos. La comparación se hizo sobre el campo `content`, no sobre los títulos:

- S:5–6 repiten el mismo cuestionario de evaluación. [S:5–6]
- W:11–12 repiten el mismo cuestionario de evaluación. [W:11–12]
- L:12–13 repiten el mismo cuestionario de evaluación. [L:12–13]

Las tarjetas repetidas no se presentan como lecciones o evaluaciones independientes. Las extracciones cubren las categorías enumeradas en este dossier, no todo el catálogo posible de seguridad de servidores, OWASP web u OWASP para LLM. No se extrajeron prompts de OpenClaw; los únicos comandos concretos aparecen en el módulo de servidores.

## Continuidad con la clase anterior

Como continuidad curricular de `class_70`, el foco pasa de la comunicación en tiempo real y los flujos agentivos a los límites de acceso, configuración y confianza que deben proteger los componentes de una aplicación. Las afirmaciones técnicas de las siguientes secciones proceden exclusivamente de los JSON de `class_71`.

## 1. Seguridad esencial del servidor

La unidad organiza el endurecimiento alrededor de cuatro áreas: cómo se inicia sesión, qué cuentas se usan, qué permisos tienen los archivos y qué servicios se exponen a internet. [S:0]

### 1.1 SSH y cuentas

El módulo recomienda autenticación SSH mediante claves y desactivar los inicios de sesión por contraseña con `PasswordAuthentication no`. También recomienda impedir el acceso SSH directo como root con `PermitRootLogin no`, usar una cuenta regular y ejecutar tareas administrativas con `sudo`. Antes de deshabilitar contraseñas, indica comprobar la clave abriendo una segunda sesión para evitar perder el acceso. Cambiar el puerto SSH aparece como una opción para reducir ruido de escaneos oportunistas, no como sustituto de la autenticación por clave. [S:1–2]

```text
PasswordAuthentication no
PermitRootLogin no
```

La práctica ilustra la creación de una cuenta y la verificación de privilegios: [S:2]

```bash
sudo adduser alice
sudo usermod -aG sudo alice
su - alice
sudo whoami
```

El resultado esperado de `sudo whoami` es `root`, tras solicitar la contraseña de `alice`. La cuenta diaria sigue siendo la cuenta regular; `sudo` se usa para la operación que requiere privilegios administrativos. [S:2]

### 1.2 Permisos

Cada archivo y directorio distingue propietario, grupo y otros; cada clase puede tener lectura, escritura y ejecución. La fuente describe el valor numérico como suma de lectura `4`, escritura `2` y ejecución `1`. Así, `755` da todos esos permisos al propietario y lectura/ejecución al grupo y a otros. `777` permite leer, escribir y ejecutar a todos; el curso lo marca como peligroso, particularmente en directorios donde una aplicación puede escribir archivos. [S:3]

### 1.3 Firewall y servicios locales

La estrategia propuesta es denegar por defecto las conexiones entrantes, permitir expresamente los puertos necesarios y habilitar el firewall. El ejemplo usa SSH en `2222/tcp`, HTTP en `80/tcp` y HTTPS en `443/tcp`. La lección también propone enlazar servicios que solo requieren acceso local a `127.0.0.1`; para PostgreSQL muestra `listen_addresses = '127.0.0.1'`. [S:4]

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

## 2. Riesgos de aplicaciones web

La lección introductoria presenta el OWASP Top 10 como una clasificación basada en datos de aplicaciones reales y encuestas a profesionales. La extracción cubre los siguientes temas: [W:0–10]

| Referencia | Riesgo y punto central |
| --- | --- |
| [W:2] | **Control de acceso roto:** el servidor no comprueba que la persona solicitante sea propietaria del recurso. El ejemplo es un endpoint de facturas cuyo ID puede cambiarse. |
| [W:3] | **Configuración incorrecta:** un ajuste permisivo o credenciales por defecto pueden exponer datos o funciones. |
| [W:4] | **Cadena de suministro e integridad:** dependencias, registros de paquetes, pipelines de construcción e imágenes base forman parte de la superficie de confianza. |
| [W:5] | **Fallos criptográficos:** proteger datos sensibles en tránsito y en reposo; no conservar datos innecesarios. |
| [W:6] | **Inyección:** datos no confiables llegan a un intérprete y se tratan como instrucciones. La lección nombra SQL, comandos y XSS. |
| [W:7] | **Diseño inseguro:** el problema nace de la especificación o arquitectura y requiere replantear el diseño, no solo corregir código. |
| [W:8] | **Fallos de autenticación:** credenciales filtradas o débiles, intentos ilimitados y gestión de sesiones deficiente. |
| [W:9] | **Registro y alertas insuficientes:** una detección tardía aumenta el tiempo durante el que una brecha puede pasar inadvertida. |
| [W:10] | **Manejo incorrecto de excepciones:** errores, tiempos de espera, falta de recursos o entradas malformadas pueden dejar al sistema en un estado inseguro o revelar información. |

El cuestionario vuelve sobre el caso de la factura y señala que la comprobación de propiedad debe realizarse del lado del servidor. [W:11–12]

## 3. Riesgos del OWASP Top 10 para aplicaciones LLM

La introducción destaca que el modelo recibe instrucciones y datos como un flujo de tokens y no puede separar de forma fiable ambos tipos de contenido. Las lecciones cubren riesgos en entradas, contexto, respuestas, acciones y componentes: [L:0–11]

### Entrada y contexto

- **Inyección de prompt:** una entrada no confiable puede manipular el comportamiento previsto. La unidad señala que los LLM no tienen un equivalente directo a las consultas parametrizadas para imponer una frontera de confianza entre instrucciones y datos. [L:2]
- **Divulgación de información sensible:** la exposición puede ocurrir en respuestas, argumentos de herramientas y otros canales; incluye datos personales, registros, credenciales, claves API y secretos propietarios. [L:3]
- **Exposición de contexto oculto:** prompts del sistema, esquemas de herramientas, instrucciones y políticas recuperadas pueden ser revelados; la lección recomienda diseñar asumiendo que ese contexto podría hacerse público. [L:4]

### Respuesta y confianza

- **Manejo inadecuado de salida:** la salida del modelo debe tratarse como entrada no confiable antes de llegar a destinos sensibles como páginas, consultas o comandos. [L:5]
- **Desinformación:** una respuesta incorrecta o no respaldada se vuelve un riesgo cuando se acepta y se utiliza para decisiones o acciones automatizadas. [L:6]

### Acciones, recursos y cadena de suministro

- **Agencia excesiva:** el sistema puede tener demasiada funcionalidad, permisos o autonomía. [L:7]
- **Consumo ilimitado:** solicitudes de bajo costo pueden provocar consumo de inferencia o recursos desproporcionado; la lección incluye facturas elevadas, bucles de razonamiento y crecimiento del contexto. [L:8]
- **Cadena de suministro:** además de paquetes, comprende modelos, adaptadores, conjuntos de datos y servicios de conversión. [L:9]
- **Envenenamiento de datos y modelos:** datos o artefactos manipulados pueden introducir patrones, sesgos o comportamientos dañinos durante preentrenamiento, ajuste fino, ingesta para RAG o reutilización de modelos. [L:10]
- **Debilidades de vectores y embeddings:** la búsqueda por similitud define qué datos puede recuperar el modelo; una separación insuficiente puede causar fugas entre inquilinos o manipulación. [L:11]

## 4. Síntesis

Los tres módulos permiten revisar límites distintos:

1. **Sistema y red:** restringir inicio de sesión, privilegios, permisos de archivos y puertos. [S:1–4]
2. **Aplicación web:** verificar autorización en el servidor, tratar las entradas según su origen, proteger datos y revisar la configuración, dependencias, errores y registros. [W:2–10]
3. **Aplicación LLM:** considerar no confiables las entradas y salidas, limitar contexto y capacidades, proteger datos y controlar componentes y consumo. [L:2–11]

La extracción no incluye una aplicación de ejemplo completa, un laboratorio paso a paso para OWASP web/LLM ni prompts de OpenClaw. Los comandos anteriores se limitan a ejemplos capturados en el JSON de servidores; no se deben presentar como guía de cambios para un servidor productivo sin verificar su configuración real.