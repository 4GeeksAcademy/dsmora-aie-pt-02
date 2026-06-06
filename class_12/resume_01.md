# Guia Docente: AI Communication Strategies - Mastering Context

Este documento adapta el modulo de comunicacion con IA para una clase online.
El foco es que el estudiante deje de escribir prompts improvisados,
aprenda ingenieria de contexto y optimice costo/claridad de cada solicitud.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Diferenciar una instruccion vaga de una instruccion estructurada.
  Como explicarlo: comparar en vivo dos prompts para la misma tarea y medir calidad de salida.
- Aplicar ingenieria de contexto para reducir ambiguedad.
  Como explicarlo: construir un bloque con rol, tarea, criterios, entradas y formato esperado.
- Reconocer ruido vs senal en prompts largos.
  Como explicarlo: depurar un prompt excesivo hasta dejar solo informacion accionable.
- Reescribir instrucciones para mejorar precision y costo de tokens.
  Como explicarlo: iterar sobre una misma consigna en 2-3 versiones y comparar resultados.
- Validar calidad de un prompt con checklist minimo.
  Como explicarlo: revisar cobertura de contexto, restricciones y objetivo de salida.

## 2. Mapa del modulo (10 lecciones)

1. 0 Hablando con ia como un profesional
2. 1 La brecha entre lo que pides y lo que obtienes
3. 1.1 Instrucciones estructuradas vs no estructuradas comparacion
4. 2 Que es la ingenieria de contexto
5. 2.1 Construyendo un contexto rico para ia
6. 2.2 Ingenieria de contexto en la practica
7. 3 El costo de palabras tokens ruido y senal
8. 3.1 Reescribiendo instrucciones excesivas para claridad
9. 4 Desafio completo de construccion de instrucciones
10. 4.1 Verificacion de conocimiento contexto y eficiencia

## 3. Guion sugerido para clase online (35 minutos)

### Bloque A (8 min): De usuario casual a comunicador profesional

- Que cambia cuando se conversa con IA con criterio de trabajo.
  Como explicarlo: presentar errores tipicos de prompts vagos y su impacto en salida.
- La brecha entre intencion y resultado.
  Como explicarlo: mostrar que el problema suele estar en la instruccion, no en el modelo.

### Bloque B (10 min): Ingenieria de contexto

- Definir el contexto minimo viable.
  Como explicarlo: usar plantilla con rol, objetivo, entradas, restricciones y formato.
- Construccion de contexto rico.
  Como explicarlo: agregar ejemplos, alcance y criterios de calidad sin sobrecargar.

### Bloque C (9 min): Ruido, senal y costo de tokens

- Coste de palabras innecesarias.
  Como explicarlo: tomar un prompt largo, medir redundancia y reducirlo por etapas.
- Reescritura para claridad.
  Como explicarlo: priorizar verbos de accion, orden de tareas y salida verificable.

### Bloque D (8 min): Desafio y verificacion

- Desafio de construccion de instrucciones.
  Como explicarlo: cada estudiante redacta prompt para un caso real de trabajo.
- Verificacion de conocimiento.
  Como explicarlo: usar checklist final para evaluar eficacia del prompt antes de ejecutarlo.

## 4. Ejemplos para mostrar en vivo

### Ejemplo 1: Prompt vago vs prompt estructurado

```text
Prompt vago:
"Hazme un resumen de esto"

Prompt estructurado:
"Actua como tutor tecnico. Resume el texto en 5 bullets.
Incluye: idea central, 2 riesgos, 2 acciones recomendadas.
Formato de salida: markdown con titulos cortos. Maximo 120 palabras."
```

### Ejemplo 2: Contexto minimo viable

```text
Rol: Mentor de producto
Objetivo: Priorizar backlog de sprint
Entradas: lista de 12 tickets con impacto/esfuerzo
Restricciones: no cambiar alcance del sprint
Salida esperada: tabla con prioridad, razon y riesgo
```

### Ejemplo 3: Reduccion de ruido de tokens

```text
Version larga: "Necesito que por favor, si puedes, me ayudes a..."
Version optimizada: "Prioriza estos 6 tickets por impacto y esfuerzo.
Devuelve top 3 con razon de negocio en 1 linea por ticket."
```

## 5. Errores frecuentes y correccion

- Error: pedir "hazlo mejor" sin contexto de objetivo.
  Correccion: explicitar audiencia, exito esperado y restricciones de entrega.
- Error: mezclar multiples tareas en una sola frase larga.
  Correccion: separar en pasos numerados con prioridad y formato de salida.
- Error: incluir demasiado contexto irrelevante.
  Correccion: filtrar a datos que cambian decisiones del modelo.
- Error: no definir criterio de validacion.
  Correccion: cerrar prompt con condiciones comprobables de calidad.

## 6. Cierre para sesion

- Mensaje clave: un buen prompt es una especificacion breve y verificable.
- Resultado esperado: estudiante capaz de disenar instrucciones claras, eficientes y repetibles.
- Siguiente paso: traducir una referencia visual a especificacion tecnica para IA (resume_02).
