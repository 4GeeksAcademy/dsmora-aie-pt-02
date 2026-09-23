# Clase 55: preparar datos y construir predicciones supervisadas

> **Nota de trazabilidad:** esta guía se redactó después de ejecutar el scraper sobre `tutorial.json` y `tutorial_2.json`. Los nombres y conceptos de los módulos están respaldados por esos JSON. La agenda, las preguntas del profesor y el puente con WeLoveReviews son organización docente añadida; no forman parte literal del LearnPack.

## Contenido de los módulos scrapeados

### Módulo 1: modelos de predicción

El JSON contiene estas lecciones: bienvenida a los modelos de predicción, qué es un modelo, cómo funciona el aprendizaje supervisado, para qué se utilizan los modelos, clasificación frente a regresión, evaluación de modelos de predicción y cierre.

### Módulo 2: preparación de datos

El JSON contiene estas lecciones: bienvenida a la preparación de datos, ETL y transformación, técnicas de limpieza y validación, normalización y enriquecimiento, desafío de transformación, carga de datos, destinos de datos, evaluación de la preparación y cierre del pipeline.

El resto de esta guía es una propuesta para facilitar la clase a partir de esos contenidos.

## Hilo de continuidad

La clase 54 presentó el aprendizaje automático, las redes neuronales y la integración de un modelo preentrenado para analizar sentimiento. Ahora damos el siguiente paso: entender que una predicción supervisada solo es confiable si los datos están correctamente preparados. El flujo de hoy conecta los dos módulos de LearnPack enviados por el instructor:

```text
pregunta de negocio
-> datos etiquetados
-> extracción y transformación
-> validación y división
-> entrenamiento o carga del modelo
-> predicción
-> evaluación
```

La idea central es:

> Preparar datos no significa maquillar los datos para que el modelo acierte; significa convertir información real en entradas consistentes, trazables y adecuadas para aprender y evaluar.

## Objetivos

Al terminar la sesión, el estudiante podrá:

- Explicar qué es un modelo supervisado y diferenciar características, etiquetas, entrenamiento, predicción y evaluación.
- Distinguir clasificación de regresión con ejemplos de negocio.
- Describir el ciclo de vida de una predicción supervisada.
- Explicar el flujo ETL: extraer, transformar y cargar.
- Detectar problemas de calidad: nulos, duplicados, tipos incorrectos, valores atípicos, categorías inconsistentes y fuga de información.
- Elegir transformaciones apropiadas sin alterar el significado de los datos.
- Separar train, validation y test antes de ajustar transformaciones que aprendan de los datos.
- Conectar la preparación de datos con el proyecto WeLoveReviews y justificar qué se limpia y qué se conserva.

## Agenda de 75 minutos

| Tiempo | Bloque | Resultado |
| --- | --- | --- |
| 0-8 | Puente desde la clase 54 | Predicción supervisada como contrato entre entrada y etiqueta |
| 8-20 | Modelo y ciclo supervisado | Clasificación, regresión y flujo de ocho pasos |
| 20-35 | ETL y calidad | Perfil de datos y catálogo de problemas |
| 35-50 | Transformaciones | Nulos, tipos, categorías, escalado y outliers |
| 50-60 | Splits y fuga de información | Dataset listo sin contaminar la evaluación |
| 60-70 | Taller aplicado | Diseñar preparación para reseñas y un dataset tabular |
| 70-75 | Cierre | Checklist y exit ticket |

Para 60 minutos, reducir el taller a un solo caso y omitir el debate detallado de outliers. Para 90 minutos, ejecutar el pseudocódigo con pandas y comparar una preparación correcta con una que produce leakage.

## Preparación del instructor

- Abrir los dos módulos: **Supervised Learning: Prediction with Labeled Data** y **Preparing Data for Model Training**.
- Tener a mano `class_54/ai-eng-sentiment-analysis-reviews_project_README.es.md`.
- Preparar una tabla pequeña con errores deliberados: edades como texto, valores nulos, una categoría `Madrid` y otra `madrid`, y una fila duplicada.
- Recordar que el proyecto de sentimiento integra un modelo preentrenado; hoy no se entrena BERT. La práctica sirve para comprender el contrato de datos y para preparar futuros modelos.

## 0-8 min: abrir con un caso de fallo

**Qué decir**

> Un modelo puede estar correctamente instalado y aun así producir predicciones inútiles. Si una fecha está interpretada como texto, si una categoría aparece con tres nombres distintos o si la etiqueta se filtró dentro de una característica, el problema no se arregla escogiendo una red neuronal más grande.

Mostrar esta situación:

```text
Entrada: "5 estrellas, el personal fue amable"
Etiqueta de referencia: 5
Predicción: 1
Pregunta: ¿falló el modelo, el dominio, la preparación, la etiqueta o la interpretación?
```

No buscar una respuesta única. El objetivo es introducir que una predicción se debe investigar con evidencia: datos de entrada, transformación aplicada, salida y referencia.

Preguntas rápidas:

1. ¿Qué representa la entrada?
2. ¿Qué representa la etiqueta?
3. ¿Qué información no deberíamos usar al generar una predicción nueva?

Respuesta esperada: la reseña es una característica de entrada, la puntuación humana puede ser una etiqueta de comparación, y no debemos usar la etiqueta real como entrada.

## 8-20 min: aprendizaje supervisado y ciclo de predicción

### Modelo mental

En aprendizaje supervisado tenemos ejemplos donde conocemos la respuesta:

```text
características X + etiqueta y -> entrenamiento -> modelo
nuevas características X_nueva -> modelo -> predicción ŷ
ŷ + y_real -> evaluación
```

Una **característica** es una variable que el modelo puede utilizar como entrada. Una **etiqueta/target** es la respuesta que queremos aprender a predecir. La predicción es la salida generada para una observación nueva.

### Clasificación y regresión

- **Clasificación:** la salida pertenece a categorías. Ejemplos: fraude/no fraude, positivo/neutral/negativo, spam/no spam.
- **Regresión:** la salida es un valor numérico continuo. Ejemplos: demanda eléctrica en kWh, precio de una vivienda, tiempo de entrega.

Una puntuación de 1 a 5 puede tratarse como clasificación ordinal si las clases representan niveles, o como regresión si el problema necesita estimar una cantidad continua. La decisión depende de la pregunta de negocio, no del tipo de columna por sí solo.

### Ciclo supervisado

1. Definir el problema y el target.
2. Recopilar ejemplos representativos.
3. Preparar y validar los datos.
4. Separar entrenamiento, validación y prueba.
5. Elegir un baseline y un modelo.
6. Entrenar con train.
7. Evaluar con datos no vistos.
8. Desplegar, monitorizar y mejorar.

**Pregunta socrática:** ¿en qué pasos puede introducirse un error aunque el código se ejecute sin excepciones? En todos: una etiqueta mal definida, un dataset sesgado, una transformación incorrecta o una métrica inadecuada pueden producir una conclusión falsa.

## 20-35 min: ETL y calidad de datos

### Extraer, transformar y cargar

```text
Extract: obtener CSV, API, base de datos o archivos
Transform: limpiar, convertir, unir, validar y crear columnas
Load: guardar el dataset preparado en el destino acordado
```

ETL no es una única función. Es una cadena reproducible que debe dejar trazabilidad de:

- origen y fecha de extracción;
- columnas esperadas y tipos;
- filas recibidas, eliminadas y resultantes;
- reglas de limpieza;
- destino y versión del dataset.

### Perfil mínimo antes de modelar

Para cada dataset preguntar:

1. ¿Cuántas filas y columnas hay?
2. ¿Qué significa cada columna?
3. ¿Cuál es el target y cuándo estará disponible?
4. ¿Qué tipos tienen las columnas?
5. ¿Cuántos nulos, duplicados y valores imposibles existen?
6. ¿Hay categorías inconsistentes?
7. ¿La distribución del target está desequilibrada?
8. ¿Hay columnas que revelan indirectamente la respuesta?

Ejemplos de problemas:

| Problema | Riesgo | Primera acción |
| --- | --- | --- |
| `"42"` en una columna numérica | Cálculos y modelo incorrectos | Convertir y revisar errores |
| Nulos | Pérdida de filas o entrada inválida | Medir y definir regla |
| Duplicados | Dar peso excesivo a ejemplos | Confirmar si son duplicados reales |
| `Madrid`, `madrid`, `MADRID` | Crear categorías artificiales | Normalizar con cuidado |
| Fecha futura | Registro imposible o mala extracción | Validar contra reglas de negocio |
| Target ausente | No se puede entrenar ese ejemplo | Separar para inferencia |
| Target escondido en una feature | Métrica artificialmente alta | Eliminar la fuga |

**Regla docente:** primero medir, después decidir, y finalmente documentar. No borrar filas silenciosamente.

## 35-50 min: transformar sin destruir el significado

### Valores faltantes

No existe una solución universal:

- Eliminar una fila puede ser correcto si falta la entrada esencial y hay pocos casos.
- Imputar la mediana puede servir para una variable numérica robusta a outliers.
- Crear una categoría `desconocido` puede ser mejor que inventar una categoría real.
- En texto, una reseña vacía no debe sustituirse por una opinión ficticia: se excluye de la inferencia o se trata como caso no analizable.

Documentar siempre cuántos valores faltaban y qué sucedió con ellos.

### Tipos y escalas

- Convertir números guardados como texto después de validar separadores y símbolos.
- Convertir fechas a un formato consistente y derivar características justificadas, como día de la semana.
- Codificar categorías nominales con one-hot encoding cuando el orden no existe.
- No asignar `1, 2, 3` a categorías sin orden: el modelo podría interpretar una relación inventada.
- Escalar variables cuando el algoritmo es sensible a magnitudes, ajustando el escalador solo con train.

### Valores atípicos

Un outlier no es automáticamente un error. Puede ser:

- un registro inválido;
- un caso real poco frecuente;
- una señal de fraude o riesgo;
- un error de medición.

Antes de eliminarlo, comprobar el contexto, la unidad y la regla de negocio. En reseñas, un texto muy largo o una puntuación extrema puede ser precisamente el caso que queremos estudiar.

### Texto y sentimiento

Para WeLoveReviews:

- conservar el texto original para auditoría;
- normalizar espacios sin borrar señales útiles como negaciones o emojis sin justificarlo;
- verificar textos nulos o vacíos;
- conservar la puntuación humana como referencia separada de la predicción;
- no eliminar críticas negativas para que coincidan con la media de 4.5;
- documentar el desajuste entre reseñas de productos, usadas para ajustar el modelo, y reseñas de servicios, presentes en el dataset.

La limpieza no debe convertir `"no está mal"` en `"está mal"` ni modificar una reseña hasta que el modelo produzca la salida esperada.

## 50-60 min: train, validation, test y data leakage

### División correcta

```text
train      -> aprender parámetros y ajustar transformaciones
validation -> elegir modelo, hiperparámetros o umbrales
test       -> estimación final con datos no usados en decisiones
```

El test se toca al final. Si observamos repetidamente el test y cambiamos el modelo, deja de ser una evaluación honesta.

### Fuga de información

Hay leakage cuando información que no estaría disponible al producir una predicción entra en el entrenamiento o en una característica. Ejemplos:

- calcular la media de una variable usando train y test antes de dividir;
- incluir `fecha_de_cancelación` para predecir una cancelación;
- usar la etiqueta humana para construir la entrada;
- duplicar la misma persona entre train y test;
- ajustar el vocabulario o escalador con todo el dataset.

La regla práctica es:

> Toda transformación que aprende algo de los datos se ajusta con train y luego se aplica a validation/test.

La división debe respetar la unidad de generalización: si queremos generalizar a usuarios nuevos, el mismo usuario no debe aparecer en train y test. Si el problema es temporal, separar por tiempo puede ser más realista que mezclar aleatoriamente.

## 60-70 min: taller aplicado

### Caso A: reseñas de WeLoveReviews

En parejas, completar:

| Pregunta | Decisión esperada |
| --- | --- |
| Entrada del modelo | Texto de la reseña |
| Referencia humana | Estrellas, si están disponibles |
| Problema | Clasificar sentimiento por bandas o predecir estrellas |
| Vacío | Excluir/tratar aparte y contar |
| Duplicado | Confirmar antes de eliminar |
| Salida | Estrellas predichas y banda |
| Evidencia | Distribución, ejemplos y falsos negativos |
| Riesgo | Desajuste producto-servicio |

Cada pareja debe escribir una decisión que **no** tomaría automáticamente y explicar por qué.

### Caso B: dataset tabular de riesgo crediticio

Columnas: `income`, `age`, `city`, `approved`, `decision_date`.

Preguntar:

1. ¿Cuál es el target? `approved`.
2. ¿Qué columnas podrían ser características? `income`, `age`, `city`, siempre que estén disponibles antes de decidir.
3. ¿Qué revisarías en `decision_date`? Si se registró después de la decisión, es fuga.
4. ¿Cómo tratarías `city`? Normalizar categorías y codificarla sin inventar orden.
5. ¿Qué split usarías si las solicitudes futuras deben predecirse? Un split temporal puede ser más fiel.

### Mini-reto

Pedir que cada grupo transforme esta observación en una cadena de evidencia:

```text
Observación: 8% de los textos están vacíos y 12% de los usuarios aparecen dos veces.
```

Respuesta modelo:

```text
Observación -> hay entradas no analizables y posible duplicación.
Interpretación -> el porcentaje de sentimiento y la evaluación podrían estar sesgados.
Decisión -> contar los vacíos aparte, revisar duplicados por identificador y documentar las filas excluidas.
Validación -> comparar el número final de filas con el esperado antes de ejecutar inferencia.
```

## 70-75 min: cierre y exit ticket

Cada estudiante responde sin consultar material:

1. ¿Qué diferencia hay entre una característica y una etiqueta?
2. ¿Cuál es la diferencia entre clasificación y regresión?
3. ¿Por qué no se ajusta un escalador con train + test?
4. Da un ejemplo de leakage.
5. ¿Qué harías con una reseña vacía?
6. ¿Qué archivo del proyecto comunica el análisis y cuál contiene producción?

### Respuestas esperadas

1. La característica entra al modelo; la etiqueta es la respuesta que aprende o contra la que se compara.
2. Clasificación produce categorías; regresión produce valores continuos.
3. Porque el test filtraría información al proceso y la métrica dejaría de representar datos realmente no vistos.
4. Usar una variable creada después del evento que se intenta predecir, o ajustar una transformación con todo el dataset antes de dividir.
5. Medirla, no inventar texto, excluirla de inferencia o tratarla como caso no analizable y documentarlo.
6. `src/explore.ipynb` comunica la historia; `src/app.py` contiene la inferencia de producción.

## Entregables y puente a la siguiente clase

No se añade un proyecto nuevo. El estudiante debe aplicar el checklist al proyecto de sentimiento y completar o revisar:

- EDA en `src/explore.ipynb`.
- Reglas de limpieza justificadas.
- Modelo fijo y carga única.
- Comparación entre predicciones y estrellas humanas.
- Falsos negativos documentados.
- Lógica migrada a `src/app.py`.
- CSV `data/processed/reviews_with_sentiment.csv`.

La siguiente práctica puede convertir este diseño en código con pandas y scikit-learn: construir un pipeline reproducible, entrenar un baseline y evaluar una predicción sin leakage.

## Frase de cierre

> Un buen modelo no empieza con una arquitectura sofisticada; empieza con una pregunta clara, datos comprendidos y transformaciones que podemos explicar.
