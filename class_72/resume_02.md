# Dossier ampliado para NotebookLM: gobernanza y seguridad de sistemas de IA

## Alcance y procedencia

Este documento organiza las cuatro extracciones LearnPack de `class_72`. Las únicas fuentes técnicas son los JSON indicados en la tabla. Las referencias `[G:N]`, `[D:N]`, `[N:N]` y `[A:N]` apuntan al campo `index` de cada JSON.

| Código | JSON | Tarjetas extraídas | Cuerpos distintos |
| --- | --- | ---: | ---: |
| G | `ai_governance.json` | 10 | 9 |
| D | `security_by_design_for_ai_systems.json` | 12 | 10 |
| N | `the_nist_cybersecurity_framework.json` | 10 | 9 |
| A | `security_in_agentic_systems.json` | 10 | 9 |

En total hay 42 tarjetas y 37 cuerpos distintos. La comparación se hizo sobre `content`, no sobre los títulos:

- G:8–9 repiten la evaluación de gobernanza. [G:8–9]
- D:9–11 repiten el ejercicio de validar salidas no confiables. [D:9–11]
- N:8–9 repiten la evaluación del marco. [N:8–9]
- A:8–9 repiten la evaluación de seguridad de agentes. [A:8–9]

Las tarjetas repetidas no son lecciones independientes. Los JSON no incluyen comandos de terminal ni prompts de OpenClaw. Los ejercicios de autorización sí contienen contratos y ejemplos de entrada/salida; no se presume que los archivos indicados por el curso existan en el entorno local.

## Continuidad con la clase anterior

`class_71` presentó riesgos de servidores, aplicaciones web y aplicaciones LLM. Esta clase desplaza el foco desde identificar riesgos hacia establecer responsabilidad, organizar la gestión de ciberseguridad y diseñar controles que limiten lo que sistemas de IA y agentes pueden hacer. Esta transición es contextual; las afirmaciones técnicas siguientes proceden de `class_72`.

## 1. Gobernanza de IA

### 1.1 Gobernanza frente a seguridad

La fuente distingue ambos conceptos mediante las preguntas que responden: seguridad pregunta si alguien puede entrar sin permiso; gobernanza pregunta qué está permitido, quién lo decidió y qué se registra. Un sistema puede tener controles de acceso y aun así carecer de responsabilidad y reglas de uso claras. [G:1]

### 1.2 Inventario y responsabilidad

El inventario es un registro vivo de cada función de IA desplegada. Entre sus campos están: nombre de la función y responsable, modelo y proveedor, datos de entrada, retención/uso para entrenamiento, revisión humana y manejo de fallos. La lección recomienda integrarlo al flujo de desarrollo y mantenerlo actualizado cuando cambien llamadas de IA o fuentes de datos. [G:2]

Integrar un proveedor externo no transfiere todas las decisiones. El proveedor controla aspectos del modelo y su infraestructura; el equipo que lo despliega decide el propósito de la función, qué datos envía y cómo informa a sus usuarios. El curso conecta esa división con las figuras de proveedor/desplegador de la Ley de IA de la UE y responsable/encargado del tratamiento en GDPR. [G:3]

### 1.3 Regulaciones y datos

- **Ley de IA de la UE:** la fuente explica que el análisis depende del uso y nivel de riesgo, no solo del modelo utilizado. [G:4]
- **GDPR:** minimizar los datos enviados al modelo y documentar el propósito y la base de procesamiento; la lección también destaca supervisión humana para determinadas decisiones automatizadas y registros de versiones y retención. [G:5]
- **FERPA:** aborda registros educativos y el uso de datos por proveedores de IA dentro del propósito y control de la institución. [G:6]
- **HIPAA:** presenta la información de salud protegida y los roles de entidades cubiertas y asociados comerciales. [G:7]

Ejemplo de minimización de datos mostrado por la lección: [G:5]

```javascript
const promptData = { country: user.countryCode };
const prompt = `Mostrar publicaciones populares en ${promptData.country}`;
```

El ejemplo pasa el código de país en lugar del objeto de usuario completo.

## 2. Marco de Ciberseguridad NIST

El material presenta el marco como un conjunto estructurado de resultados y vocabulario común, no como un producto o certificación. La función `Gobernar` sustenta las demás porque define contexto, responsabilidad y estrategia de riesgo. [N:1–2,8]

| Función | Contenido en la extracción |
| --- | --- |
| Gobernar | Contexto organizativo, apetito de riesgo, responsabilidad y dirección. [N:2] |
| Identificar | Inventario de activos de hardware/software y datos; clasificación y evaluación continua de riesgos. [N:3] |
| Proteger | Salvaguardas como gestión de identidad/acceso, mínimo privilegio, autenticación multifactor y configuraciones seguras. [N:4] |
| Detectar | Monitoreo continuo, registros, rutas de auditoría y ajuste de alertas. [N:5] |
| Responder | Roles, responsabilidades, comunicación y rutas de escalamiento preparados antes de un incidente. [N:6] |
| Recuperar | Restauración alineada con continuidad, prioridades de servicio y objetivos de tiempo de recuperación; probar que la restauración funciona. [N:7–9] |

La evaluación subraya que hacer copias de seguridad sin probar una restauración no demuestra que la recuperación esté lista. [N:9]

## 3. Seguridad por diseño para sistemas de IA

El módulo enmarca la seguridad como una propiedad del diseño: manejar entradas y salidas no confiables con salvaguardas desde el inicio. [D:0]

- **Mínimo privilegio y fallo seguro:** cada componente recibe solo los permisos necesarios; una acción que no se reconoce se rechaza por defecto. [D:1]
- **Entradas no confiables:** entradas de usuarios y servicios externos, archivos, webhooks y mensajes deben tratarse como no confiables. [D:2]
- **Secretos fuera del código:** claves, contraseñas y tokens no deben codificarse en el repositorio; el historial y los registros automatizados pueden conservarlos o exponerlos. [D:3]
- **Inyección de prompt y fuga:** instrucciones y contenido llegan al modelo como texto; el prompt del sistema no garantiza por sí solo que secretos o datos ajenos permanezcan ocultos. [D:4–5]
- **Agencia excesiva:** la salida del modelo que pueda convertirse en acción debe revisarse como entrada no confiable. [D:6]
- **Sandboxing y límites:** el código generado debe ejecutarse aislado, sin acceso a credenciales de producción, al host o a red irrestricta, con límite de tiempo; se recomienda limitar tasa. [D:7]
- **Registro y aprobación humana:** mantener una pista de auditoría que permita reconstruir acciones, y requerir revisión humana en acciones relevantes. [D:8]

### Ejercicio `review_action(action)`

El ejercicio define `SAFE_ACTIONS`, `CONFIRM_ACTIONS` y `PROPOSED`. La función debe aceptar acciones seguras, exigir confirmación para acciones conocidas e irreversibles, y denegar tipos desconocidos o ausentes. [D:9]

```python
def review_action(action):
    action_type = action.get("type")
    if action_type in CONFIRM_ACTIONS:
        return "confirm"
    if action_type in SAFE_ACTIONS:
        return "allowed"
    return "denied"
```

Para las entradas suministradas, se esperan estos resultados en orden: `read_file` → `allowed`; `send_email` → `confirm`; `drop_table` → `denied`; acción sin `type` → `denied`. [D:9]

## 4. Seguridad en sistemas agentivos

El curso describe el lenguaje natural como superficie de ataque: instrucciones y datos se procesan juntos, por lo que un prompt de sistema orienta pero no impone un límite de seguridad absoluto. [A:0–2]

- **Mínimo privilegio del modelo:** conceder al agente solo las herramientas, credenciales y accesos necesarios. [A:3]
- **Aprobación antes de actuar:** usar reversibilidad y radio de impacto para decidir qué acciones requieren confirmación humana. [A:4]
- **Control de acciones:** una puerta en código ordinario decide entre `allowed`, `confirm` y `denied`, sin delegar la autorización al modelo. [A:5]
- **Confidencialidad:** controlar las fuentes que entran al contexto —usuario, documentos, herramientas, historial y otros agentes— y las salidas que pueden revelar datos. [A:6]
- **Agotamiento de recursos:** las solicitudes pueden disparar cálculos costosos, varias llamadas o contextos largos; el módulo examina el riesgo de degradación y costos imprevistos. [A:7]

### Ejercicio `classify(action)`

El ejercicio proporciona `GRANTED`, `IRREVERSIBLE`, `BULK_THRESHOLD` y `PROPOSED`. La función debe denegar herramientas no concedidas, pedir confirmación para herramientas irreversibles o acciones concedidas que superen el umbral de registros, y permitir solo acciones concedidas, reversibles y dentro del límite. Si no se indica `records`, se considera un registro. [A:5]

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

Los resultados esperados para las entradas citadas son: `read_file` → `allowed`; `send_email` → `confirm`; `update_rows` con 5000 registros → `confirm`; `run_shell` no concedida → `denied`. [A:5]

## 5. Síntesis

Los cuatro módulos se conectan mediante una cadena de decisiones:

1. **Gobernanza:** saber qué funciones de IA existen, qué datos procesan y quién responde por propósito y despliegue. [G:2–3]
2. **Gestión:** organizar activos, salvaguardas, detección, respuesta y recuperación en un marco común. [N:1–7]
3. **Diseño:** limitar privilegios y tratar entradas, secretos y salidas de IA con controles externos. [D:1–9]
4. **Acción agentiva:** comprobar autorización, irreversibilidad y volumen antes de permitir que una acción alcance una herramienta. [A:3–5]

La extracción no contiene instrucciones de instalación ni comandos para ejecutar los ejercicios; las funciones anteriores expresan únicamente las reglas y pruebas descritas en los JSON. No se debe inferir que constituyen una implementación completa para producción.