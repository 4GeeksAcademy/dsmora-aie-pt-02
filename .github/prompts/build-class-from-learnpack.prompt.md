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
3. Lee el contenido de los JSON y extrae hechos, temas, librerías, ejemplos y comandos reales. No inventes contenido.
4. Si un ejemplo o librería no aparece en los JSON, no lo añadas. Si no hay ejemplo concreto, omítelo o deja una explicación conceptual muy breve.
5. Redacta `{{class_name}}/resume_01.md` como resumen para profesor, de 60-75 minutos, y asegúrate de incluir:
- objetivo de la clase,
- desarrollo de la clase,
- ejemplo de código basado en el JSON cuando exista,
- qué decir en clase,
- qué preguntar después,
- cierre sugerido,
- y, si aplica, comandos exactos y prompts de demo.
6. Antes de terminar, comprueba que cada afirmación del resumen esté respaldada por los JSON. Si no lo está, elimínala.
7. Entrega una salida breve indicando archivos creados/actualizados.
