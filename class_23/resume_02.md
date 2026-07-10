# Guia Docente Taller: Class 23 - Skill de Orquestacion con Telegram + Composio

Clase online para 60-75 minutos.
Documento para profesor: enfoque practico para construir una skill real que reciba ordenes por Telegram y ejecute acciones en Google Docs y Google Calendar via Composio.

## 1) Objetivos de aprendizaje

Al finalizar, el estudiante podra:

- Diseñar una skill de OpenClaw para un flujo multi-herramienta (Telegram + Composio).
- Definir disparadores claros para evitar activaciones ambiguas.
- Estandarizar salida verificable en markdown y registro de acciones.
- Aplicar una estrategia minima de seguridad para credenciales y datos personales.
- Probar la skill con casos positivos y negativos de activacion.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y objetivo del caso real: 5 min
- Bloque A - Caso de uso y limites de la skill: 12 min
- Bloque B - Estructura de SKILL.md + contratos de entrada/salida: 14 min
- Bloque C - Construccion guiada de la propuesta: 18 min
- Bloque D - QA de activacion y hardening rapido: 11 min
- Cierre: 5 min

Extension a 75 min:

- Agregar 10 min para implementar una segunda variante de salida (resumen ejecutivo para coordinacion).

Version 60 min:

- Recortar 5 min del Bloque C (usar plantilla ya preparada).

## 3) Preparacion docente

Checklist tecnico:

- OpenClaw CLI funcionando.
- Workspace de clase disponible.
- Canal de Telegram bot activo para pruebas.
- Integraciones Composio listas para Google Docs y Google Calendar.

Comandos de verificacion:

```bash
openclaw doctor
openclaw status --deep
ls -la .github/skills
```

## 4) Guion docente detallado

## Apertura (5 min)

Que decir (literal):

"Hoy vamos a crear una skill util en operacion real: recibir una instruccion por Telegram, procesarla con reglas claras y producir acciones en Google Docs y Calendar via Composio."

"La meta no es automatizar por automatizar. La meta es tener un flujo auditable, repetible y seguro."

---

## Bloque A - Caso de uso y limites (12 min)

### A1. Caso de uso del bootcamp (6 min)

Que decir (literal):

"Caso: cada manana llega un mensaje por Telegram con pendientes del dia. El agente debe crear o actualizar una minuta en Google Docs y generar/actualizar eventos en Calendar."

"Si el mensaje no trae fecha o contexto suficiente, la skill no inventa: pide aclaracion."

Prompt exacto sugerido:

```text
Define alcance para una skill llamada telegram-academic-ops.
Devuelve solo:
1) Disparadores validos
2) Disparadores que NO deben activar
3) Datos minimos requeridos
4) Salida verificable
Contexto: bootcamp, seguimiento de clases y tutorias.
```

### A2. Limites funcionales (6 min)

Que decir (literal):

"Una skill robusta dice explicitamente lo que no hace. Eso evita errores de activacion y reduce costo de contexto."

"Nuestra skill no enviara mensajes masivos ni cambiara eventos historicos sin confirmacion."

---

## Bloque B - Estructura de SKILL.md y contratos (14 min)

### B1. Contrato de entrada (7 min)

Que decir (literal):

"Sin contrato de entrada no hay confiabilidad. Definimos campos minimos: tipo de accion, fecha, zona horaria, canal destino y prioridad."

Ejemplo de contrato minimo:

```text
accion: crear_evento | actualizar_doc | resumen_dia
fecha: YYYY-MM-DD
timezone: America/Bogota
titulo: string
detalles: string
audiencia: staff | estudiantes | ambos
```

### B2. Contrato de salida (7 min)

Que decir (literal):

"La salida debe poder auditarse en 20 segundos: que se hizo, donde, y que quedo pendiente."

Formato de salida esperado:

```text
resultado: ok | parcial | error
acciones_ejecutadas:
- docs: <doc_url_o_id>
- calendar: <event_id_o_n/a>
pendientes:
- <lista>
```

---

## Bloque C - Construccion guiada de la propuesta (18 min)

### C1. Crear skill propuesta en el repo (10 min)

Comandos exactos:

```bash
mkdir -p .github/skills/telegram-composio-academic-ops
cat > .github/skills/telegram-composio-academic-ops/SKILL.md << 'EOF'
---
name: telegram-composio-academic-ops
description: Orquesta operaciones academicas desde Telegram usando Composio para Google Docs y Google Calendar.
---

# Skill: telegram-composio-academic-ops

## Cuando usar
Usar cuando el usuario pida, desde Telegram o chat operativo, crear o actualizar minuta diaria, programar eventos academicos o generar resumen operativo del dia.

## No usar
- Solicitudes ambiguas sin fecha ni accion.
- Mensajes puramente conversacionales.
- Acciones masivas sin confirmacion explicita.

## Prerrequisitos
- Integracion de Telegram bot habilitada.
- Integracion Composio habilitada para Google Docs y Google Calendar.
- Zona horaria del workspace definida.

## Procedimiento
1. Identificar accion solicitada: crear_evento, actualizar_doc o resumen_dia.
2. Validar campos minimos (fecha, titulo, timezone).
3. Si faltan datos criticos, pedir aclaracion antes de ejecutar.
4. Si accion incluye documento:
   - Crear o actualizar minuta en Google Docs con formato estandar.
5. Si accion incluye calendario:
   - Crear o actualizar evento en Google Calendar con hora, titulo y descripcion.
6. Confirmar resultado con resumen auditable y pendientes.

## Salida esperada
Respuesta estructurada con estado, recursos afectados (doc/evento) y pendientes.

## Criterios de calidad
- No inventar fechas u horarios.
- No exponer credenciales ni tokens.
- Trazabilidad de cada accion ejecutada.
EOF

sed -n '1,240p' .github/skills/telegram-composio-academic-ops/SKILL.md
```

Que decir (literal):

"Si el alumno solo recuerda una idea de hoy, que sea esta: sin criterios de calidad la skill parece util, pero falla en produccion."

### C2. Prompt de prueba funcional (8 min)

Prompt exacto sugerido:

```text
Actua usando la skill telegram-composio-academic-ops.
Entrada:
- accion: crear_evento
- fecha: 2026-07-15
- timezone: America/Bogota
- titulo: Mentoria cohort 1690
- detalles: Revisar progreso de modulos 21 a 23 y bloquear riesgos.
- audiencia: estudiantes

Devuelve:
1) Validacion de entrada
2) Plan de ejecucion
3) Resultado estructurado
4) Mensaje final para Telegram (tono claro y breve)
```

---

## Bloque D - QA y hardening rapido (11 min)

### D1. Casos de activacion (6 min)

Que decir (literal):

"Evaluamos la skill como producto: donde activa bien, donde no debe activar, y como se comporta cuando faltan datos."

Prompt exacto sugerido:

```text
Evalua la skill telegram-composio-academic-ops.
Devuelve:
- 3 casos donde SI debe activarse
- 3 casos donde NO debe activarse
- 3 riesgos operativos
- 3 mejoras puntuales del SKILL.md
```

### D2. Hardening minimo (5 min)

Que decir (literal):

"No hay automatizacion segura sin reglas simples: principio de minimo privilegio, confirmacion en acciones sensibles y logs limpios sin secretos."

Checklist rapido:

- Confirmacion para acciones masivas.
- Bloqueo de ejecucion si falta fecha.
- Zona horaria obligatoria.
- Salida con trazabilidad y pendientes.

## 5) Cierre y chequeo (5 min)

Preguntas de chequeo:

1. Que diferencia hay entre una skill util y una skill confiable?
2. Que campos nunca deben faltar para Calendar?
3. Que condiciones obligan a pedir aclaracion antes de ejecutar?
4. Como verificas trazabilidad en la salida?

Actividad de salida:

- Cada estudiante define una variante de la skill para su flujo diario y lista 2 disparadores validos + 2 invalidos.