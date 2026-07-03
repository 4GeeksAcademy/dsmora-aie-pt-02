# Guia Docente Completa: Class 19 - Fundamentos de IA Generativa, Agentes de Codigo y Comunicacion Estructurada

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos para ejecutar demos en vivo.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Explicar que es IA generativa y como se diferencia del software determinista.
- Describir el rol de los LLMs, tokens y limites practicos (errores convincentes, sesgos, costo).
- Trabajar con agentes de codigo en modo humano-en-el-bucle, evitando anti-patrones de copia ciega.
- Redactar prompts estructurados con Markdown, JSON y YAML para obtener respuestas mas precisas.
- Iterar con criterio: pedir, verificar, corregir, volver a pedir.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y contexto: 5 min
- Bloque A - IA generativa sin humo: 12 min
- Bloque B - Agentes de codigo y control humano: 15 min
- Bloque C - Tokens, costo y calidad de salida: 12 min
- Bloque D - Hablar con IA usando formato estructurado: 16 min
- Cierre + checklist + Q&A: 5 min

Si tienes 75 min:

- Agrega 10 min de laboratorio: cada estudiante transforma un prompt caotico en uno estructurado y compara resultados.

Si tienes 60 min:

- Recorta Bloque C a 7 min (solo concepto + una demo rapida) y deja optimizacion avanzada de tokens como lectura posterior.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- VS Code abierto con este repositorio.
- Terminal funcional en la raiz del proyecto.
- Acceso a un asistente AI (OpenClaw, Copilot Chat o ChatGPT) para demos en vivo.
- Archivo de notas para guardar prompts y respuestas de ejemplo.

Comandos de verificacion previa:

```bash
cd /workspaces/dsmora-aie-pt-02
pwd
ls class_19
python3 --version
```

Verifica tambien que existan los 4 contenidos base de la clase:

```bash
ls class_19/*.json
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy no vamos a usar IA como magia. Vamos a usar IA como herramienta de ingenieria: entendiendo como responde, como se equivoca y como guiarla con estructura."

"La meta de hoy no es memorizar terminos; es salir con un flujo practico: pedir bien, validar, iterar y controlar calidad."

## Bloque A - IA generativa sin humo (12 min)

### A1. Concepto rapido (4 min)

Que decir (literal):

"La IA generativa no consulta una verdad absoluta. Predice el siguiente token probable segun patrones. Por eso puede sonar segura y aun asi estar equivocada."

"Software clasico: misma entrada, misma salida definida por reglas. LLM: misma entrada, salida probable con variacion."

### A2. Demo guiada: variabilidad y precision del prompt (4 min)

Prompt exacto sugerido:

```text
Explica en 3 lineas que es IA generativa para una persona sin perfil tecnico.
```

Luego pide variacion controlada:

```text
Repite la explicacion anterior, pero ahora en formato de analogia de cocina y maximo 40 palabras.
```

Que decir (literal):

"Mismo tema, distinta salida, porque cambie el contexto y la restriccion. La calidad del prompt determina la utilidad de la respuesta."

### A3. Mini practica guiada (4 min)

Prompt exacto para estudiantes:

```text
Compara software tradicional vs IA generativa en una tabla de 4 filas: logica, repetibilidad, tipo de error y forma de validacion.
```

Pide que compartan una diferencia clave en voz alta.

## Bloque B - Agentes de codigo y control humano (15 min)

### B1. Concepto y riesgos (5 min)

Que decir (literal):

"Un agente de codigo acelera implementacion, no reemplaza criterio. Si copias y pegas sin leer, conviertes velocidad en deuda tecnica."

"Regla de oro: humano en el bucle. Tu decides arquitectura, aceptas o rechazas cambios, y validas comportamiento."

Anti-patrones a remarcar:

- Copiar y pegar sin entender.
- Pedir cambios enormes en un solo prompt.
- No correr pruebas despues de generar codigo.

### B2. Ejemplo practico (5 min)

Ejecuta (sobre el repo, como ejemplo de inspeccion minima):

```bash
cd /workspaces/dsmora-aie-pt-02
ls
rg --files class_19 | head
```

Prompt exacto sugerido:

```text
Actua como reviewer de codigo. Dame una checklist de 6 pasos para validar cualquier snippet generado por IA antes de mergearlo.
Incluye: lectura linea por linea, casos borde, pruebas y riesgos de seguridad.
```

Que decir (literal):

"No necesito que el modelo tenga siempre razon. Necesito un proceso que capture cuando no la tiene."

### B3. Validacion (5 min)

Checklist en vivo:

- El estudiante puede explicar que hace cada bloque de codigo generado.
- El estudiante puede nombrar al menos 1 caso borde que romperia el snippet.
- El estudiante propone una prueba concreta para validar la salida.

## Bloque C - Tokens, costo y calidad de salida (12 min)

### C1. Explicacion corta (4 min)

Que decir (literal):

"Token es la unidad de texto que procesa el modelo. Mas tokens significa mas costo y, muchas veces, mas ruido."

"Optimizar tokens no es escribir menos por escribir menos. Es escribir lo necesario con estructura clara."

### C2. Demo comparativa (4 min)

Prompt largo y confuso (muestra ejemplo de mala practica):

```text
Hola, necesito ayuda con varias cosas de mi app, no se bien por donde empezar, tengo backend y frontend, tambien errores, tambien quisiera tests, y ademas mejorar rendimiento y seguridad, y no se si usar React o Next, dame algo.
```

Prompt optimizado:

```text
Contexto: app web con frontend React y API Node.
Objetivo: reducir errores en login.
Tarea: propone 3 hipotesis de falla y 1 prueba por hipotesis.
Formato de salida: tabla con columnas (hipotesis, evidencia esperada, prueba).
```

Que decir (literal):

"Segundo prompt: menos ambiguo, mejor contexto, salida validable. Eso mejora calidad y reduce vueltas inutiles."

### C3. Comando rapido de apoyo (4 min)

```bash
cd /workspaces/dsmora-aie-pt-02
wc -c class_19/*.json
```

Que decir (literal):

"No medimos tokens exactos con este comando, pero si vemos magnitud de contexto. Mas texto no siempre significa mejor respuesta."

## Bloque D - Hablar con IA usando formato estructurado (16 min)

### D1. Markdown para pensar y pedir (4 min)

Prompt exacto sugerido:

```text
Reescribe este pedido en Markdown estructurado:
"necesito ayuda para mi proyecto final con timeline tareas riesgos y entregables"
Incluye secciones: Objetivo, Alcance, Tareas, Riesgos, Entregables.
```

Que decir (literal):

"Markdown no es decoracion. Es una forma de ordenar pensamiento para que el modelo entienda prioridad y relacion entre partes."

### D2. JSON para salida verificable (4 min)

Prompt exacto sugerido:

```text
Devuelve SOLO JSON valido con esta estructura:
{
  "feature": "login",
  "acceptance_criteria": ["..."],
  "test_cases": [{"name":"...","input":"...","expected":"..."}]
}
Tema: autenticacion con email y password.
```

Que decir (literal):

"Cuando quiero parsear o automatizar, pido JSON estricto. Si no valida, no pasa."

### D3. YAML para configuracion legible (4 min)

Prompt exacto sugerido:

```text
Genera un ejemplo minimo de configuracion YAML para un proyecto de aprendizaje:
- entorno: dev
- lenguaje: javascript
- reglas: usar eslint y pruebas basicas
Incluye comentarios breves en YAML.
```

### D4. Cierre de bloque con iteracion (4 min)

Prompt exacto sugerido:

```text
Ahora mejora tu respuesta anterior aplicando estos criterios:
1) menos ambiguedad
2) pasos accionables
3) salida facil de verificar
Devuelve primero "Cambios aplicados:" y luego la version final.
```

Que decir (literal):

"La habilidad clave no es pedir una vez. Es iterar con criterio hasta que la salida sea util y verificable."

## 5) Cierre (5 min)

Que decir (literal):

"Si hoy te llevas una sola idea, que sea esta: IA sin criterio te da velocidad fragil; IA con estructura te da velocidad confiable."

"Tu ventaja profesional no es competir contra el modelo. Es saber dirigirlo, evaluarlo y mejorarlo en ciclos cortos."

Checklist final en vivo:

```bash
cd /workspaces/dsmora-aie-pt-02
ls class_19
```

Checklist conceptual final:

- Puedo explicar diferencia entre prediccion y comprension.
- Puedo usar humano-en-el-bucle en cualquier tarea con agente.
- Puedo transformar un prompt caotico en formato estructurado.

## 6) Preguntas de chequeo rapidas

- Por que una respuesta fluida de IA no garantiza que sea correcta?
- Que cambia en tu trabajo cuando usas humano-en-el-bucle?
- Cuando elegirias JSON en lugar de Markdown?
- Que haria primero si el codigo generado funciona pero no lo entiendo?
- Como decides si debes iterar el prompt o empezar de nuevo?

## 7) Plan de contingencia

Si falla la demo principal con el asistente AI:

```bash
cd /workspaces/dsmora-aie-pt-02
cat class_19/introduction_to_generative_ai.json | head -n 40
cat class_19/using_coding_agents.json | head -n 40
```

Usa esos fragmentos para hacer analisis manual guiado de prompts y calidad de salida.

Si falla internet o login a herramienta externa:

- Ejecuta la clase en modo simulacion: el profesor lee prompt y respuesta preparada.
- Mueve el foco a evaluacion critica de respuestas (deteccion de ambiguedad y riesgos).
- Cierra con ejercicio en parejas: reescritura de prompt + rubrica de validacion.
