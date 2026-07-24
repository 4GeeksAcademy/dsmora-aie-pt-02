# Guía docente: Class 28 - Arquitectura backend, FastAPI y entornos virtuales

Este documento está pensado para el profesor. No es un resumen para alumnos, sino un soporte para explicar con propiedad, responder dudas y guiar el debate de forma clara.

## 1) Objetivo de la clase

Ayudar al grupo a entender que la arquitectura backend no es un detalle estético, sino una decisión que afecta a:

- claridad del código
- facilidad para cambiar cosas después
- capacidad de trabajar en equipo
- calidad de los tests
- coste de mantenimiento

La idea central es que el alumnado aprenda a tomar decisiones con criterio, no solo a repetir nombres.

## 2) Qué debe quedar claro al final

El profesor debería dejar estas ideas muy visibles:

- La arquitectura ayuda a organizar responsabilidades.
- No existe una arquitectura “mejor” en absoluto; existe una más adecuada según el contexto.
- MVC, capas, hexagonal y serverless no son incompatibles: son formas distintas de pensar la separación.
- FastAPI ayuda a exponer una API, pero la arquitectura es lo que hace que el proyecto sea sostenible.
- `uv` no es un detalle opcional: es parte del flujo profesional porque hace el entorno reproducible.

## 3) Cómo explicarlo sin que suene abstracto

La forma más útil es partir de un problema real.

### Historia base para el profesor

“Imagina un proyecto en el que una ruta HTTP hace validación, lógica de negocio y acceso a datos al mismo tiempo. El sistema funciona, pero cada cambio comienza a romper otras cosas. La arquitectura sirve para poner límites claros.”

### Regla de oro

No se enseña arquitectura como teoría pura. Se enseña como respuesta a una pregunta concreta:

- ¿Qué pasa cuando el proyecto empieza a crecer?
- ¿Qué pasa si cambia la base de datos?
- ¿Qué pasa si entra más gente al equipo?
- ¿Qué pasa si un endpoint termina haciendo demasiado?

## 4) Comparación breve de arquitecturas

La comparación debe ser sencilla y práctica.

- Monolítica: empieza simple y funciona bien para MVP pequeños, pero se vuelve difícil de mantener si crece sin límites claros.
- MVC: separa modelo, vista y controlador para hacer más visible el flujo de una petición.
- Capas: organiza el sistema por niveles de responsabilidad, lo que suele ayudar mucho a equipos que necesitan claridad.
- Hexagonal: aísla el núcleo de negocio de tecnologías externas como bases de datos o frameworks.
- Microservicios: divide el sistema en piezas más pequeñas, útil cuando hay muchos equipos o mucha escalabilidad, pero con más complejidad operativa.
- Serverless: ejecuta funciones por eventos sin gestionar infraestructura directamente, útil para ciertos escenarios, pero con dependencia del proveedor.

## 5) Ejemplo simple de estructura de carpetas

Un ejemplo útil para mostrar en clase es este:

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

La idea no es que este árbol sea perfecto, sino que permita mostrar claramente qué se separa y por qué.

- `api` recibe la petición
- `services` contiene la lógica de negocio
- `repositories` encapsula el acceso a datos
- `models` representa entidades o contratos

## 6) Ejemplo de refactorización para explicar el problema

Un ejemplo muy útil es mostrar un endpoint que mezcla todo a la vez:

```python
@app.post("/users")
def create_user(payload: dict):
    if "email" not in payload:
        return {"error": "email required"}, 400

    if "@" not in payload["email"]:
        return {"error": "invalid email"}, 400

    db.append(payload)
    return {"ok": True}, 201
```

Luego el profesor puede pedir una mejora sencilla: mover la validación a un servicio y el acceso a datos a un repositorio. Eso permite explicar que el problema no es que el código “funcione”, sino que mezcla responsabilidades y se vuelve frágil.

## 7) Ritmo recomendado de la clase

- Apertura: 5 min
- Aprender: 10 min
- Reflexionar: 10 min
- Tener en cuenta: 8 min
- Hacer: 8 min
- Evitar: 8 min
- Cierre: 5 min

## 8) Puntos imprescindibles que debe cubrir el profesor

- Trade-offs entre MVC y arquitectura en capas para el proyecto transversal.
- Reglas básicas de imports en Python y riesgo de dependencias circulares.
- Por qué FastAPI aporta valor frente a montar HTTP de forma manual.
- Por qué `uv` es clave para entornos reproducibles y trabajo en equipo.
- Priorizar razones de negocio sobre términos de moda.

## 9) Preguntas clave para el debate

- ¿Qué decisión de arquitectura del día uno genera más rework meses después y por qué?
- ¿Dónde está la línea entre “estructura suficiente” y sobre-diseño prematuro?
- ¿Cómo detectar que un layout de carpetas sirve para hoy pero bloquea mañana?
- ¿Por qué importa un entorno reproducible como `uv` cuando hay compañeros o agentes de código implicados?

## 10) Checkpoint de la clase

Cada estudiante debe defender una propuesta concreta de arquitectura para el proyecto transversal con una razón de negocio clara. No basta con decir “usar capas”; hay que explicar por qué esa decisión ayuda al proyecto.

## 11) Prompts útiles para IA durante la clase

- “Actúa como arquitecto backend senior y explica en español cuándo conviene usar MVC, capas, hexagonal, microservicios y serverless. Incluye una ventaja y un riesgo de cada una.”
- “Tengo una API en FastAPI donde una ruta mezcla validación, negocio y acceso a datos. Propón una refactorización paso a paso con una estructura de carpetas clara.”
- “Explícame por qué `uv` es importante para un proyecto Python colaborativo y qué diferencia hay entre `pyproject.toml`, `uv.lock` y `.venv`.”

## 12) Cierre recomendado

“Lo importante no es memorizar nombres de arquitectura. Lo importante es entender que todo sistema necesita límites claros. Cuando esos límites no existen, el proyecto se vuelve frágil. Cuando sí existen, el equipo puede crecer, cambiar y mantener el software con más confianza.”
