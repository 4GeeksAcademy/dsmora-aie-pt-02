# Guía docente ampliada: Class 28 - Arquitectura backend, organización Python, FastAPI y entornos virtuales

Este documento está pensado para el profesor. No es un resumen para alumnos, sino un soporte para explicar con propiedad, responder dudas y manejar la clase con más seguridad.

## 1) Objetivo pedagógico de la clase

La clase busca que el profesor ayude al grupo a entender que la arquitectura no es un detalle estético, sino una decisión que influye en:

- claridad del código
- facilidad para cambiar cosas luego
- capacidad de trabajar en equipo
- calidad de los tests
- coste de mantenimiento

El objetivo no es que el alumnado memorice nombres, sino que pueda empezar a tomar decisiones con criterio cuando vea un proyecto real.

## 2) Instrucción para el profesor: debate de arquitectura backend

### 2.1 Propósito de la actividad

La actividad debe ayudar a que cada estudiante defienda una propuesta concreta de arquitectura para el proyecto transversal, no solo repita conceptos teóricos. La idea es que el debate se centre en decisiones reales: qué carpetas crear, qué módulos separar, qué patrón elegir y por qué eso ayuda al proyecto.

### 2.2 Duración recomendada

- Debate y reflexión guiada: 45–60 minutos
- Si el tiempo es ajustado, se puede reducir a 40 minutos manteniendo el núcleo: arquitectura, estructura modular, FastAPI y entorno reproducible

### 2.3 Ritmo recomendado

1. Apertura (5 min)
2. Aprender (10 min)
3. Reflexionar (10 min)
4. Tener en cuenta (8 min)
5. Hacer (8 min)
6. Evitar (8 min)
7. Cierre (5 min)

### 2.4 Puntos imprescindibles que debe cubrir el profesor

- Trade-offs entre MVC y arquitectura en capas para el proyecto transversal
- Reglas básicas de imports en Python y riesgo de dependencias circulares
- Por qué FastAPI aporta valor frente a montar HTTP de forma manual
- Flujo con `uv` para entornos reproducibles y trabajo en equipo
- Priorizar razones de negocio sobre términos de moda

### 2.5 Criterios de participación

- Aporta un ejemplo concreto que conecte un tema teórico con el contexto del proyecto transversal
- Cuestiona o amplía el trade-off de arquitectura de otro con un “por qué”, no solo con acuerdo
- Formula o responde al menos una pregunta sobre estructura Python, elementos FastAPI o gestión de entornos

### 2.6 Debate orientado a la práctica

#### Apertura — impacto profesional

- Cuando un prototipo empieza a crecer, ¿qué decisión de arquitectura del día uno genera más rework meses después y por qué?

#### Aprender

- Patrones backend comunes: MVC, capas y serverless
- Límites de organización Python: PEP8, imports absolutos y relativos, uso de `__init__.py`
- Piezas de FastAPI: `app`, endpoints, `APIRouter` y modelos de datos

#### Reflexionar

- ¿Dónde está la línea entre “estructura suficiente” y sobre-diseño prematuro?
- ¿Cómo detectar que el layout de carpetas sirve para hoy pero bloquea mañana?

#### Tener en cuenta

- Disciplina de imports y prevención de dependencias circulares
- Entornos reproducibles con `uv`
- Elegir patrones por necesidad de negocio, no por moda técnica

#### Hacer

- Proponer un layout backend para el transversal
- Mapear dominios a carpetas o módulos
- Definir endpoints y routers antes de codificar comportamiento
- Instalar FastAPI en un entorno con `uv`

#### Evitar

- Sobrediseño antes de tener requisitos claros
- Saltarse el entorno virtual
- Ignorar higiene de imports o circular imports
- Elegir una arquitectura “bonita” sin justificación de negocio

### 2.7 Checkpoint de la clase

Cada estudiante debe defender un layout de carpetas o módulos y una decisión de arquitectura con una razón de negocio concreta. El objetivo es que el resultado no sea solo una propuesta visual, sino una decisión discutible, ejecutable y alineada con el proyecto transversal.

### 2.8 Ejemplo breve de layout de carpetas para mostrar en clase

Un ejemplo simple y útil para ilustrar la idea es este:

```text
backend/
  app/
    main.py
    api/
      routers.py
    services/
      user_service.py
    repositories/
      user_repository.py
    models/
      user.py
    core/
      exceptions.py
```

La idea no es que este árbol sea “perfecto”, sino que permita mostrar de forma concreta qué se separa y por qué. El profesor puede decir:

- `routers` recibe la petición
- `services` contiene la lógica de negocio
- `repositories` encapsula el acceso a datos
- `models` representa entidades o contratos

### 2.9 Mini caso de refactorización para ilustrar el problema

Un caso muy útil es mostrar un endpoint que mezcla todo a la vez:

```python
@app.post("/users")
def create_user(payload: dict):
    if "email" not in payload:
        return {"error": "email required"}, 400

    # lógica de negocio inline
    if "@" not in payload["email"]:
        return {"error": "invalid email"}, 400

    # acceso a datos inline
    db.append(payload)
    return {"ok": True}, 201
```

Luego el profesor puede pedir una mejora sencilla: mover la validación a un servicio y el acceso a datos a un repositorio. Eso permite explicar que el problema no es el código que “funciona”, sino que el código mezcla responsabilidades y se vuelve frágil.

### 2.10 Pregunta final de cierre

Una pregunta de cierre muy útil es:

- “¿Cómo ayudará tu propuesta de arquitectura a que compañeros humanos y agentes de código produzcan FastAPI consistente en el transversal, y no solo se vea bien en una slide?”

Esta pregunta conecta arquitectura con trabajo en equipo, mantenibilidad y colaboración real.

### 2.11 Rúbrica mínima de evaluación

Para distinguir una propuesta superficial de una madura, el profesor puede evaluar con estos criterios:

- Claridad de responsabilidades: separa bien rutas, lógica y datos
- Justificación de negocio: la arquitectura responde a una necesidad concreta del proyecto
- Viabilidad práctica: la propuesta es ejecutable y no solo teórica
- Compatibilidad con FastAPI: el layout encaja con routers, modelos y servicios
- Reproducibilidad: contempla entorno virtual y dependencias claras

## 3) Qué debe quedar claro al final de la clase

Al terminar, el profesor debería poder dejar estas ideas asimiladas:

- La arquitectura ayuda a organizar responsabilidades.
- No existe una arquitectura “mejor” en absoluto; existe una arquitectura más adecuada según el contexto.
- MVC, capas, hexagonal y serverless no son incompatibles: son formas distintas de pensar la separación.
- Un proyecto pequeño puede empezar simple y luego crecer sin volverse un caos.
- FastAPI facilita exponer una API, pero la arquitectura sigue siendo lo que hace que el proyecto sea sostenible.
- Un entorno virtual y un flujo reproducible son parte de la calidad profesional del desarrollo.

## 3) Cómo explicar la arquitectura sin que suene abstracto

La mejor forma de explicarlo es convertirlo en una historia sencilla y visual.

### Historia base para el profesor

“Imagina que estás coordinando un restaurante. Si todo el mundo hace todo en la misma cocina, el servicio se complica. Si el cocinero prepara, el camarero sirve y el encargado gestiona el stock, todo fluye mejor. En software pasa lo mismo: si una ruta HTTP hace validación, lógica de negocio, acceso a base de datos y formato de respuesta, el sistema se vuelve difícil de mantener.”

### Regla de oro para enseñar esto

No se enseña arquitectura como teoría pura. Se enseña como respuesta a un problema concreto:

- “¿Qué pasa cuando el proyecto empieza a crecer?”
- “¿Qué pasa si cambiamos de base de datos?”
- “¿Qué pasa si el equipo se amplía?”
- “¿Qué pasa si un endpoint se llena de lógica?”

## 4) Comparación clara entre arquitecturas

La clave es mostrar que estas arquitecturas no son un ranking, sino diferentes maneras de separar responsabilidades.

### Tabla comparativa rápida

| Arquitectura | Idea central | Lo que resuelve | Ventaja principal | Debilidad habitual | Cuándo usarla |
|---|---|---|---|---|---|
| Monolítica | Todo en una aplicación unificada | Simplifica el arranque | Muy sencilla de empezar | Crece difícilmente si no se organiza | Proyectos pequeños o MVP |
| MVC | Modelo, Vista, Controlador | Separa la interacción de la lógica y los datos | Muy intuitiva | Puede volverse confusa en apps grandes | Apps web tradicionales o proyectos sencillos |
| Capas | Presentación, negocio, datos | Separa por niveles de responsabilidad | Muy clara para equipos | Puede volverse rígida si se sobre-abstracta | Proyectos medianos con reglas de negocio claras |
| Hexagonal | Núcleo de negocio aislado, puertos y adaptadores | Aísla la lógica de tecnologías externas | Muy robusta frente a cambios | Requiere más disciplina conceptual | Sistemas que cambian de base de datos, APIs o frameworks |
| Microservicios | Varias piezas independientes que se comunican | Escala por dominio | Permite despliegues y equipos separados | Más complejidad operativa | Sistemas grandes, equipos grandes, alto crecimiento |
| Serverless | Funciones ejecutadas por eventos | Reduce la gestión de infraestructura | Muy rápida para ciertos escenarios | Dependencia del proveedor y sobrecarga de integración | APIs/eventos/automatizaciones con carga variable |

## 5) Cómo contar cada una de ellas en clase

### 5.1 Monolítica

Explicación breve para el profesor:

“La arquitectura monolítica es la forma más simple: una sola unidad de software donde todo vive junto. Es muy útil al principio, porque permite avanzar rápido. El problema aparece cuando el sistema crece y todas las partes empiezan a depender unas de otras.”

Puntos clave:

- Fácil de arrancar
- Ideal para MVP
- Riesgo de acoplamiento cuando crece

Ejemplo mental:

“Una app que tiene usuarios, pagos, reportes y administración en un mismo bloque. Funciona, pero cada cambio puede afectar a varias áreas.”

### 5.2 MVC

Explicación breve:

“MVC divide la app en tres piezas: el Modelo (datos y lógica), la Vista (cómo se muestra) y el Controlador (la coordinación). Es una forma muy natural de pensar la separación.”

Puntos clave:

- Muy visual
- Útil para entender el flujo de una petición
- Menos potente para separar lógica compleja que el enfoque en capas o hexagonal

Ejemplo mental:

“Una petición entra al controlador, el controlador pide datos al modelo y luego la vista prepara la respuesta.”

### 5.3 Arquitectura en capas

Explicación breve:

“En capas, la aplicación se organiza por niveles. La capa de presentación recibe la petición; la de negocio decide qué hacer; la de datos accede a la persistencia.”

Puntos clave:

- Muy buena para equipos que necesitan claridad
- Facilita tests y cambios parciales
- Ayuda a evitar mezclar todo en un solo sitio

Ejemplo mental:

“Una ruta HTTP no debería hablar directamente con la base de datos. Debería pasar por una capa de negocio.”

### 5.4 Arquitectura hexagonal

Explicación breve:

“La arquitectura hexagonal se centra en el núcleo de negocio y deja fuera las tecnologías externas. El negocio no depende de una base de datos concreta ni de un framework concreto.”

Puntos clave:

- Aísla la lógica de negocio
- Permite cambiar infraestructura sin reescribir todo
- Muy útil cuando se anticipa cambio

Ejemplo mental:

“Si hoy guardamos usuarios en PostgreSQL y mañana queremos moverlos a MongoDB, el núcleo de negocio no debería cambiar.”

### 5.5 Microservicios

Explicación breve:

“Microservicios dividen el sistema en servicios autónomos. Cada servicio tiene responsabilidad propia y puede desplegarse por separado.”

Puntos clave:

- Escalabilidad por dominio
- Equipos separados
- Mayor complejidad operativa

Ejemplo mental:

“Una tienda online con un servicio de usuarios, otro de pagos y otro de inventario.”

### 5.6 Serverless

Explicación breve:

“Serverless no significa que no haya servidores; significa que no los gestionas tú directamente. El proveedor ejecuta funciones cuando ocurre un evento.”

Puntos clave:

- Muy útil para eventos y cargas variables
- Menos cuidado de infraestructura
- Puede introducir complejidad de integración y dependencia del proveedor

Ejemplo mental:

“Una función que se dispara cuando llega un archivo o cuando un usuario crea una cuenta.”

## 6) Ejemplo práctico con sistema de ficheros

Esto es lo que más ayuda a que el alumnado visualice la diferencia.

### Ejemplo base: una app de usuarios

Supongamos que queremos crear una API para gestionar usuarios.

### Versión simple y confusa

```text
project/
  app.py
```

En este caso, todo está mezclado:

- validación
- lógica de negocio
- acceso a datos
- respuestas HTTP

Esto es difícil de mantener.

### Versión MVC

```text
project/
  controllers/
    user_controller.py
  models/
    user_model.py
  views/
    user_view.py
  main.py
```

Aquí el flujo es más claro:

- el controlador recibe la petición
- el modelo procesa la información
- la vista prepara la respuesta

### Versión en capas

```text
project/
  presentation/
    user_routes.py
  business/
    user_service.py
  data/
    user_repository.py
  domain/
    user.py
```

Aquí el mensaje clave es:

- la ruta no accede directamente a los datos
- el servicio contiene la lógica
- el repositorio encapsula el acceso a la persistencia

### Versión hexagonal

```text
project/
  core/
    user_service.py
    user.py
  ports/
    user_repository.py
  adapters/
    postgres_user_repository.py
    in_memory_user_repository.py
  interfaces/
    api.py
```

Aquí el mensaje clave es:

- el negocio vive en el núcleo
- los adaptadores se encargan de las tecnologías externas
- si cambias de PostgreSQL a Mongo, el core no tiene que cambiar

### Frase para este ejemplo

“Las carpetas no hacen arquitectura por sí mismas; lo que importa es el límite entre responsabilidades. La estructura de ficheros debe reflejar ese límite.”

## 7) Cómo mostrarlo y contarlo en clase

### Método recomendado para el profesor

No intentes explicar todas las arquitecturas como si fueran alternativas absolutas. Mejor hazlo así:

1. Presenta un problema real: “una ruta hace demasiadas cosas”
2. Muestra cómo se ve el problema en un archivo único
3. Muéstralo en una estructura de carpetas
4. Compara el enfoque con MVC, capas y hexagonal
5. Conecta cada uno con una ventaja concreta

### Estructura de narración ideal

- “Primero vemos el problema.”
- “Luego vemos cómo se organiza el código.”
- “Después entendemos por qué esa organización ayuda.”
- “Por último, vemos cuándo conviene cada patrón.”

### Frases útiles para decir en clase

- “La arquitectura no es decoración, es una forma de evitar caos.”
- “Si una ruta hace validación, negocio y base de datos, el sistema está mezclado.”
- “El objetivo no es escribir más código, sino escribirlo en el sitio correcto.”
- “Una buena arquitectura no elimina la complejidad; la hace visible y manejable.”

## 8) Guion de clase pensado para 75 minutos

### 0–8 min: apertura y contexto

- Presentar el problema: “¿por qué importa cómo se organiza un backend?”
- Enunciar que la arquitectura ayuda a sostener el crecimiento del proyecto
- Relacionarlo con la idea de mantenimiento y equipo

### 8–22 min: arquitectura backend

- Explicar monolítica, MVC, capas y hexagonal
- Hacer una comparación rápida y visible
- Mostrar las diferencias en términos de separación y cambio futuro

### 22–38 min: separación de responsabilidades

- Mostrar un ejemplo de código mezclado
- Mostrar cómo se reorganiza por carpetas y módulos
- Explicar por qué la separación mejora el mantenimiento

### 38–60 min: FastAPI como ejemplo concreto

- Crear un app mínima con un endpoint de salud
- Añadir un endpoint con parámetros
- Añadir un modelo Pydantic para validar datos
- Relacionar esto con la idea de que la API es una frontera, no el centro del negocio

### 60–72 min: entornos virtuales y flujo profesional

- Mostrar por qué el entorno virtual importa
- Explicar `uv`, `pyproject.toml`, `uv.lock` y `.venv`
- Enfatizar que el entorno reproducible es parte de la calidad profesional

### 72–75 min: cierre

- Hacer 2 o 3 preguntas de reflexión
- Resumir: “no se trata de memorizar, sino de pensar en límites claros”

## 9) Preguntas de reflexión para el profesor

Estas preguntas ayudan a que la clase no se quede en definiciones vacías:

- “Si una ruta empieza a hacer de todo, ¿qué problema aparece?”
- “¿Qué pasa si cambiamos de base de datos?”
- “¿Qué ventaja tiene separar lógica de negocio de la API?”
- “¿Por qué un entorno virtual no es opcional en un proyecto serio?”

## 10) Dudas comunes y respuestas breves

### “¿MVC y capas son lo mismo?”
No. MVC es un patrón de organización alrededor de interacción, mientras que capas es una organización por niveles de responsabilidad.

### “¿Hexagonal es demasiado compleja para empezar?”
No siempre. Para un proyecto pequeño puede parecer excesiva, pero su valor aparece cuando el sistema necesita flexibilidad.

### “¿Serverless es mejor que las otras?”
No. Es una opción concreta para ciertos problemas, especialmente eventos y cargas variables.

### “¿Por qué no meterlo todo en una sola carpeta?”
Porque el acoplamiento crece y cada cambio rompe más cosas.

### “¿La arquitectura cambia el código o solo la organización?”
Cambia ambas cosas. La organización del código y la manera de pensar el sistema.

## 11) Prompts útiles para IA durante la clase

### Prompt 1: comparar arquitecturas

```text
Actúa como arquitecto backend senior y explica en español, de forma breve y clara, cuándo conviene usar monolítica, MVC, arquitectura en capas, arquitectura hexagonal, microservicios y serverless. Incluye una ventaja y un riesgo de cada una.
```

### Prompt 2: refactorizar una ruta mezclada

```text
Tengo una API en FastAPI donde una ruta mezcla validación, lógica de negocio y acceso a datos. Propón una refactorización paso a paso con una estructura de carpetas clara.
```

### Prompt 3: mostrar estructura de proyecto

```text
Genera un ejemplo de proyecto Python con FastAPI usando carpetas para routes, services, repositories y domain. El objetivo es mostrar separación de responsabilidades.
```

### Prompt 4: explicación de entornos virtuales

```text
Explícame en español por qué un entorno virtual es importante, qué diferencia hay entre pyproject.toml, uv.lock y .venv, y cómo explicarlo a un grupo inicial.
```

## 12) Cierre recomendado para el profesor

“Lo importante no es memorizar nombres de arquitectura. Lo importante es entender que todo sistema necesita límites claros. Cuando esos límites no existen, el proyecto se vuelve frágil. Cuando sí existen, el equipo puede crecer, cambiar y mantener el software con más confianza.”
