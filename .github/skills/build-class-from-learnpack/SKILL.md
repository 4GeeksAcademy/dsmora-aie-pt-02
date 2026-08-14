---
name: build-class-from-learnpack
description: "Crear class_N desde URLs de learn-pack: ejecutar scripts/scraper.py, generar JSON en class_N y redactar resumen docente 60-75 min con guion literal, comandos exactos y prompts completos para profesor. Usar cuando el usuario pida crear una nueva clase desde URLs y no quiera repetir instrucciones de formato."
---

# Build Class From LearnPack

## Propósito

Automatizar este flujo completo en una sola ejecución:

1. Recibir una clase destino (por ejemplo `class_18`) y una lista de URLs de `*.learn-pack.com`.
2. Ejecutar scraping con `scripts/scraper.py` para generar JSON de contenidos.
3. Crear o actualizar `resume_01.md` en la carpeta de la clase.
4. Entregar un resumen docente orientado a clase de 60-75 minutos con:
- Guion literal de qué decir.
- Comandos exactos a ejecutar.
- Prompts exactos para demos.
- Bloques opcionales para recortar (60) o extender (75).

## Reglas de calidad obligatorias

Antes de redactar cualquier resumen o ejemplo:

- La única fuente de verdad es el contenido de los JSON generados por el scraper.
- No usar teoría, ejemplos, definiciones, comparaciones, comandos ni fuentes externas al propio JSON de la clase, salvo que el usuario lo pida explícitamente.
- No reutilizar contenido teórico de otras clases, memorias, README, documentación externa o conocimiento general del modelo.
- Sí se permite reorganizar el material en formato docente y añadir estructura pedagógica como agenda, bloques, tiempos, checklist, preguntas de chequeo y cierres, siempre que esa estructura no introduzca teoría nueva.
- No inventar librerías, frameworks, comandos, ejemplos, prompts ni explicaciones que no aparezcan en los JSON.
- Si el JSON contiene un ejemplo de código, reutilizarlo o parafrasearlo conservadoramente.
- Si el JSON no contiene un ejemplo concreto, no inventarlo: se debe omitir el ejemplo o dejarlo como una idea conceptual muy general.
- Cada afirmación del resumen debe estar respaldada por el contenido del JSON. Si no lo está, debe eliminarse.
- El resumen debe ser útil para enseñar en clase y debe incluir: objetivo, desarrollo de la clase, ejemplo de código validado por el JSON, qué decir en clase, qué preguntar después y cierre sugerido.

### Regla de trazabilidad obligatoria

- Si el usuario pregunta si "se inventó algo", interpretar eso como contenido teórico o fuentes, no como formato docente.
- La respuesta correcta debe distinguir explícitamente entre estructura pedagógica añadida por el agente y contenido teórico, que debe salir solo de los JSON.
- En caso de duda, sacrificar riqueza pedagógica antes que introducir teoría no respaldada por el JSON.

## Entradas esperadas

- `class_name`: formato `class_N`.
- `urls`: lista de URLs learn-pack (mínimo 1).
- `project_urls` (opcional): lista de URLs de proyecto onepage de Learn (por ejemplo rutas `/project/...`).
- `duration_target`: por defecto 60-75 min.
- `resume_file`: por defecto `resume_01.md`.

## Salidas esperadas

- Archivos JSON en `class_N/` nombrados por subdominio de cada URL.
- Si hay proyecto: archivo fuente del proyecto en `class_N/` (JSON o Markdown) con contenido extraido del onepage.
- Archivo `class_N/resume_01.md` con guía docente completa.

## Flujo operativo

### Paso 1: Validación mínima

- Confirmar que `scripts/scraper.py` existe.
- Confirmar que `class_name` cumple `^class_\d+$`.
- Confirmar que todas las URLs contienen `learn-pack.com`.

Si la clase no existe, crear carpeta automáticamente.

### Paso 2: Scraping

Ejecutar:

```bash
python3 scripts/scraper.py --target "class_N:url1,url2,url3"
```

Notas:

- Mantener `--max-concurrency` por defecto salvo que el usuario pida cambiarlo.
- Si hay tokens en URL, mantenerlos intactos.

### Paso 2.5: Proyectos onepage (opcional)

Si el usuario incluye `project_urls`, procesar cada proyecto asi:

1. Intentar extraer contenido visible desde el selector `#main-container` (onepage, sin navegacion por cards).
2. Si el render falla (por ejemplo `Application error`), usar fallback por API de BreatheCode:
	- Resolver `slug` del proyecto desde la URL.
	- Consultar `https://breathecode.herokuapp.com/v1/registry/asset/<slug>` (o variante `-es` si aplica).
	- Tomar `readme_url` y descargar el README (idealmente idioma del usuario).
3. Guardar evidencia en `class_N/` con nombre estable, por ejemplo:
	- `<project_slug>_project_asset.json`
	- `<project_slug>_project_README.es.md`

Reglas:

- Tratar el proyecto como fuente adicional de verdad, con la misma restriccion: no inventar contenido fuera de lo extraido.
- Si no se logra extraer contenido util, declarar la limitacion explicitamente en el resumen y no inventar requisitos.

### Paso 3: Verificación de salida

- Listar `class_N/`.
- Verificar que existe al menos 1 JSON nuevo.
- Leer muestras de contenido para construir temario real.

### Paso 4: Construcción del resumen docente

Generar `class_N/resume_01.md` con estos requisitos estrictos:

1. Enfoque para profesor, no para alumno.
2. Duración total 60-75 minutos.
3. Incluir frases literales de explicación (`Qué decir (literal)`).
4. Incluir comandos shell exactos en bloques `bash`.
5. Incluir prompts exactos para OpenClaw en bloques `text`.
6. Distribuir tiempos por bloque pensando en tiempo de explicación, no en tiempo de tipeo.
7. Incluir variantes de recorte (60) y extensión (75).
8. Incluir checklist de preparación y plan de contingencia.
9. Si hay proyecto, agregar bloque especifico con:
	- Resumen de requisitos del proyecto.
	- Como hilar el proyecto con los modulos/lecciones previos.
	- Ejemplos en lenguaje natural alineados al brief del proyecto.
	- Mini plan en pseudocodigo para ejecutar el proyecto paso a paso.

### Paso 5: Control de calidad

Antes de finalizar, confirmar que el resumen contiene como mínimo:

- Objetivos de aprendizaje.
- Agenda con tiempos.
- Guion detallado por bloques.
- Ejemplos completos de comandos y prompts.
- Cierre con preguntas de chequeo.

Si existe proyecto, validar ademas:

- El bloque de proyecto no contradice el brief original.
- Las tareas/criterios de evaluacion del proyecto aparecen resumidos.
- El mini plan en pseudocodigo refleja el flujo real (setup, consultas, validacion, informe/entrega).

## Estilo de redacción requerido

- Español claro, accionable y orientado a docencia en vivo.
- Priorizar secuencia demostrable en clase.
- Evitar teoría abstracta sin demo.
- Permitir que el profesor omita bloques sin romper la narrativa.

## Plantilla

Usar como base el archivo de apoyo:

- `teacher_summary_template.md`

Adaptar la plantilla a los temas reales extraídos de los JSON generados.

## Criterios de éxito

Se considera completado cuando:

- El scraping terminó sin errores.
- Existen JSON en `class_N/` para las URLs dadas.
- Existe `class_N/resume_01.md` cumpliendo formato docente 60-75 min.
- El resultado final es utilizable directamente por el profesor para impartir la clase.
