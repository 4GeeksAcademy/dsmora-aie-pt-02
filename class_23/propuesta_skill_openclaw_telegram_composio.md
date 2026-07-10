# Propuesta de Skill OpenClaw: Telegram + Composio (Google Docs y Calendar)

## 1) Objetivo

Definir una skill que permita al agente operar tareas academicas desde mensajes de Telegram, ejecutando acciones en Google Docs y Google Calendar via Composio, con trazabilidad y validacion de datos.

## 2) Nombre sugerido

- `telegram-composio-academic-ops`

## 3) Problema que resuelve

- Estandariza la operacion diaria de clases y mentorias.
- Evita respuestas ambiguas al exigir campos minimos.
- Reduce errores de calendario y notas dispersas.

## 4) Disparadores recomendados

Activar cuando el mensaje solicite alguna de estas intenciones:

- Crear o actualizar minuta diaria de clase.
- Programar o modificar evento academico.
- Generar resumen operativo del dia para staff/estudiantes.

No activar cuando:

- El mensaje sea conversacional sin accion operativa.
- Falten fecha y objetivo de la tarea.
- Se pidan acciones masivas sin confirmacion.

## 5) Contrato minimo de entrada

```text
accion: crear_evento | actualizar_doc | resumen_dia
fecha: YYYY-MM-DD
timezone: America/Bogota (o equivalente)
titulo: string
detalles: string
audiencia: staff | estudiantes | ambos
```

## 6) Contrato de salida

```text
resultado: ok | parcial | error
acciones_ejecutadas:
- docs: <doc_url_o_id>
- calendar: <event_id_o_n/a>
pendientes:
- <lista>
mensaje_telegram_final: <texto breve>
```

## 7) Borrador de SKILL.md

```markdown
---
name: telegram-composio-academic-ops
description: Orquesta operaciones academicas desde Telegram usando Composio para Google Docs y Google Calendar.
---

# Skill: telegram-composio-academic-ops

## Cuando usar
Usar cuando se solicite crear o actualizar minuta, crear/editar evento academico o generar resumen operativo diario.

## No usar
- Solicitudes ambiguas sin fecha.
- Conversacion informal sin accion.
- Acciones masivas sin confirmacion.

## Prerrequisitos
- Telegram bot habilitado.
- Composio conectado a Google Docs.
- Composio conectado a Google Calendar.
- Zona horaria del workspace definida.

## Procedimiento
1. Detectar intencion: crear_evento, actualizar_doc o resumen_dia.
2. Validar campos minimos de entrada.
3. Si faltan datos, pedir aclaracion antes de ejecutar.
4. Si corresponde Docs, crear o actualizar minuta estandar.
5. Si corresponde Calendar, crear o actualizar evento con horario valido.
6. Emitir salida estructurada con trazabilidad y pendientes.

## Salida esperada
Estado de ejecucion + recursos modificados + pendientes + mensaje final para Telegram.

## Criterios de calidad
- No inventar fecha ni hora.
- No exponer secretos o tokens.
- Registrar que accion se ejecuto y donde.
```

## 8) Riesgos y mitigaciones

- Riesgo: ambiguedad en fecha/hora.
  Mitigacion: bloqueo de ejecucion hasta confirmar datetime y timezone.

- Riesgo: sobre-escritura de documentos incorrectos.
  Mitigacion: confirmar doc_id cuando exista historial de minutas.

- Riesgo: ruido operativo en Telegram.
  Mitigacion: formato de respuesta corto, con estado y siguiente accion.

## 9) Siguiente iteracion sugerida

- Agregar modo `solo_borrador` para simular ejecucion sin escribir en Docs/Calendar.
- Agregar prioridad (`alta`, `media`, `baja`) para ordenar acciones del dia.
- Integrar plantilla fija de minuta con secciones: Objetivo, Acuerdos, Bloqueos, Proximos pasos.