# Class 54: Usar modelos de predicción

⏰ Duración: 1 día (esta guía propone un debate de unos 50 minutos y una práctica de integración que puede ocupar el resto de la jornada).

Los estudiantes cubren fundamentos de ML—datasets, targets, features, aprendizaje supervisado vs no supervisado—y cuándo las redes neuronales aportan valor real. Practican el flujo de ocho pasos, distinguen clasificación de regresión e integran modelos preentrenados validando con muestras reales. La evaluación prioriza el encuadre del problema y la evidencia por encima del nombre del algoritmo.

Esta guía complementa a `resume_01.md`: mientras esa guía es el guion docente minuto a minuto, esta es el guion de un debate socrático sobre el mismo temario, usando como caso concreto el proyecto WeLoveReviews (análisis de sentimiento sobre 500 reseñas con `nlptown/bert-base-multilingual-uncased-sentiment`) que ya se trabajó en la clase.

Los splits train/validation/test, el baseline de clase mayoritaria, la monitorización operativa y la code review que aparecen como preguntas de debate son ampliaciones pedagógicas para razonar sobre una integración profesional; no son entregables adicionales exigidos por el brief del proyecto. El entregable concreto sigue siendo el descrito en `resume_01.md` y en `ai-eng-sentiment-analysis-reviews_project_README.es.md`.

**Checkpoint de la clase:** cada estudiante puede explicar qué tipo de modelo encaja con la pregunta de negocio y demostrar el modelo descargado generando predicciones sobre una muestra del proyecto WeLoveReviews. La muestra sirve para validar la integración; no sustituye el análisis completo de las 500 reseñas.

### Ritmo del debate

1. Apertura → Aprender (vocabulario ML + encuadre supervisado) → Reflexionar (trade-offs de redes neuronales) → Tener en cuenta (desajuste de dominio, métricas) → Hacer (flujo de selección de modelos) → Evitar (antipatrones) → Cierre
2. **Imprescindible:** aprendizaje supervisado definido por datos etiquetados, no por el nombre del algoritmo; el proceso de ocho pasos frente a "elegir un algoritmo"; elegir y validar modelos preentrenados antes de integrarlos
3. **Si hay tiempo:** contrastar clasificación y regresión con un escenario concreto cada una
4. **Tiempo orientativo:** ~50 min de debate + práctica de integración

### Criterios de participación

- Aporta ejemplos concretos que conecten conceptos del syllabus (dataset, target, etiquetas) con un escenario de predicción real
- Cuestiona la elección de modelo de un compañero con evidencia (forma de los datos, tipo de problema), no solo con métricas de popularidad
- Articula al menos un modo de fallo y cómo lo detectaría antes de desplegar

### Debate

#### Apertura — impacto profesional

1. Un producto despliega un modelo de predicción que brilló en la demo y luego cae la confianza del cliente. ¿Qué decisión previa (definición del problema, datos o elección del modelo) lo provocó con más probabilidad, y cómo lo demostrarías?

#### Aprender

Vocabulario central de ML, el flujo de ocho pasos desde definir el problema hasta desplegar, y el aprendizaje supervisado como predicción a partir de ejemplos etiquetados—no como marca de algoritmo.

**Preguntas reflexivas:**

1. Para la pregunta de negocio de WeLoveReviews (¿el sentimiento escrito coincide con el promedio de 4.5 estrellas?), ¿qué debe cumplirse en etiquetas y features para que el aprendizaje supervisado sea válido, y qué se rompe primero si esa suposición falla?
2. ¿Qué alternativa más simple (reglas, baseline de clase mayoritaria) probarías antes de descargar un modelo neuronal, y qué evidencia te convencería de subir la complejidad?

#### Reflexionar

Redes neuronales como una herramienta más dentro del ML; la conversación de cuándo NO usar redes; equilibrio entre capacidad del modelo, volumen de datos e interpretabilidad para stakeholders.

**Preguntas reflexivas:**

1. ¿Dónde trazarías la línea entre un modelo clásico y una red neuronal para el caso de WeLoveReviews—qué restricción (tamaño de datos, latencia, explicabilidad) inclina la balanza?
2. Si eliges un modelo más pesado, ¿qué coste de segundo orden asume el equipo en mantenimiento, depuración o inferencia?

Sondeos del facilitador:

- Si dicen "las redes siempre son mejores," pregunta qué señal necesitarían de un baseline más simple para justificar la complejidad extra.
- Si dicen "fine-tuneamos después," pregunta qué pasa con los plazos de integración si el dominio de entrenamiento del modelo no coincide con sus datos (como el desajuste entre reseñas de productos y reseñas de servicios en `nlptown`).

#### Tener en cuenta

Splits train/validation/test y baselines antes de confiar en métricas; desajuste de dominio al adoptar modelos de hubs; precisión sola en datos desbalanceados; fijar versiones y probar con muestra propia primero.

**Preguntas reflexivas:**

1. Un modelo del hub muestra benchmarks fuertes—¿qué tres comprobaciones harías con *tus* datos antes de cablearlo al backend, y cuál bloquearía el merge?
2. ¿Cómo detectarías una degradación silenciosa cuando la población en producción se aleja de los datos con los que se entrenó el modelo?

#### Hacer

Alinear tipo de modelo con el problema (clasificación → salida discreta, regresión → continua); integrar modelos preentrenados con paso de validación sobre muestras reales; cargar una vez al arranque, fijar versiones, preferir artefactos mantenidos en el hub.

**Preguntas reflexivas:**

1. Recorre el filtro de selección que usarías en un hub—descargas y estrellas son fáciles; ¿qué prueba observable te haría confiar en la salida sobre cinco filas del dataset de reseñas?
2. Tras la integración, ¿qué log o métrica única demostraría que las predicciones funcionan—no solo que el import tuvo éxito?

#### Evitar

Evaluar sobre datos de entrenamiento; tratar la precisión como suficiente; ignorar el cambio de distribución; cargar el modelo en cada petición; saltarse validación post-integración; adoptar modelos sin leer el contexto de entrenamiento.

**Preguntas reflexivas:**

1. Si la precisión luce perfecta el primer día, ¿qué antipatrón suele esconderse detrás de ese número en datos desbalanceados, y cómo lo expondrías?
2. ¿Qué se rompe a nivel operativo si cada llamada a la API recarga un modelo preentrenado grande, y qué tan reversible es ese error de arquitectura?

Sondeos del facilitador:

- Si dicen "validamos en producción," pregunta quién paga el coste de predicciones erróneas antes de tener una auditoría por muestreo.
- Si dicen "cualquier modelo popular sirve," pregunta qué leerían en la ficha del modelo para refutar eso en menos de diez minutos.

### Cierre — Excelencia como AI Engineer

1. ¿Qué decisión del debate de hoy—encuadre del problema, tipo de modelo o disciplina de validación—defenderías en una code review para demostrar que aplicas modelos de predicción como ingeniero, no como quien descarga por moda?
