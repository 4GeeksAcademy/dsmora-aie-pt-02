# Guía Docente Completa: Class 31 - Introducción a Agentes de IA y Primer Agente en Python

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos, prompts completos y un mini demo de Python para enseñar desde lo conceptual hasta la implementación básica.

## 1) Objetivo de la clase

Al finalizar, el estudiante podrá:

- Entender la diferencia entre un LLM simple y un agente de IA.
- Explicar el ciclo observar → decidir → actuar y por qué necesita límites de bucle.
- Distinguir cuándo una llamada directa a un modelo basta y cuándo conviene un agente.
- Crear un agente básico en Python con herramientas simples y una instrucción del sistema clara.
- Aplicar buenas prácticas para evitar errores comunes en agentes.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y contexto: 5 min
- Bloque A: Qué es un agente y cómo se diferencia de un LLM: 10 min
- Bloque B: Ciclo del agente y límites del bucle: 12 min
- Bloque C: Herramientas, instrucciones del sistema y mejores prácticas: 15 min
- Bloque D: Demo en Python de un agente simple: 15 min
- Cierre + preguntas + checklist: 8 min

Si tienes 75 min:

- Añade 8-10 min de práctica guiada para modificar la herramienta o el objetivo del agente.

Si tienes 60 min:

- Recorta el bloque D a una demo breve y deja la parte de extensiones como tarea opcional.

## 3) Preparación docente (antes de clase)

Checklist técnico:

- Python 3.10+ disponible.
- Terminal abierta en la carpeta del proyecto.
- `python3` disponible.
- Conexión a internet no es necesaria para la demo, pero sí para mostrar el contexto del curso.

Comandos de verificación previa:

```bash
python3 --version
```

Carpeta demo sugerida:

```bash
mkdir -p class_31/demo_agent
cd class_31/demo_agent
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Qué decir (literal):

"Hoy vamos a pasar de hablar de modelos de lenguaje a construir sistemas que hacen más de una cosa: observan, deciden y actúan."

"El objetivo no es solo responder preguntas, sino crear agentes que puedan ejecutar pasos hasta alcanzar una meta."

## Bloque A - Qué es un agente y cómo se diferencia de un LLM (10 min)

### A1. Concepto rápido (4 min)

Qué decir (literal):

"Un LLM simple recibe una entrada y devuelve una salida. Un agente, en cambio, sigue un ciclo: observa lo que pasa, decide qué hacer y actúa."

"Eso lo hace útil para tareas de varios pasos, como buscar información, usar herramientas y corregir el camino según lo que va descubriendo."

### A2. Ejemplo de comparación (3 min)

Qué decir (literal):

"Si le pido a un modelo que traduzca una frase, una sola llamada basta. Si le pido que reserve un vuelo, compare opciones y finalmente confirme, eso ya no es una sola acción: requiere un proceso más complejo."

### A3. Mini reflexión (3 min)

Prompt exacto sugerido para OpenClaw:

```text
Actúa como profesor de IA. Explícame con un ejemplo simple la diferencia entre un LLM y un agente de IA, y dime cuándo conviene usar uno u otro en un proyecto real.
```

## Bloque B - Ciclo del agente y límites del bucle (12 min)

### B1. Observa, decide, actúa (6 min)

Qué decir (literal):

"El corazón de un agente es un bucle. Primero observa el estado actual, luego decide qué hacer y finalmente actúa. Después repite el proceso si todavía no ha terminado."

"En programación, esto se representa con un bucle while o for controlado por un máximo de iteraciones."

### B2. Riesgo de bucles infinitos (3 min)

Qué decir (literal):

"Sin límites, un agente puede quedarse repitiendo acciones indefinidamente. Por eso necesitamos condiciones de parada, como alcanzar la respuesta final, llegar al límite de iteraciones o detectar un error."

### B3. Mini ejemplo de diseño (3 min)

Qué decir (literal):

"Un agente bien diseñado no solo piensa: también sabe cuándo parar. Eso es clave para que sea confiable y no consuma recursos de forma descontrolada."

## Bloque C - Herramientas, instrucciones del sistema y mejores prácticas (15 min)

### C1. Qué son las herramientas (5 min)

Qué decir (literal):

"Las herramientas son funciones de Python que el agente puede invocar para hacer algo concreto: consultar datos, buscar información, ejecutar una acción o transformar un resultado."

"El modelo no ejecuta el trabajo directamente; decide qué herramienta usar según el contexto."

### C2. Instrucciones del sistema (5 min)

Qué decir (literal):

"La instrucción del sistema es como la 'programación cerebral' del agente. Le dice qué objetivo tiene, qué herramientas puede usar y en qué formato debe responder."

"Si el formato es ambiguo, el agente se vuelve impredecible. Si el formato es claro, el código puede consumir sus respuestas de forma confiable."

### C3. Mejores prácticas (5 min)

Qué decir (literal):

"Conviene mantener herramientas simples y específicas, limitar su número, validar entradas y registrar qué hizo el agente en cada paso."

"Un agente confiable no se construye con muchas herramientas aleatorias, sino con pocas decisiones bien definidas."

Prompt exacto sugerido para OpenClaw:

```text
Actúa como experto en diseño de agentes de IA. Dame un ejemplo breve de cómo estructurar un sistema prompt para un agente que puede usar dos herramientas simples: una para obtener el clima y otra para responder en español.
```

## Bloque D - Demo en Python: construir un agente simple (15 min)

### D1. Crear el archivo de demo (5 min)

Ejecuta:

```bash
cd class_31/demo_agent
cat > agent_demo.py <<'PY'
from typing import List, Dict

memory: List[Dict[str, str]] = []


def get_weather(city: str) -> str:
    return f"El clima en {city} es agradable y soleado."


def get_greeting(name: str, language: str) -> str:
    if language == "es":
        return f"¡Hola, {name}!"
    return f"Hello, {name}!"


def fake_llm(memory: List[Dict[str, str]]) -> Dict[str, str]:
    user_text = " ".join(item["content"] for item in memory if item["role"] == "user")
    if "clima" in user_text.lower():
        return {"type": "tool_call", "tool": "get_weather", "args": {"city": "Madrid"}}
    if "hola" in user_text.lower():
        return {"type": "tool_call", "tool": "get_greeting", "args": {"name": "Ana", "language": "es"}}
    return {"type": "final_answer", "content": "No puedo hacer esa tarea aún."}


def run_agent(user_input: str) -> str:
    memory.append({"role": "user", "content": user_input})
    for _ in range(3):
        decision = fake_llm(memory)
        if decision["type"] == "final_answer":
            return decision["content"]

        if decision["tool"] == "get_weather":
            result = get_weather(decision["args"]["city"])
        elif decision["tool"] == "get_greeting":
            result = get_greeting(decision["args"]["name"], decision["args"]["language"])
        else:
            result = "Herramienta desconocida"

        memory.append({"role": "tool", "content": result})

    return "Se alcanzó el límite de iteraciones"


print(run_agent("¿Cuál es el clima en Madrid?"))
print(run_agent("Hola"))
PY
python3 agent_demo.py
```

### D2. Explicar lo que pasa (5 min)

Qué decir (literal):

"Aquí se ve el patrón básico: el agente observa la entrada, decide qué herramienta usar y ejecuta una acción. Luego puede continuar si necesita más contexto."

"La clave es que el modelo toma decisiones, pero las herramientas son las que hacen trabajo real."

### D3. Variación rápida (5 min)

Qué decir (literal):

"Si quieren, podemos ampliar el ejemplo con una segunda herramienta, una condición de parada más explícita o un prompt del sistema que oriente mejor las decisiones."

## Cierre (5-8 min)

Qué decir (literal):

"Lo más importante es que un agente no es magia: es un patrón de diseño con objetivo, herramientas, memoria y un bucle de decisión."

"Si entendemos esto, ya estamos listos para construir sistemas más útiles y más complejos."

Preguntas de chequeo:

- ¿Cuál es la diferencia principal entre un LLM y un agente?
- ¿Por qué necesitamos límites de iteración?
- ¿Qué hace una herramienta en un agente?
- ¿Por qué la instrucción del sistema importa tanto?

## 5) Variantes de recorte y extensión

### Versión 60 min

- Reducir el bloque C a 10 min.
- Mantener la demo de Python en una sola ejecución.
- Dejar la parte de mejorar el prompt como tarea opcional.

### Versión 75 min

- Añadir 10 min de práctica guiada para cambiar el objetivo del agente o añadir una segunda herramienta.
- Pedir a los estudiantes que modifiquen el ejemplo para responder a una pregunta más compleja.

## 6) Plan de contingencia

Si el ejemplo en Python falla:

- Verificar que `python3` funcione.
- Revisar que el archivo `agent_demo.py` exista en la carpeta correcta.
- Simplificar el ejemplo y dejar solo una herramienta.

Si la discusión se alarga:

- Mover la demo a un segundo plano y terminar con la explicación conceptual.
- Dejar la práctica extra como tarea opcional para casa.
