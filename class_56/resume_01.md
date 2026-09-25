# Clase 56: modelos de clasificación y entrenamiento de un clasificador

## Hilo de continuidad

La clase 55 trabajó la preparación de datos, la división entre entrenamiento, validación y prueba, y los riesgos de fuga de información. En esta clase se utiliza ese dataset preparado para comprender cómo funcionan los modelos de clasificación y cómo se entrena, evalúa y mejora un clasificador.

Los dos módulos de LearnPack siguen este recorrido:

```text
datos preparados
-> problema de clasificación
-> representación de características
-> división train / validation / test
-> selección y entrenamiento del clasificador
-> predicción
-> evaluación
-> detección de sobreajuste
```

La idea central es:

> Un clasificador no es bueno solo porque tenga una accuracy alta. Debe aprender con datos adecuados, generalizar a ejemplos no vistos y ser evaluado con métricas que reflejen el coste real de sus errores.

## Objetivos

Al terminar la sesión, el estudiante podrá:

- Explicar qué es un problema de clasificación y distinguirlo de uno de regresión.
- Diferenciar clasificación binaria y multiclase.
- Describir cómo un modelo aprende una frontera de decisión a partir de características y etiquetas.
- Convertir texto en características numéricas mediante bolsa de palabras y TF-IDF.
- Explicar cómo funciona un árbol de decisión y qué representan sus nodos, ramas y hojas.
- Identificar sobreajuste e inestabilidad en árboles individuales.
- Comparar árboles de decisión, bosques aleatorios y gradient boosting.
- Elegir un algoritmo inicial considerando tamaño de datos, interpretabilidad, relaciones no lineales y balance de clases.
- Separar correctamente datos de entrenamiento, validación y prueba.
- Entrenar un clasificador con el patrón `fit`/`predict` de scikit-learn.
- Interpretar matriz de confusión, precision, recall, F1-score y reporte de clasificación.
- Detectar sobreajuste comparando rendimiento en train y test.

## Agenda de 90 minutos

| Tiempo | Bloque | Resultado |
| --- | --- | --- |
| 0-8 | Puente y caso de negocio | Definir entrada, clases y coste del error |
| 8-20 | Qué es la clasificación | Distinguir binaria, multiclase y multilabel |
| 20-32 | De datos a características | Representar texto y variables tabulares |
| 32-45 | Árboles de decisión | Leer reglas y entender divisiones |
| 45-57 | Límites y ensamblajes | Relacionar sobreajuste con random forest y boosting |
| 57-70 | División y entrenamiento | Aplicar el flujo train/validation/test |
| 70-82 | Evaluación | Leer matriz de confusión y reporte |
| 82-88 | Taller aplicado | Completar y comparar clasificadores |
| 88-90 | Cierre | Exit ticket y checklist |

Para 60 minutos, omitir el detalle de TF-IDF y el bloque de gradient boosting, y realizar el taller con un único clasificador. Para 120 minutos, comparar varios modelos, ajustar `max_depth` y `n_estimators`, y analizar errores por clase.

## Preparación del instructor

- Abrir `class_56/tutorial.json` y `class_56/tutorial_2.json`.
- Tener disponible el dataset preparado de la clase 55 o usar Iris para una primera demostración.
- Preparar una matriz de confusión sencilla con una clase minoritaria.
- Recordar que una clasificación puede tener dos clases o varias, y que la métrica adecuada depende del problema.
- Tener claro que el curso utiliza ejemplos de scikit-learn; las ejecuciones del alumnado deben respetar la división de datos y evitar leakage.

## 0-8 min: abrir con una decisión de negocio

Presentar este caso:

```text
Un sistema debe decidir si una transacción es legítima o fraudulenta.
El 95 % de las transacciones son legítimas y el 5 % son fraude.
Un modelo predice siempre “legítima” y obtiene 95 % de accuracy.
```

Preguntar:

1. ¿Es útil el modelo?
2. ¿Qué tipo de error sería más costoso: un falso positivo o un falso negativo?
3. ¿Qué métrica mirarías además de accuracy?

La respuesta esperada es que la accuracy puede ocultar el fracaso en la clase minoritaria. Se deben revisar la matriz de confusión, recall, precision y F1-score, según el coste de cada error.

## 8-20 min: qué es la clasificación

La clasificación asigna una observación a una categoría a partir de sus características:

```text
características X + etiqueta y
-> aprendizaje de una frontera o regla
-> clase predicha
```

Ejemplos:

- correo spam o no spam;
- transacción fraudulenta o legítima;
- cliente que abandona o permanece;
- imagen clasificada como gato, perro o ave;
- reseña clasificada como negativa, neutral o positiva.

### Tipos de clasificación

- **Binaria:** exactamente dos clases posibles.
- **Multiclase:** una observación pertenece a una entre tres o más clases.
- **Multilabel:** una observación puede tener varias etiquetas al mismo tiempo.

No confundir clasificación con regresión. Si la salida es una categoría, es clasificación; si es un valor continuo, es regresión. Una puntuación de estrellas puede modelarse como clases ordinales o como una cantidad numérica, pero la decisión debe responder a la pregunta de negocio.

### Frontera de decisión

El modelo aprende una separación en el espacio de características. Para dos variables podría verse como una línea o una curva; con más variables es una superficie difícil de visualizar. La forma de esa frontera depende del algoritmo:

- regresión logística: frontera generalmente lineal;
- árbol de decisión: regiones construidas mediante reglas escalonadas;
- ensambles: combinación de muchas fronteras y reglas.

## 20-32 min: de datos a características

Los clasificadores trabajan con representaciones numéricas. Las variables tabulares pueden limpiarse y codificarse, pero el texto también debe convertirse en columnas o vectores.

### Bolsa de palabras

La bolsa de palabras construye un vocabulario con los términos de entrenamiento. Cada palabra se convierte en una característica y cada documento en una fila de conteos:

```text
vocabulario: gratis | dinero | reunión | factura | ahora
documento:       1   |   1    |   0     |   0      |  1
```

El modelo puede aprender reglas como «si aparece `gratis`, aumenta la probabilidad de spam». Esta representación ignora gran parte del orden de las palabras, por lo que debe utilizarse conociendo sus limitaciones.

### TF-IDF

TF-IDF pondera la frecuencia de un término en un documento y reduce el peso de las palabras que aparecen en casi todos los documentos. Es una representación útil como baseline para clasificación de texto.

Reglas de seguridad:

- dividir antes de ajustar el vectorizador;
- aprender el vocabulario solo con train;
- transformar validation y test con el vectorizador ya ajustado;
- evitar que la etiqueta o información posterior al evento entre en el texto.

## 32-45 min: árboles de decisión

Un árbol clasifica siguiendo reglas `if/then` desde un nodo raíz hasta una hoja:

```text
¿puntaje_credito > 700?
├── sí  -> ¿ingresos > 50 000?
│        ├── sí -> APROBADO
│        └── no -> RECHAZADO
└── no  -> RECHAZADO
```

### Cómo aprende un árbol

1. Evalúa posibles características y umbrales.
2. Busca una división que separe mejor las clases.
3. Repite el proceso en cada rama.
4. Detiene el crecimiento según límites como profundidad máxima o número mínimo de muestras.
5. Asigna una clase en cada hoja.

La impureza mide qué tan mezcladas están las clases en un nodo. Un nodo con ejemplos de una sola clase tiene impureza baja; uno con clases muy mezcladas tiene impureza alta.

### Ventajas y límites

Ventajas:

- reglas fáciles de explicar;
- captura relaciones no lineales;
- no requiere escalado de características;
- funciona con interacciones entre variables.

Riesgos:

- puede crecer demasiado y memorizar el entrenamiento;
- pequeños cambios en los datos pueden producir un árbol muy diferente;
- un árbol individual puede ser inestable y sensible a outliers.

## 45-57 min: ensamblajes y elección del algoritmo

### Bosque aleatorio

Un bosque aleatorio entrena muchos árboles con muestras y subconjuntos de características diferentes. Después combina sus predicciones. La diversidad entre árboles reduce la varianza y suele mejorar la estabilidad frente a un árbol individual.

### Gradient boosting

El boosting construye modelos secuencialmente. Cada nuevo modelo intenta corregir errores de los anteriores. Puede alcanzar muy buen rendimiento en datos tabulares, aunque normalmente requiere más ajuste de hiperparámetros.

### Marco de decisión

| Situación | Punto de partida razonable |
| --- | --- |
| Dataset pequeño y necesidad de explicación | Regresión logística o árbol pequeño |
| Relaciones no lineales y baseline tabular | Árbol de decisión |
| Mayor robustez y menor varianza | Random forest |
| Dataset tabular con optimización de rendimiento | Gradient boosting |
| Texto con baseline interpretable | TF-IDF más clasificador lineal |

Estas son orientaciones, no reglas absolutas. Se debe comparar contra un baseline, revisar el coste de los errores y comprobar el comportamiento en datos no vistos.

## 57-70 min: dividir y entrenar

La secuencia segura es:

```text
dataset
-> train: aprende parámetros
-> validation: compara modelos y ajusta hiperparámetros
-> test: evaluación final una sola vez
```

En problemas desbalanceados se debe considerar la estratificación para conservar aproximadamente la proporción de clases en cada división. Si existe dependencia temporal o por usuario, el split debe respetar la unidad de generalización y no mezclar información del futuro o del mismo usuario entre conjuntos.

### Patrón de scikit-learn

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

Separar claramente:

- **hiperparámetros:** elegidos por el desarrollador, como `max_depth`;
- **parámetros aprendidos:** calculados durante `fit`;
- **predicción:** aplicación del modelo a datos que no deben modificarlo.

El preprocesamiento también debe formar parte de un pipeline para impedir que el escalador, codificador o vectorizador aprenda de validation o test.

## 70-82 min: evaluar el rendimiento

### Matriz de confusión

Para clasificación binaria:

| | Predicción positiva | Predicción negativa |
| --- | --- | --- |
| Real positiva | Verdadero positivo | Falso negativo |
| Real negativa | Falso positivo | Verdadero negativo |

- **Precision:** de los casos predichos como positivos, cuántos eran positivos.
- **Recall:** de los positivos reales, cuántos detectó el modelo.
- **F1-score:** equilibrio entre precision y recall.
- **Accuracy:** proporción total de aciertos.

Cuando las clases están desequilibradas, accuracy no debe analizarse sola. Hay que revisar métricas por clase y el objetivo del negocio. En fraude, por ejemplo, un recall bajo de la clase fraudulenta puede ser más grave que una cantidad moderada de falsos positivos.

### Preguntas para leer un reporte

1. ¿Qué clase tiene el F1-score más bajo?
2. ¿El modelo está ignorando la clase minoritaria?
3. ¿Los falsos negativos son más costosos que los falsos positivos?
4. ¿La métrica se calculó en datos realmente no vistos?
5. ¿Hay ejemplos concretos que contradigan la métrica agregada?

## 82-88 min: taller aplicado

### Ejercicio A: tres clasificadores

Usar Iris o un dataset binario preparado y completar este flujo:

1. Separar `X` e `y`.
2. Crear train y test con `random_state=42` y, cuando corresponda, `stratify=y`.
3. Instanciar un `DecisionTreeClassifier`, un `LogisticRegression` y un `RandomForestClassifier`.
4. Entrenar cada modelo solo con train.
5. Predecir sobre test.
6. Comparar accuracy, precision, recall y F1-score.
7. Explicar cuál elegirían y por qué.

### Ejercicio B: detectar sobreajuste

Comparar `model.score(X_train, y_train)` con `model.score(X_test, y_test)`:

- train muy alto y test mucho más bajo: posible sobreajuste;
- ambos bajos: posible subajuste o características insuficientes;
- ambos altos: comprobar que el split y el dataset no tengan leakage.

No basta con reducir la profundidad porque sube o baja una métrica. Hay que validar el cambio en un conjunto que no se haya usado para tomar la decisión.

## Cierre y exit ticket

Cada estudiante debe completar:

1. «Mi problema de clasificación tiene como entrada ______ y como clases ______.»
2. «La métrica más importante es ______ porque el coste de ______ es mayor.»
3. «Para evitar leakage, ajustaré ______ únicamente con train.»
4. «Sospecharía sobreajuste si ______.»
5. «Antes de elegir el modelo, compararé contra ______.»

Checklist final:

- [ ] El target y las clases están definidos.
- [ ] Las características están disponibles antes de la predicción.
- [ ] El split respeta el balance y la unidad de generalización.
- [ ] El preprocesamiento se ajusta solo con train.
- [ ] El modelo se compara contra un baseline.
- [ ] Se revisan métricas por clase y ejemplos concretos.
- [ ] Se evalúa el sobreajuste entre train y datos no vistos.
- [ ] Las decisiones y limitaciones quedan documentadas.