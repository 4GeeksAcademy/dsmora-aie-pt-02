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

## Entradas esperadas

- `class_name`: formato `class_N`.
- `urls`: lista de URLs learn-pack (mínimo 1).
- `duration_target`: por defecto 60-75 min.
- `resume_file`: por defecto `resume_01.md`.

## Salidas esperadas

- Archivos JSON en `class_N/` nombrados por subdominio de cada URL.
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

### Paso 5: Control de calidad

Antes de finalizar, confirmar que el resumen contiene como mínimo:

- Objetivos de aprendizaje.
- Agenda con tiempos.
- Guion detallado por bloques.
- Ejemplos completos de comandos y prompts.
- Cierre con preguntas de chequeo.

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
