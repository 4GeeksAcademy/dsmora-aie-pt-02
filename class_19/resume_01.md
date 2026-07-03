# Guia Docente Completa: Class 19 - IA Generativa, Agentes de Codigo y Comunicacion Estructurada

Clase online para 90 minutos.
Documento para profesor: incluye guion literal, agenda ampliada, laboratorio, prompts completos y criterios de evaluacion rapida.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Explicar que es IA generativa y como se diferencia del software determinista.
- Describir que es un LLM, como funciona a alto nivel, que papel juegan los tokens y por que una respuesta convincente no garantiza verdad.
- Reconocer limites practicos: sesgos, errores convincentes, falta de comprension real, costo y ventana de contexto.
- Trabajar con agentes de codigo en modo humano-en-el-bucle, evitando anti-patrones de copia ciega.
- Distinguir tipos de herramientas y modelos para elegir una opcion razonable segun contexto, costo y profundidad.
- Redactar prompts estructurados con Markdown para obtener respuestas mas precisas y faciles de verificar.
- Iterar con criterio: pedir, verificar, corregir, volver a pedir.

## 2) Agenda sugerida para 90 min

Ruta base de 90 minutos:

- Apertura y expectativas: 5 min
- Bloque A - IA generativa sin humo: 18 min
- Bloque B - LLMs, tokens y limites reales: 15 min
- Bloque C - Agentes de codigo y control humano: 18 min
- Bloque D - Herramientas y control de contexto en Copilot Chat: 10 min
- Bloque E - Hablar con IA usando formato estructurado: 18 min
- Laboratorio integrador y cierre: 6 min

Idea pedagogica de la sesion:

- Primero desmitizar la IA.
- Luego entender como responde.
- Despues usarla con control.
- Finalmente pedir mejor y validar mejor.

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- VS Code abierto con este repositorio.
- Terminal funcional en la raiz del proyecto.
- Acceso a un asistente AI (OpenClaw, Copilot Chat o ChatGPT) para demos en vivo.
- Archivo de notas para guardar prompts y respuestas de ejemplo.
- Tener listos 2 prompts: uno caotico y uno estructurado.

Comandos de verificacion previa:

```bash
cd /workspaces/dsmora-aie-pt-02
pwd
ls class_19
python3 --version
```

Verifica tambien que existan los contenidos base de la clase:

```bash
ls class_19/*.json
```

Comando de apoyo para ubicar el material durante la clase:

```bash
rg '"title"' class_19/*.json
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy no vamos a usar IA como magia. Vamos a usar IA como herramienta de ingenieria: entendiendo como responde, como se equivoca y como guiarla con estructura."

"La meta de hoy no es memorizar terminos; es salir con un flujo practico: pedir bien, validar, iterar y controlar calidad."

"Quiero que al final de esta clase puedan distinguir entre una respuesta que suena bien y una respuesta que realmente sirve."

Pregunta de arranque para el grupo:

- Cuando una IA te responde con seguridad, que te hace pensar que esta en lo correcto?

Usa 1 o 2 respuestas de estudiantes para abrir el tema de confianza vs verificacion.

## Bloque A - IA generativa sin humo (18 min)

### A1. Concepto rapido y diferencia con software tradicional (6 min)

Que decir (literal):

"La IA generativa no consulta una verdad absoluta. Predice el siguiente token probable segun patrones. Por eso puede sonar segura y aun asi estar equivocada."

"Software clasico: misma entrada, misma salida definida por reglas. LLM: misma entrada, salida probable con variacion."

"La creatividad y el error nacen del mismo mecanismo: prediccion probabilistica."

Puntos a remarcar:

- El software tradicional ejecuta instrucciones exactas.
- La IA generativa produce continuaciones plausibles.
- La variabilidad no es un bug: es parte del sistema.
- Cambios pequenos en el prompt pueden cambiar mucho la salida.

### A2. Demo guiada: variabilidad y precision del prompt (6 min)

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

### A3. Mini practica guiada (6 min)

Prompt exacto para estudiantes:

```text
Compara software tradicional vs IA generativa en una tabla de 4 filas: logica, repetibilidad, tipo de error y forma de validacion.
```

Pide que compartan una diferencia clave en voz alta.

Microcierre del bloque:

"Si entiendes que el modelo predice patrones y no consulta una verdad perfecta, dejas de tratar la IA como oraculo y empiezas a tratarla como sistema."

## Bloque B - LLMs, tokens y limites reales (15 min)

### B1. Que es un LLM y como se entrena a alto nivel (5 min)

Que decir (literal):

"Un LLM es un modelo entrenado con enormes cantidades de texto y codigo para predecir la siguiente pieza de lenguaje. No piensa como un humano. Reconoce patrones a gran escala."

"No guarda una base de datos perfecta de respuestas. Aprende regularidades: que suele venir despues de que."

Puntos a explicar:

- Entrada y salida son texto o tokens.
- El entrenamiento captura patrones frecuentes.
- Los datos de entrenamiento tambien transmiten sesgos y limitaciones.
- Son sistemas potentes, pero no tienen intencion, criterio moral ni comprension real.

### B2. Tokens, contexto y costo (5 min)

Que decir (literal):

"Token es la unidad de texto que procesa el modelo. Mas tokens significa mas costo y, muchas veces, mas ruido."

"Optimizar tokens no es escribir menos por escribir menos. Es escribir lo necesario con estructura clara."

Demo comparativa:

Prompt largo y confuso:

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

Comando rapido de apoyo:

```bash
cd /workspaces/dsmora-aie-pt-02
wc -c class_19/*.json
```

### B3. Limites que importan en clase y en trabajo real (5 min)

Que decir (literal):

"Una IA puede sonar inteligente porque produce lenguaje fluido. Pero fluidez no es lo mismo que comprension."

"No puede definir tus valores, no entiende el impacto real de una decision y no puede asumir tu responsabilidad profesional."

Lista de limites que el estudiante debe recordar:

- Puede inventar datos con tono convincente.
- Puede reproducir sesgos del entrenamiento.
- Puede perder detalles si el contexto es ambiguo o excesivo.
- Puede producir algo sintacticamente correcto pero conceptualmente equivocado.

Pregunta de chequeo:

- Si una respuesta parece excelente, cual es el siguiente paso antes de confiar en ella?

## Bloque C - Agentes de codigo y control humano (18 min)

### C1. Que es un agente de codigo y que puede hacer (6 min)

Que decir (literal):

"Un agente de codigo va mas alla del autocompletado. Puede leer contexto, proponer funciones, explicar codigo, sugerir pruebas y ayudarte a depurar."

"Eso no significa que piense por ti. Significa que acelera partes del trabajo si tu mantienes el control."

Diferencias utiles:

- Autocompletado: predice siguiente fragmento local.
- Agente: trabaja con tareas mas amplias y contexto mas rico.
- Humano: define objetivo, valida calidad, decide que aceptar.

### C2. Principio humano-en-el-bucle (6 min)

Que decir (literal):

"Regla de oro: humano en el bucle. Tu decides arquitectura, aceptas o rechazas cambios, y validas comportamiento."

"Tu rol no desaparece. Cambia: menos mecanografia, mas criterio."

Anti-patrones a remarcar:

- Copiar y pegar sin entender.
- Pedir cambios enormes en un solo prompt.
- No correr pruebas despues de generar codigo.
- Confundir velocidad con calidad.

Prompt exacto sugerido:

```text
Actua como reviewer de codigo. Dame una checklist de 6 pasos para validar cualquier snippet generado por IA antes de mergearlo.
Incluye: lectura linea por linea, casos borde, pruebas y riesgos de seguridad.
```

### C3. Ejemplo practico y micro-validacion (6 min)

Ejecuta:

```bash
cd /workspaces/dsmora-aie-pt-02
ls
rg --files class_19 | head
```

Que decir (literal):

"No necesito que el modelo tenga siempre razon. Necesito un proceso que capture cuando no la tiene."

Checklist en vivo:

- El estudiante puede explicar que hace cada bloque de codigo generado.
- El estudiante puede nombrar al menos 1 caso borde que romperia el snippet.
- El estudiante propone una prueba concreta para validar la salida.

## Bloque D - Herramientas y control de contexto en Copilot Chat (10 min)

### D1. Tipos de herramientas de agentes (3 min)

Que decir (literal):

"No todas las herramientas de IA se integran igual en tu flujo. Algunas viven dentro del editor, otras en navegador, otras son entornos completos."

Categorias a presentar:

- Extensiones de IDE.
- Agentes independientes.
- Herramientas en la nube.
- Asistentes integrados en plataformas de desarrollo.

Pregunta guia:

- Si necesito contexto de varios archivos y flujo continuo de programacion, me sirve mas un chat generico o una herramienta integrada al editor?

### D2. Como limitar contexto en Copilot Chat sin perder precision (4 min)

Que decir (literal):

"En Copilot Chat, mas contexto no siempre mejora la respuesta. Muchas veces la empeora. La habilidad importante es entregar solo el contexto que controla la decision."

Tecnicas concretas para mostrar en clase:

- Seleccionar solo el bloque de codigo relevante en el editor antes de preguntar.
- Pedir ayuda sobre el archivo activo en vez de describir todo el proyecto.
- Mencionar una funcion, componente o error puntual en lugar de "revisa todo".
- Pegar un fragmento pequeno con el error real en vez de logs completos.
- Abrir un chat nuevo cuando cambias de problema para evitar arrastrar contexto viejo.
- Pedir un formato de salida corto: lista, tabla o pasos maximos.

Que decir (literal):

"Si el modelo empieza a responder cosas que no pediste, muchas veces no falta inteligencia: sobra contexto."

### D3. Prompt para Copilot con contexto acotado (3 min)

Recomendacion docente:

- Para depurar: compartir solo error, funcion y comportamiento esperado.
- Para refactor: compartir una funcion y una restriccion clara.
- Para aprender: pedir explicacion sobre un bloque seleccionado, no sobre todo el archivo.
- Para iterar: una pregunta por cambio, no cinco objetivos juntos.

## Bloque E - Hablar con IA usando formato estructurado (18 min)

### E1. Estructura como pensamiento, no solo como formato (3 min)

Que decir (literal):

"Markdown no es decoracion. Es una manera de reducir ambiguedad y obligarte a pensar mejor antes de pedir."

"Si no puedes estructurar bien tu pedido, probablemente todavia no esta claro en tu cabeza."

### E2. Markdown para organizar y priorizar (4 min)

Prompt exacto sugerido:

```text
Reescribe este pedido en Markdown estructurado:
"necesito ayuda para mi proyecto final con timeline tareas riesgos y entregables"
Incluye secciones: Objetivo, Alcance, Tareas, Riesgos, Entregables.
```

Que decir (literal):

"Markdown no es solo para que se vea bonito. Es una jerarquia de ideas. Le dice al modelo que es principal, que es detalle y que es lista verificable."

### E3. Prompt flojo vs prompt mejorado (5 min)

Prompt flojo:

```text
Ayudame con el login de mi app.
```

Posible salida inesperada:

- Te propone rediseñar toda la autenticacion.
- Mezcla frontend, backend, UX y seguridad sin prioridad.
- Da consejos genericos imposibles de validar.

Prompt mejorado en Markdown:

```text
# Contexto
Tengo una app con frontend React y backend Node.

# Problema
El login falla de forma intermitente.

# Lo que necesito
- 3 hipotesis priorizadas
- 1 prueba concreta por hipotesis
- separar posibles causas de frontend y backend

# Restricciones
- no proponer reescritura completa
- no cambiar framework

# Formato de salida
Tabla con columnas: hipotesis, evidencia esperada, prueba.
```

Que decir (literal):

"Un mal prompt no siempre produce una mala respuesta. A veces produce una respuesta demasiado amplia, elegante y poco util. Eso tambien es un fallo."

### E4. Caso de salida inesperada y correccion guiada (4 min)

Prompt con ambiguedad:

```text
Explica este error y dime como arreglarlo rapido.
```

Caso para mostrar en clase:

- El modelo inventa una causa no presente en el error.
- Responde con seguridad aunque falte contexto.
- Sugiere pasos que no corresponden al stack real.

Mejora sugerida del prompt:

```text
# Error observado
Al enviar el formulario de login recibo 401 Unauthorized.

# Stack
- frontend React
- backend Node/Express

# Quiero que hagas
- explica 2 causas plausibles
- indica que evidencia buscar en frontend y backend
- no inventes causas que no se puedan inferir del error

# Responde en
Lista numerada de maximo 5 puntos.
```

Que decir (literal):

"Cuando una salida es inesperada, no siempre corriges la respuesta: corriges el prompt y el contexto."

### E5. Elegir el formato correcto e iterar (3 min)

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

Regla practica para el grupo:

- Si el problema es ambiguo, primero estructura contexto.
- Si la respuesta se desordena, reduce alcance.
- Si la salida inventa cosas, agrega restricciones explicitas.
- Si la respuesta sigue siendo amplia, pide menos tareas por turno.

## 5) Laboratorio integrador (6 min)

Objetivo:

- Pasar de un prompt caotico a un prompt en Markdown, mas acotado y validable.

Caso de trabajo:

```text
Necesito ayuda con mi app porque falla el login y no se si es frontend o backend y tambien quiero mejorar la experiencia del usuario y agregar tests.
```

Instruccion para estudiantes:

- Reescribir el pedido en formato Markdown con secciones.
- Limitar el contexto a lo necesario para diagnosticar el problema.
- Agregar al menos 2 restricciones y 2 criterios de verificacion.

Version esperada orientativa:

```text
Contexto: app web con frontend React y API Node.
Problema: el login falla de forma intermitente.
Objetivo: identificar 3 hipotesis priorizadas.
Restricciones:
- no cambiar framework
- no proponer reescritura total
Salida: tabla con hipotesis, evidencia, prueba.
Criterios de verificacion:
- cada hipotesis debe incluir una prueba ejecutable
- la salida debe distinguir frontend vs backend
```

## 6) Cierre (6 min)

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
- Puedo nombrar al menos 2 limites reales de un LLM.
- Puedo usar humano-en-el-bucle en cualquier tarea con agente.
- Puedo usar Markdown para estructurar un pedido ambiguo.
- Puedo reducir contexto en Copilot Chat para obtener respuestas mas utiles.
- Puedo transformar un prompt caotico en uno estructurado y verificable.

## 7) Preguntas de chequeo rapidas

- Por que una respuesta fluida de IA no garantiza que sea correcta?
- Que cambia en tu trabajo cuando usas humano-en-el-bucle?
- Que problema resuelven los tokens y la ventana de contexto en tu forma de pedir?
- Que senales te muestran que en Copilot Chat metiste demasiado contexto?
- Que partes del contexto quitarias primero si la respuesta se volvio demasiado amplia?
- Como decides si debes iterar el prompt o empezar de nuevo?
- Que riesgos aparecen si aceptas codigo generado sin leerlo linea por linea?
- Como mejoras un prompt cuando la salida fue inesperada pero no totalmente inutil?

## 8) Evidencias de aprendizaje observables

- El estudiante deja de describir la IA como "sistema que sabe" y empieza a describirla como sistema probabilistico.
- El estudiante formula prompts con objetivo, contexto, restricciones y formato de salida.
- El estudiante recorta contexto innecesario al trabajar en Copilot Chat.
- El estudiante pide validacion o pruebas en vez de aceptar la primera respuesta.
- El estudiante puede justificar por que agrego o quito contexto en un prompt.

## 9) Riesgos comunes y refuerzo recomendado

- Riesgo: creer que "si suena bien, esta bien".
  Refuerzo: pedir siempre evidencia, prueba o criterio de verificacion.
- Riesgo: prompts demasiado amplios y ambiguos.
  Refuerzo: dividir en una sola tarea por iteracion.
- Riesgo: pedir codigo sin entender arquitectura.
  Refuerzo: obligar explicacion previa de la solucion.
- Riesgo: copiar y pegar sin probar.
  Refuerzo: checklist minima de lectura, caso borde y prueba.
- Riesgo: elegir formato por costumbre y no por necesidad.
  Refuerzo: usar Markdown como formato base y priorizar claridad antes que sofisticacion.

## 10) Distribucion final de tiempo

- Apertura: 5 min
- Bloque A: 18 min
- Bloque B: 15 min
- Bloque C: 18 min
- Bloque D: 10 min
- Bloque E: 18 min
- Laboratorio integrador y cierre: 6 min

Total: 90 min

## 11) Plan de contingencia

Si falla la demo principal con el asistente AI:

```bash
cd /workspaces/dsmora-aie-pt-02
cat class_19/introduction_to_generative_ai.json | head -n 40
cat class_19/using_coding_agents.json | head -n 40
```

Usa esos fragmentos para hacer analisis manual guiado de prompts, limites y calidad de salida.

Si falla internet o login a herramienta externa:

- Ejecuta la clase en modo simulacion: el profesor lee prompt y respuesta preparada.
- Mueve el foco a evaluacion critica de respuestas: deteccion de ambiguedad, sesgo y riesgo.
- Cierra con ejercicio en parejas: reescritura de prompt + eleccion de formato + rubrica de validacion.

