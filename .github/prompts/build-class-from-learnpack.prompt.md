---
mode: agent
description: "Genera class_N desde URLs de learn-pack: ejecuta scraper y crea resumen docente 60-75 min con guion literal + comandos + prompts exactos."
---

Objetivo

Crear una clase completa desde URLs de learn-pack siguiendo el flujo institucional.

Entradas

- class_name: {{class_name}}
- urls_csv: {{urls_csv}}
- duration_target: {{duration_target}}

Instrucciones

1. Ejecuta scraping con:

```bash
python3 scripts/scraper.py --target "{{class_name}}:{{urls_csv}}"
```

2. Verifica que en `{{class_name}}/` existan JSON nuevos.
3. Lee el contenido de los JSON y redacta `{{class_name}}/resume_01.md`.
4. El resumen debe ser para profesor, durar entre 60-75 minutos y contener:
- agenda por tiempos,
- guion literal de qué decir,
- comandos exactos a ejecutar,
- prompts exactos para demos,
- variantes para versión 60 min y 75 min,
- checklist de preparación,
- plan de contingencia.
5. Entrega una salida breve indicando archivos creados/actualizados.
