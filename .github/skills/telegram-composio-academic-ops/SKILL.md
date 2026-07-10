---
name: telegram-composio-academic-ops
description: Orquesta operaciones academicas desde Telegram usando Composio para Google Docs y Google Calendar.
---

# Skill: telegram-composio-academic-ops

## Cuando usar
Usar cuando se solicite crear o actualizar minuta, crear o editar evento academico, o generar resumen operativo diario.

## No usar
- Solicitudes ambiguas sin fecha ni objetivo.
- Conversacion informal sin accion operativa.
- Acciones masivas sin confirmacion explicita.

## Prerrequisitos
- Telegram bot habilitado.
- Composio conectado a Google Docs.
- Composio conectado a Google Calendar.
- Zona horaria del workspace definida.

## Entradas minimas esperadas
- accion: crear_evento | actualizar_doc | resumen_dia
- fecha: YYYY-MM-DD
- timezone: string valida
- titulo: string
- detalles: string
- audiencia: staff | estudiantes | ambos

## Procedimiento
1. Detectar intencion de la solicitud y mapearla a una accion valida.
2. Validar campos minimos de entrada antes de ejecutar herramientas.
3. Si faltan datos criticos (fecha/hora/timezone), pedir aclaracion.
4. Si aplica Docs, crear o actualizar minuta con formato estandar.
5. Si aplica Calendar, crear o actualizar evento con horario valido.
6. Responder con salida estructurada y trazabilidad de acciones.

## Salida esperada
- resultado: ok | parcial | error
- acciones_ejecutadas: recursos afectados en Docs/Calendar
- pendientes: lista de faltantes o confirmaciones requeridas
- mensaje_telegram_final: texto breve para el canal

## Criterios de calidad
- No inventar fechas ni horarios.
- No exponer tokens ni credenciales.
- Mantener trazabilidad de cada accion ejecutada.
- Confirmar antes de acciones potencialmente destructivas.
