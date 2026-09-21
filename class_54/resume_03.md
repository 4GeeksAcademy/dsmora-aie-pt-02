# Clase 54: EDA, insights y conexión con el proyecto

## Propósito de esta guía

Esta guía añade el puente que falta entre los módulos de LearnPack y el proyecto **WeLoveReviews**. Los módulos explican los fundamentos del aprendizaje automático, las redes neuronales y los modelos preentrenados. El proyecto, además, exige explorar un dataset real, extraer insights, justificar una limpieza, documentar decisiones y comunicar resultados.

El objetivo no es convertir esta sesión en una clase completa de estadística. El objetivo es que el profesor pueda explicar por qué no se debe ejecutar un modelo sobre datos desconocidos y cómo pasar de una observación a una decisión defendible.

## Qué cubren los módulos y qué añade el proyecto

Los módulos cubren principalmente:

- Qué es el aprendizaje automático.
- Datasets, características, etiquetas y predicciones.
- Aprendizaje supervisado, no supervisado, auto-supervisado y por refuerzo.
- Clasificación y regresión.
- Redes neuronales y aprendizaje profundo.
- Modelos preentrenados.
- Carga, inferencia y evaluación conceptual de un modelo.

El proyecto añade contenidos de práctica profesional que no se explican con el mismo detalle en los módulos:

- Análisis exploratorio de datos o EDA.
- Inspección de calidad de un CSV real.
- Formulación de insights a partir de observaciones.
- Decisiones de limpieza justificadas.
- Notebook como documento de comunicación.
- Integración de un modelo existente en vez de entrenar uno nuevo.
- Comparación entre señales distintas: texto, estrellas humanas y predicción del modelo.
- Identificación y explicación de falsos negativos.
- Separación entre notebook de análisis y script de producción.
- Exportación de un CSV procesado.

Frase clave para el profesor:

> Los módulos enseñan qué es un modelo; el proyecto enseña cómo decidir si los datos y la salida del modelo son útiles para una pregunta de negocio.

## Caso de negocio

WeLoveReviews recibe 500 reseñas escritas de un negocio cuya puntuación media es de 4.5 sobre 5. La account manager quiere saber:

1. Cuántas reseñas parecen positivas, neutrales o negativas según el texto.
2. Si esa distribución coincide con la puntuación media de 4.5 estrellas.
3. Por qué podrían existir diferencias entre las estrellas y el sentimiento escrito.
4. Si el modelo puede producir errores sistemáticos.

El proyecto utiliza el modelo:

```text
nlptown/bert-base-multilingual-uncased-sentiment
```

El modelo devuelve una predicción de 1 a 5 estrellas. El proyecto pide convertirla en bandas:

```text
| Predicción del modelo | Banda    |
| --------------------- | -------- |
| 1-2 estrellas         | Negativo |
| 3 estrellas           | Neutral  |
| 4-5 estrellas         | Positivo |
```

La media de 4.5 es una medida agregada del negocio. La predicción del modelo es una salida individual para cada reseña. No deben tratarse como si fueran la misma variable.

## Qué es EDA

EDA significa **Exploratory Data Analysis**, o **análisis exploratorio de datos**.

Es un proceso para conocer los datos antes de analizarlos o modelarlos. Incluye inspecciones, resúmenes, conteos, distribuciones, ejemplos y visualizaciones sencillas.

Una definición para explicar en clase:

> El EDA es la investigación inicial que hacemos sobre los datos para descubrir su estructura, calidad, patrones, limitaciones y preguntas relevantes antes de tomar decisiones de modelado.

EDA no significa:

- Ejecutar el modelo y aceptar sus resultados.
- Hacer gráficos sin interpretarlos.
- Eliminar datos automáticamente.
- Buscar únicamente una correlación bonita.
- Sustituir la evaluación del modelo.

## El flujo completo del proyecto

Presentar el proyecto como esta cadena:

```text
pregunta de negocio
-> conocer los datos
-> encontrar problemas y patrones
-> extraer insights
-> decidir y justificar la limpieza
-> elegir o integrar el modelo
-> ejecutar inferencia
-> evaluar y revisar errores
-> comunicar conclusiones
```

El EDA aparece antes de la inferencia porque las decisiones sobre los datos pueden cambiar la forma de usar el modelo.

## Preguntas mínimas del EDA

Antes de ejecutar el modelo, el estudiante debe responder mediante código y texto:

### 1. ¿Cuántas filas y columnas hay?

Comprobar que el dataset tiene las 500 reseñas esperadas. Si el número no coincide, no se debe continuar como si nada hubiera ocurrido.

Posibles causas:

- El archivo no es el correcto.
- Se han perdido filas durante una transformación.
- Hay filtros aplicados previamente.
- Existen filas duplicadas.

### 2. ¿Qué representa cada columna?

Identificar las columnas de texto, estrellas, identificadores u otros metadatos. El estudiante debe poder explicar cuál será la entrada del modelo y cuál será la referencia humana para comparar.

En este caso, el texto de la reseña es la entrada principal. Si existe una puntuación humana, debe conservarse para el análisis de desacuerdos.

### 3. ¿Qué tipos de datos tiene cada columna?

Comprobar si las estrellas están almacenadas como números o como texto y si las reseñas están almacenadas como cadenas.

Una columna numérica guardada como texto puede impedir cálculos correctos de medias, conteos o comparaciones.

### 4. ¿Hay valores nulos o textos vacíos?

Contar valores nulos y cadenas vacías. Un registro sin texto no puede enviarse al modelo de la misma manera que una reseña completa.

La decisión no debe ser silenciosa. El notebook debe indicar cuántos registros se encontraron y qué se hizo con ellos.

### 5. ¿Hay duplicados?

Comprobar si aparecen reseñas repetidas o identificadores duplicados. Los duplicados pueden alterar los porcentajes y dar demasiado peso a una misma opinión.

No siempre se deben eliminar automáticamente: primero hay que decidir si son duplicados reales o reseñas legítimamente iguales.

### 6. ¿Cómo se distribuyen las estrellas humanas?

Contar las reseñas con 1, 2, 3, 4 y 5 estrellas. La media de 4.5 por sí sola no muestra la distribución completa.

Dos datasets pueden tener la misma media y distribuciones muy diferentes. Por ejemplo, uno puede concentrarse en 4 y 5, mientras otro puede mezclar muchas valoraciones muy bajas y muy altas.

### 7. ¿Cómo son los textos?

Revisar ejemplos y, si resulta útil, calcular longitud en caracteres o palabras. Buscar:

- Textos vacíos.
- Textos extremadamente cortos.
- Textos muy largos.
- Comentarios con emojis.
- HTML o caracteres extraños.
- Idiomas mezclados.
- Quejas y elogios en la misma reseña.

Estas observaciones pueden ayudar a interpretar errores posteriores.

## De una observación a un insight

El profesor debe enseñar esta estructura:

```text
observación
-> interpretación
-> consecuencia para el proyecto
```

Ejemplo:

```text
Observación: existen textos vacíos.
Interpretación: algunas filas no contienen evidencia lingüística.
Consecuencia: hay que excluirlas, tratarlas aparte o documentar que no son analizables.
```

Otro ejemplo:

```text
Observación: la mayoría de las estrellas humanas son 4 o 5.
Interpretación: la referencia está inclinada hacia valoraciones positivas.
Consecuencia: una gran proporción de predicciones positivas no demuestra por sí sola que el modelo entienda bien el texto.
```

## Ejemplos de insights que pueden aparecer

Los siguientes son ejemplos de razonamiento. No deben presentarse como resultados reales hasta calcularlos sobre el CSV.

### Insight 1: la media oculta la distribución

Si la media es 4.5, todavía no sabemos cuántas reseñas tienen 1, 2, 3, 4 o 5 estrellas.

**Decisión:** contar cada categoría y mostrar la distribución, no comunicar únicamente la media.

### Insight 2: las estrellas y el texto son señales diferentes

Una persona puede dar 5 estrellas y escribir una queja concreta sobre el tiempo de espera. Otra puede dar 3 estrellas y escribir un comentario amable con una reserva.

**Decisión:** comparar la predicción con la puntuación, pero revisar los desacuerdos mediante ejemplos reales.

### Insight 3: una reseña puede mezclar sentimientos

Una reseña puede elogiar al personal y criticar el precio o la espera. Un único valor positivo, neutral o negativo puede simplificar demasiado el contenido.

**Decisión:** documentar límites del análisis y no presentar la banda como una descripción completa de la opinión.

### Insight 4: el dominio puede afectar al modelo

El modelo se ajustó con reseñas de productos, mientras que el dataset del proyecto contiene reseñas de servicios. El vocabulario y las situaciones pueden ser diferentes.

**Decisión:** buscar falsos negativos y formular hipótesis sobre el desajuste de dominio.

### Insight 5: los textos cortos tienen menos contexto

Una reseña como "bien" o "regular" puede ser ambigua fuera de contexto.

**Decisión:** incluir ejemplos cortos en la revisión manual y comprobar si el modelo falla más en ellos.

## Qué es una buena limpieza

La limpieza no consiste en borrar todo lo que parezca extraño. Es una serie de transformaciones justificadas por el EDA.

Ejemplos posibles:

- Eliminar filas sin texto si el modelo necesita texto.
- Normalizar espacios sobrantes.
- Convertir una columna de estrellas a tipo numérico.
- Eliminar duplicados reales.
- Mantener emojis o signos si aportan sentimiento.
- Documentar registros excluidos y el motivo.

La limpieza debe ser conservadora. No conviene:

- Cambiar el contenido de la reseña para hacer que el modelo acierte.
- Eliminar críticas negativas solo porque contradicen la media.
- Traducir textos automáticamente sin documentarlo.
- Sustituir valores faltantes por una opinión inventada.

## EDA no es evaluación del modelo

Es importante separar dos momentos:

```text
EDA:
¿cómo son los datos antes de modelar?

Evaluación:
¿qué tan útiles son las predicciones del modelo?
```

El EDA puede revelar que hay textos vacíos, duplicados o clases desbalanceadas. La evaluación posterior debe comprobar la distribución de predicciones, comparar con referencias disponibles y revisar manualmente entre 15 y 20 reseñas.

## Notebook como documento de comunicación

El proyecto exige que `src/explore.ipynb` sea un documento ejecutado y legible, no solo una colección de celdas.

Una estructura recomendada es:

```text
1. Objetivo de negocio
2. Carga y descripción del dataset
3. EDA: tamaño, columnas, tipos y calidad
4. Distribución de estrellas y ejemplos de texto
5. Insights y decisiones de limpieza
6. Plan de acción y justificación del modelo
7. Inferencia sobre las reseñas
8. Mapeo de estrellas a bandas
9. Distribución positivo/neutral/negativo
10. Comparación con la media de 4.5
11. Falsos negativos
12. Revisión manual de 15-20 reseñas
13. Limitaciones y conclusiones
```

Cada bloque importante de código debe tener una explicación breve en Markdown:

- Qué se está comprobando.
- Qué resultado se obtuvo.
- Por qué ese resultado importa.
- Qué decisión se toma a continuación.

## Contenido del proyecto que el profesor debe explicar

### Integración, no entrenamiento

El proyecto no pide entrenar un modelo desde cero ni hacer fine-tuning. Pide integrar un modelo preentrenado, ejecutar inferencia y validar sus resultados.

```text
modelo preentrenado + texto de reseña -> estrellas predichas -> banda de sentimiento
```

### Carga eficiente

El modelo se carga una sola vez antes de procesar las reseñas. No debe descargarse ni inicializarse una vez por cada fila.

```text
cargar modelo una vez
-> recorrer las reseñas
-> generar predicciones
-> guardar resultados
```

### Salida procesada

El proyecto pide crear:

```text
data/processed/reviews_with_sentiment.csv
```

La salida debe conservar la información necesaria para revisar las predicciones y analizar los desacuerdos.

### Notebook y aplicación

Separar responsabilidades:

- `src/explore.ipynb`: historia del análisis, EDA, insights, gráficos, resultados y conclusiones.
- `src/app.py`: lógica limpia de inferencia para producción.
- `data/processed/reviews_with_sentiment.csv`: salida enriquecida.
- `requirements.txt`: dependencias con versiones fijadas.

### Falsos negativos

El proyecto pide buscar casos en los que el modelo predice 1 o 2 estrellas, pero:

- la puntuación humana es 4 o 5; o
- al leer el texto, parece positivo o neutral.

Para documentar un caso no basta con copiar la reseña. Hay que incluir:

1. El texto o un extracto suficiente.
2. La puntuación humana, si existe.
3. La predicción del modelo.
4. La banda asignada.
5. La explicación posible del desacuerdo.

## Preguntas para comprobar comprensión

1. ¿Qué diferencia hay entre observar que el 80% de las reseñas tiene 4 o 5 estrellas y extraer un insight?
2. ¿Por qué una media de 4.5 no describe toda la distribución?
3. ¿Qué harías con una reseña sin texto?
4. ¿Por qué no debemos eliminar automáticamente todos los textos cortos?
5. ¿Por qué una reseña de servicio puede confundir a un modelo ajustado con productos?
6. ¿Qué diferencia hay entre el EDA y la evaluación del modelo?
7. ¿Qué información debe conservarse para investigar un falso negativo?
8. ¿Por qué el modelo se carga una sola vez?
9. ¿Qué debe contener el notebook y qué debe contener `src/app.py`?
10. ¿Qué conclusión sería demasiado fuerte a partir de una sola predicción?

## Cierre para el profesor

La idea principal que debe quedar es:

> Antes de preguntar qué predice un modelo, tenemos que conocer qué datos le estamos entregando y qué significa cada resultado.

El proyecto evalúa más que una llamada correcta a Hugging Face. Evalúa si el estudiante puede construir una cadena de evidencia:

```text
los datos tienen esta estructura
-> encontramos estos problemas o patrones
-> tomamos estas decisiones de limpieza
-> usamos este modelo por estas razones
-> observamos estos resultados
-> revisamos estos errores
-> comunicamos esta conclusión con sus limitaciones
```

Esta cadena convierte el EDA y los insights en parte central del trabajo de ingeniería de IA, aunque los módulos no los desarrollen como una lección independiente.
