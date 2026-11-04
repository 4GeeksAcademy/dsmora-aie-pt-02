# Guía docente: Clase 72 - Gobernanza y seguridad de sistemas de IA

Duración base: 70 minutos, adaptable a 60 o 75. Guía autosuficiente para el profesor.

## Fuentes y límites

Las únicas fuentes técnicas son los cuatro JSON de esta carpeta. Referencias: `[G:N]` = `ai_governance.json`; `[D:N]` = `security_by_design_for_ai_systems.json`; `[N:N]` = `the_nist_cybersecurity_framework.json`; `[A:N]` = `security_in_agentic_systems.json`. El número corresponde al campo `index`.

Se extrajeron 42 tarjetas con 37 cuerpos distintos. G:8–9, N:8–9 y A:8–9 repiten cada una el mismo cuerpo de evaluación/conclusión. D:9–11 repiten el ejercicio de validar salidas no confiables. No contar esos duplicados como lecciones adicionales. Los JSON no proporcionan comandos de terminal ni prompts de OpenClaw; no se inventan. Los dos ejercicios de código sí incluyen el enunciado y resultados esperados en sus fuentes.

## Continuidad y objetivos

La clase 71 recorrió riesgos de servidores, aplicaciones web y aplicaciones LLM. Esta clase conecta esos riesgos con las decisiones que los gobiernan: quién responde por el sistema de IA, cómo se estructura la gestión de ciberseguridad y qué controles deben interponerse antes de que un agente actúe.

**Qué decir (literal):** «En la clase anterior identificamos riesgos en servidores y aplicaciones. Hoy damos el siguiente paso: definir quién responde por cada función de IA y diseñar controles para que entradas o decisiones del modelo no lleguen sin revisión a datos y herramientas».

Al terminar, el estudiante podrá:

- Distinguir gobernanza de seguridad y describir qué datos, modelo, proveedor y responsable registrar en un inventario de IA. [G:1–3]
- Relacionar las seis funciones del Marco NIST con actividades de ciberseguridad. [N:1–7]
- Explicar mínimo privilegio, entrada no confiable, sandboxing y aprobación humana como decisiones de diseño. [D:1–3,7–9]
- Aplicar las reglas de `review_action(action)` y `classify(action)` a las acciones de prueba de las lecciones. [D:9; A:5]

## Preparación y contingencia

- Tener esta guía a mano. Los fragmentos de código incluidos abajo contienen el contrato de los ejercicios y los datos de prueba publicados en los JSON.
- No ejecutar las funciones sobre herramientas o sistemas reales durante la clase: su propósito aquí es clasificar acciones y observar las salidas esperadas.
- La extracción no da instrucciones de instalación, comandos de terminal ni prompts de OpenClaw. No afirmar que los archivos `action_gate.py` o `agent_gate.py` existen localmente; se mencionan como archivos del ejercicio.
- Si no hay entorno Python, resolver las dos funciones en pizarra usando los ejemplos y veredictos de esta guía.

## Agenda base: 70 minutos

| Minutos | Bloque |
| --- | --- |
| 0–5 | Continuidad: del riesgo a la responsabilidad |
| 5–18 | Gobernanza de IA: inventario, roles y datos |
| 18–30 | NIST: seis funciones para gestionar ciberseguridad |
| 30–44 | Seguridad por diseño: entradas, permisos y límites |
| 44–56 | Seguridad agentiva: capacidades, confirmación y confidencialidad |
| 56–66 | Ejercicios: puertas de decisión para acciones |
| 66–70 | Preguntas de chequeo y cierre |

## 0–5 min: del riesgo a la responsabilidad

**Qué decir (literal):** «Una lista de riesgos ayuda a reconocer problemas; la gobernanza añade otras preguntas: quién decidió el propósito, qué datos se procesan y quién responde por el resultado».

La lección diferencia seguridad —si alguien puede entrar sin permiso— de gobernanza —qué está permitido, quién lo decidió y qué queda registrado—. [G:1]

**Pregunta:** «¿Puede un sistema estar protegido contra accesos no autorizados y, aun así, carecer de gobernanza?»

**Respuesta esperada:** sí. Seguridad y gobernanza responden preguntas distintas; la gobernanza define reglas, decisiones y responsabilidad. [G:1]

## 5–18 min: gobernanza de IA, inventario y datos

**Qué decir (literal):** «No podemos responder qué reglas aplican ni quién es responsable si ni siquiera sabemos qué funciones de IA tenemos o qué datos les enviamos».

El inventario es un registro vivo de funciones de IA. La fuente enumera campos como nombre y responsable de la función, modelo y proveedor, entradas de datos, retención y uso para entrenamiento, revisión humana y manejo de fallos. El proveedor controla el modelo y su infraestructura; el equipo que lo integra decide el propósito, los datos enviados y la experiencia para sus usuarios. Usar un modelo externo no transfiere automáticamente esas decisiones. [G:2–3]

La unidad presenta la Ley de IA de la UE como un marco que clasifica usos según riesgo y ámbito de aplicación. Para el GDPR, destaca la minimización: enviar al modelo solo los campos necesarios, documentar por qué se procesan los datos y considerar revisión humana para decisiones automatizadas con efectos significativos. También incluye lecciones sobre datos educativos (FERPA) y de salud (HIPAA); son ejemplos de contextos donde el tipo de dato y el rol del proveedor afectan el análisis. [G:4–7]

Ejemplo de minimización tomado de la fuente: construir la entrada con el código de país en vez del perfil completo. [G:5]

```javascript
const promptData = { country: user.countryCode };
const prompt = `Mostrar publicaciones populares en ${promptData.country}`;
```

Explicar que el objeto contiene el dato mínimo usado en el prompt del ejemplo. No ampliar la afirmación a otros campos ni añadir datos personales. [G:5]

**Qué preguntar después:** «¿Qué decisiones siguen siendo responsabilidad del equipo aunque el modelo lo ofrezca un proveedor externo?»

**Respuesta esperada:** el propósito de la función, qué datos se le envían, cómo se informa a los usuarios y la responsabilidad inicial por el despliegue. [G:3]

## 18–30 min: NIST y las seis funciones

**Qué decir (literal):** «El marco no es un producto para instalar ni una certificación que se completa una vez. Organiza resultados y ofrece un lenguaje compartido para gestionar la ciberseguridad».

Recorrer las funciones como un ciclo de trabajo; `Gobernar` sustenta las demás: [N:1–7]

| Función | Idea que debe quedar clara |
| --- | --- |
| Gobernar | Definir contexto, responsabilidades, estrategia y apetito de riesgo. [N:2] |
| Identificar | Mantener inventarios de activos y datos, clasificarlos y evaluar riesgos. [N:3] |
| Proteger | Aplicar salvaguardas como mínimo privilegio, identidad y acceso y configuraciones seguras. [N:4] |
| Detectar | Monitorear, registrar eventos y ajustar alertas para que sean útiles. [N:5] |
| Responder | Preparar roles, responsabilidades y rutas de escalamiento antes del incidente. [N:6] |
| Recuperar | Restaurar servicios según prioridades y objetivos de continuidad; probar la recuperación. [N:7–9] |

La evaluación ofrece un ejemplo útil: tener copias de seguridad nocturnas no basta si nunca se probó restaurarlas. [N:9]

**Pregunta:** «¿Qué función contiene la acción de detectar y escalar un incidente? ¿Y cuál cubre volver a operar?»

**Respuesta esperada:** Responder y Recuperar, respectivamente. [N:6–7]

## 30–44 min: seguridad por diseño

**Qué decir (literal):** «La defensa no debe depender de que el modelo obedezca siempre. Diseñemos límites externos: tratemos las entradas como no confiables, demos pocos permisos y validemos las acciones antes de ejecutarlas».

Puntos para explicar en orden:

1. **Mínimo privilegio y fallo seguro:** dar a cada componente solo los permisos necesarios; cuando una acción no se reconoce, rechazarla en vez de permitirla por defecto. [D:1]
2. **Entradas no confiables:** datos de usuario, APIs externas, archivos, webhooks y mensajes de cola no son confiables solo por su formato o procedencia. [D:2]
3. **Secretos fuera del código:** la lección identifica claves API, contraseñas y tokens como secretos y explica que el historial del repositorio o los registros de CI/CD pueden conservarlos o exponerlos. [D:3]
4. **Inyección y fuga:** las instrucciones y el contenido llegan como texto al LLM; el prompt del sistema no es una frontera de seguridad que garantice que la información no se filtre. [D:4–5]
5. **Sandbox y límites:** ejecutar código generado en un entorno aislado, sin credenciales de producción, acceso irrestricto al host o a la red, y con un límite de tiempo; la fuente también propone limitar la tasa. [D:7]
6. **Registro y revisión humana:** conservar suficiente información para reconstruir qué ocurrió y exigir aprobación antes de determinadas acciones. [D:8]

**Qué preguntar después:** «Si el modelo propone una acción, ¿qué componente debe decidir si pasa a una herramienta?»

**Respuesta esperada:** código externo al modelo que revise la acción antes de permitirla, solicitar confirmación o denegarla. [D:9]

## 44–56 min: seguridad de sistemas agentivos

**Qué decir (literal):** «En un agente, texto y datos pueden influir en una decisión de acción. El control decisivo no es hacer el prompt cada vez más largo; es limitar lo que el agente puede hacer y poner una puerta de autorización fuera del modelo».

La lección explica que el lenguaje natural es una superficie de ataque y que el system prompt puede orientar el comportamiento habitual, pero no garantiza por sí solo límites absolutos. El mínimo privilegio del modelo limita herramientas, credenciales y accesos; pedir confirmación depende de la reversibilidad y del radio de impacto. [A:1–4]

La confidencialidad se revisa tanto en entradas como salidas: el contexto puede incluir mensajes, documentos recuperados, resultados de herramientas, historial y otros agentes. La fuente también cubre agotamiento de recursos por el coste de solicitudes, múltiples llamadas o contextos largos. [A:6–7]

**Pregunta:** «¿Qué dos criterios propone la lección para decidir si una acción debe esperar aprobación humana?»

**Respuesta esperada:** si es reversible y cuál es su radio de impacto. [A:4]

## 56–66 min: dos puertas de decisión

### Ejercicio 1: `review_action(action)`

La función recibe un diccionario `action` con el campo `type`. Usa `SAFE_ACTIONS` y `CONFIRM_ACTIONS` ya definidos por el ejercicio y devuelve `allowed`, `confirm` o `denied`. Una acción segura se permite; una acción irreversible conocida requiere confirmación; un tipo desconocido o ausente se deniega sin producir error. [D:9]

Solución mínima derivada directamente del contrato del ejercicio: [D:9]

```python
SAFE_ACTIONS = {"read_file", "search_docs", "summarize"}
CONFIRM_ACTIONS = {"send_email", "delete_record", "transfer_funds"}
PROPOSED = [
    {"type": "read_file"},
    {"type": "send_email"},
    {"type": "drop_table"},
    {},
]

def review_action(action):
    action_type = action.get("type")
    if action_type in CONFIRM_ACTIONS:
        return "confirm"
    if action_type in SAFE_ACTIONS:
        return "allowed"
    return "denied"

for action in PROPOSED:
    print(review_action(action))
```

Resultado esperado: `allowed`, `confirm`, `denied`, `denied`. La ausencia de `type` se trata como desconocida y la puerta falla cerrada. [D:9]

### Ejercicio 2: `classify(action)`

La función recibe una acción con campo `tool` y, opcionalmente, `records`. El ejercicio ya define `GRANTED`, `IRREVERSIBLE` y `BULK_THRESHOLD`. Primero se rechaza una herramienta no concedida; luego se pide confirmación para una herramienta irreversible o una acción concedida que supera el umbral de registros. Si falta `records`, se considera un registro. [A:5]

Implementación de la regla descrita por el ejercicio: [A:5]

```python
def classify(action):
    tool = action.get("tool")
    if tool not in GRANTED:
        return "denied"
    if tool in IRREVERSIBLE:
        return "confirm"
    if action.get("records", 1) > BULK_THRESHOLD:
        return "confirm"
    return "allowed"
```

Resultados esperados en las acciones de prueba: `read_file` → `allowed`; `send_email` → `confirm`; `update_rows` con 5000 registros → `confirm`; `run_shell` no concedida → `denied`. [A:5]

**Qué decir (literal):** «El primer control decide por tipo de acción. El segundo añade permisos concedidos, irreversibilidad y volumen. En ambos, lo desconocido no pasa automáticamente».

## 66–70 min: cierre

Preguntas de chequeo:

- ¿Qué diferencia hay entre gobernanza y seguridad? [G:1]
- ¿Qué función del marco NIST sustenta las otras cinco? [N:2,8]
- ¿Qué debe suceder con una herramienta no concedida o un tipo de acción desconocido? [D:9; A:5]
- ¿Cuándo pasa una acción de agente de ejecución automática a confirmación? [A:4–5]

**Cierre sugerido (literal):** «Gobernar es saber qué IA existe y quién responde por sus datos y propósito. Gestionar seguridad requiere identificar, proteger, detectar, responder y recuperar. Y cuando un agente propone una acción, un control externo debe decidir si se permite, se confirma o se deniega».

## Ajustes de duración

- **Versión de 60 minutos:** reducir a una pregunta de cada marco regulatorio; explicar NIST con una frase por función; resolver solo `classify` y mencionar `review_action` como segundo ejemplo de fallo cerrado.
- **Versión de 75 minutos:** dedicar cinco minutos adicionales a que el grupo clasifique las cuatro acciones de `PROPOSED` y justifique cada veredicto usando los conjuntos y el umbral definidos en el ejercicio.

## Límites de demostración

Los JSON no incluyen comandos para iniciar los ejercicios ni prompts de OpenClaw. Los fragmentos Python reproducen el contrato, las constantes y los resultados dados por las lecciones; `classify` asume que `GRANTED`, `IRREVERSIBLE` y `BULK_THRESHOLD` ya están definidos como indica el ejercicio. No ejecutar las puertas contra herramientas reales.