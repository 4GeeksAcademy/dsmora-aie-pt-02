# Guia Docente Completa: Class 23 - Arquitectura Avanzada y Skills en OpenClaw

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para demos en vivo.

## 1) Objetivos de aprendizaje

Al finalizar, el estudiante podra:

- Explicar las 3 capas arquitectonicas de OpenClaw: espacio de trabajo, estructura de archivos y diagnosticos.
- Identificar cuando usar multiples espacios de trabajo para aislamiento de contexto y seguridad.
- Describir el rol de los archivos clave del workspace (IDENTITY.md, SOUL.md, AGENTS.md, USER.md, TOOLS.md, MEMORY.md).
- Ejecutar diagnosticos basicos con `openclaw doctor`, `openclaw gateway probe` y `openclaw status --deep`.
- Diseñar e instalar una skill con `SKILL.md` usando el enfoque de divulgacion progresiva de 3 niveles.

## 2) Agenda sugerida (60-75 min)

Ruta base de 67 minutos:

- Apertura y mapa mental de la clase: 5 min
- Bloque A - Arquitectura y workspace: 15 min
- Bloque B - Privacidad, canales y diagnostico: 14 min
- Bloque C - Skills: de concepto a anatomia: 13 min
- Bloque D - Construccion guiada de una skill: 15 min
- Cierre y chequeo de comprension: 5 min

Version corta (60 min):

- Recortar 4 min del Bloque D (dejar una sola prueba de activacion).
- Recortar 3 min del Bloque B (mostrar solo `openclaw doctor`).

Version extendida (75 min):

- Agregar 8 min de laboratorio: cada estudiante define una segunda skill de su dominio.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- VS Code abierto en la raiz del repo.
- Terminal bash funcional.
- OpenClaw CLI instalado y autenticado.
- Workspace de OpenClaw inicializado.

Comandos de verificacion previa:

```bash
pwd
ls -la
openclaw --help
openclaw status || true
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy vamos a pasar de usar OpenClaw como chat inteligente a operarlo como sistema: con arquitectura clara, diagnostico y habilidades reutilizables."

"Si entiendes el workspace, los archivos y las skills, puedes construir agentes mas confiables y menos fragiles."

---

## Bloque A - Arquitectura y workspace (15 min)

### A1. Las 3 capas arquitectonicas (6 min)

Que decir (literal):

"OpenClaw se entiende en 3 capas: 1) espacio de trabajo, 2) archivos de configuracion, 3) diagnosticos. Si falla una capa, el agente se comporta raro aunque el prompt sea bueno."

"Piensen en esto como una pila: el diagnostico no reemplaza a la configuracion, y la configuracion no reemplaza a un workspace bien aislado."

### A2. Workspace como entorno operativo (5 min)

Que decir (literal):

"El workspace no es una carpeta cualquiera. Es la identidad del agente en ejecucion: su memoria, sus reglas y sus habilidades viven ahi."

"Separar workspace por cliente o por contexto personal/profesional reduce fugas de contexto y errores de seguridad."

Comando de apoyo en vivo:

```bash
echo "Workspace por contexto = menos mezcla de memoria y reglas"
```

### A3. Cuadro rapido de archivos clave (4 min)

Que decir (literal):

"No memoricen todo, memoricen para que sirve cada archivo: identidad, personalidad, reglas, usuario, herramientas y memoria."

Prompt exacto sugerido (OpenClaw):

```text
Genera una tabla en markdown con columnas:
Archivo, Rol principal, Momento de carga, Riesgo si esta mal definido.
Incluye: IDENTITY.md, SOUL.md, AGENTS.md, USER.md, TOOLS.md, MEMORY.md.
Responde en maximo 12 filas y lenguaje tecnico simple.
```

---

## Bloque B - Privacidad, canales y diagnostico (14 min)

### B1. Canales y privacidad (4 min)

Que decir (literal):

"En DM el agente puede cargar contexto mas sensible como memoria personal. En grupos, debe cargar solo lo seguro para compartir."

"La regla de oro: privacidad por defecto. Si no estas seguro, no expongas memoria en canal compartido."

### B2. Diagnosticar antes de tocar configuracion (5 min)

Que decir (literal):

"Primero diagnosticar, despues editar. Si tocas configuracion sin diagnostico, solo cambias un problema por otro."

Comandos exactos para demo:

```bash
openclaw doctor
openclaw gateway probe
openclaw status --deep
```

### B3. Lectura de salida y priorizacion (5 min)

Que decir (literal):

"No todos los mensajes tienen la misma gravedad. Error rojo primero, advertencia amarilla despues."

"Nuestro objetivo no es salida bonita: es sistema estable y repetible."

Prompt exacto sugerido (OpenClaw):

```text
Actua como mentor tecnico.
Te paso una salida de diagnostico de OpenClaw.
Devuelve:
1) Top 3 problemas por severidad
2) Causa probable de cada uno
3) Accion concreta inmediata
4) Como verificar que quedo resuelto
Formato: lista numerada, maximo 12 lineas.
```

---

## Bloque C - Skills: de concepto a anatomia (13 min)

### C1. De generalista a especialista (4 min)

Que decir (literal):

"Un LLM generalista responde muchas cosas. Una skill convierte esa capacidad en procedimiento confiable para una tarea repetible."

"Si la tarea ocurre varias veces y esperas consistencia, conviene skill. Si es unica o muy creativa, no siempre conviene."

### C2. Divulgacion progresiva de 3 niveles (4 min)

Que decir (literal):

"Nivel 1: metadata corta para decidir si activar. Nivel 2: SKILL.md con instrucciones centrales. Nivel 3: docs/scripts/referencias para casos concretos."

"Esto evita cargar todo siempre y protege contexto util para la tarea activa."

### C3. Anatomia canonica de una skill (5 min)

Comando exacto para crear estructura de ejemplo:

```bash
mkdir -p .github/skills/assignment-checker/{scripts,references}
cat > .github/skills/assignment-checker/SKILL.md << 'EOF'
---
name: assignment-checker
description: Revisa tareas pendientes de un estudiante y genera resumen accionable.
---

# Skill: assignment-checker

## Cuando usar
Cuando el usuario pida estado de tareas pendientes o resumen semanal.

## Prerrequisitos
- Token de API disponible
- ID de estudiante definido

## Procedimiento
1. Obtener tareas desde API.
2. Filtrar pendientes.
3. Generar resumen por prioridad.
4. Guardar salida en archivo con fecha.

## Salida esperada
Archivo markdown con tareas pendientes y proximos pasos.
EOF

sed -n '1,220p' .github/skills/assignment-checker/SKILL.md
```

Que decir (literal):

"Una buena descripcion activa la skill cuando corresponde. Una mala descripcion la dispara en cualquier cosa."

---

## Bloque D - Construccion guiada de una skill (15 min)

### D1. Marco de diseno en 4 preguntas (5 min)

Que decir (literal):

"Antes de escribir, respondemos 4 preguntas: que datos necesito, que acciones puedo ejecutar, que resultado verificable debo producir y cuando NO debo activar."

Prompt exacto sugerido (OpenClaw):

```text
Ayudame a disenar una skill llamada weekly-progress-report.
Responde en 4 secciones exactas:
1) Datos requeridos
2) Acciones paso a paso
3) Salida verificable
4) Casos en los que NO debe activarse
Contexto: bootcamp de programacion, seguimiento semanal de estudiantes.
```

### D2. Instalacion y prueba de activacion (6 min)

Comandos exactos para demo:

```bash
mkdir -p .github/skills/weekly-progress-report
cat > .github/skills/weekly-progress-report/SKILL.md << 'EOF'
---
name: weekly-progress-report
description: Genera reporte semanal de progreso de estudiantes con riesgos y acciones.
---

# Skill: weekly-progress-report

## Cuando usar
Cuando pidan consolidar progreso semanal de estudiantes.

## Procedimiento
1. Recolectar datos base (entregas, asistencia, bloqueos).
2. Clasificar estado por estudiante.
3. Redactar reporte con riesgos y acciones.

## Salida esperada
Tabla por estudiante y plan de seguimiento semanal.
EOF

sed -n '1,200p' .github/skills/weekly-progress-report/SKILL.md
```

### D3. Iteracion rapida (4 min)

Que decir (literal):

"Una skill no se califica por intencion sino por comportamiento. La medimos con activaciones correctas y salidas verificables."

Prompt exacto sugerido (OpenClaw):

```text
Evalua esta skill con enfoque QA.
Devuelve:
- 3 casos donde SI debe activarse
- 3 casos donde NO debe activarse
- 3 mejoras concretas al SKILL.md (linea a cambiar + reemplazo propuesto)
```

---

## 5) Variantes de tiempo (60 vs 75)

Si solo tienes 60 min:

- Mantener A1, A2 y B2 obligatorios.
- En C3, mostrar solo estructura y primer bloque del SKILL.md.
- En D2, dejar instalada la skill pero sin segunda ronda de QA.

Si tienes 75 min:

- Agregar laboratorio de 8 min: cada estudiante define una skill de su stack.
- Cerrar con 2 revisiones cruzadas entre estudiantes (peer review rapido).

## 6) Checklist de preparacion (10 min antes)

- Confirmar que la CLI responde (`openclaw --help`).
- Confirmar acceso a workspace activo.
- Tener 2 prompts de respaldo copiados.
- Tener un `SKILL.md` base listo para copiar/pegar si falla internet.

## 7) Plan de contingencia

Si falla OpenClaw CLI:

- Continuar con simulacion local de `SKILL.md` y enfoque conceptual de activacion.
- Pedir a estudiantes validar calidad del archivo con checklist manual.

Si falla la red o autenticacion:

- Trabajar en modo offline: estructura de skill + casos de activacion/no activacion.
- Reagendar solo la parte de ejecucion de comandos de diagnostico.

Si el grupo va muy avanzado:

- Extender con comparativa de dos skills solapadas y resolver conflicto de alcance.

## 8) Cierre y preguntas de chequeo (5 min)

Que decir (literal):

"Hoy no solo aprendimos comandos. Aprendimos a pensar OpenClaw como sistema: arquitectura, privacidad, diagnostico y habilidades confiables."

Preguntas de chequeo final:

1. Que problema evita usar multiples workspaces?
2. En que canal tiene sentido cargar memoria sensible y por que?
3. Que diferencia practica hay entre `openclaw doctor` y `openclaw status --deep`?
4. Cual es la senal de que una skill esta mal definida desde su descripcion?
5. Que 4 preguntas debes responder antes de escribir un `SKILL.md`?

Actividad de salida (1 minuto):

- Cada estudiante escribe en una linea: "Skill que voy a construir esta semana + trigger principal".