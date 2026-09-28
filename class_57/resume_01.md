# Clase 57: Series temporales, modelos de regresión y entrenamiento de un regresor con scikit-learn

## Hilo de continuidad

En la clase 56 se trabajó con clasificación: cómo entrenar modelos que predicen categorías y cómo evaluarlos con matriz de confusión, precisión, recall y F1-score. En esta clase se da el salto a la regresión — predecir valores numéricos continuos — y se exploran las series temporales como contexto para entender predicciones sobre datos que evolucionan en el tiempo.

Los contenidos de LearnPack siguen este recorrido:

```text
clasificación (clase 56)
-> ¿qué es regresión?
-> cómo aprenden los modelos de regresión (residuos, descenso por gradiente)
-> árboles de decisión y ensamblajes adaptados a regresión
-> bosque aleatorio como regresor
-> regresión lineal vs random forest vs XGBoost
-> preparación de datos para regresión
-> métricas de evaluación: R², MSE, MAE
-> entrenamiento completo de un regresor con scikit-learn
-> monitoreo de deriva con PSI
```

La idea central es:

> La regresión no solo responde "¿cuánto?" en lugar de "¿qué categoría?". Requiere métricas que midan cercanía (MSE, R²) en vez de aciertos, y una preparación de datos que prescinde de la estratificación porque el objetivo es continuo.

## Objetivos

Al terminar la sesión, el estudiante podrá:

- Explicar qué distingue un problema de regresión de uno de clasificación.
- Describir cómo aprenden los modelos de regresión mediante el ciclo predecir-medir-ajustar (residuo, descenso por gradiente).
- Diferenciar regresión lineal, Random Forest Regressor y XGBoost según sus supuestos, fortalezas y debilidades.
- Entender cómo los árboles de decisión se adaptan a objetivos continuos (minimización de varianza) y cómo el ensamblaje (bosque aleatorio) promedia múltiples árboles.
- Preparar datos para regresión: separar X/y, dividir sin estratificación, escalar con StandardScaler.
- Calcular e interpretar R², MSE y MAE.
- Entrenar un modelo LinearRegression y un RandomForestRegressor con scikit-learn usando el patrón `fit`/`predict`.
- Identificar el concepto de deriva del modelo y el propósito del PSI (Population Stability Index).

## Agenda de 75 minutos

| Tiempo | Bloque | Resultado |
| --- | --- | --- |
| 0-7 | Puente desde clasificación | Recordar accuracy vs. cercanía numérica |
| 7-20 | ¿Qué es regresión? | Residuo, descenso por gradiente, ejemplos |
| 20-32 | Algoritmos de regresión | Lineal, árboles, random forest, XGBoost |
| 32-45 | Preparación de datos | Sin estratificación, escalado, split |
| 45-57 | Métricas de evaluación | R², MSE, MAE |
| 57-68 | Entrenamiento con scikit-learn | Pipeline fit/predict con dos modelos |
| 68-75 | Cierre y PSI | Deriva, checklist |

Para 60 minutos, omitir el detalle de XGBoost y PSI, y centrarse en regresión lineal + random forest + R²/MSE. Para 90 minutos, incluir el bloque de PSI completo y comparar tres algoritmos.

## Preparación del instructor

- Tener abiertos `class_57/tutorial.json` (regression-models) y `class_57/tutorial_2.json` (training a regression model).
- Los contenidos de series temporales están en `class_57/time_series.json` (3 lecciones: qué son, análisis visual, modelos ARIMA/Exponential Smoothing/LSTM) y `class_57/exploring_time_series.json` (enlace a notebook Colab interactivo).
- Tener preparado un dataset pequeño de precios de casas o usar el que proporciona el tutorial_2.
- Recordar que la clase 56 usó clasificación; esta clase cambia a regresión pero comparte herramientas (árboles, ensamblajes, train/test split).

## 0-7 min: puente desde clasificación (caso de negocio)

Presentar este contraste:

```text
Clasificación: ¿Es fraude o no? → categoría.
Regresión: ¿Cuánto cuesta esta casa? → número continuo.
```

Preguntar:

1. ¿Qué problema del mundo real predecirías con un número en vez de una etiqueta?
2. Si un modelo de precio de casa falla por 10.000 €, ¿es un error igual que si falla por 100.000 €?
3. ¿Cómo medirías qué tan cerca estuvo la predicción del valor real?

La respuesta esperada es que en clasificación un error es binario (acierto/fallo), mientras que en regresión la magnitud del error importa. Esto prepara la necesidad de métricas como MSE y R².

## 7-20 min: qué es la regresión y cómo aprenden los modelos

### Definición (tutorial.json, lesson 1)

Regresión es un tipo de aprendizaje supervisado donde el objetivo es predecir un valor numérico continuo. La variable de salida puede tomar cualquier valor dentro de un rango, y los valores intermedios son significativos.

Conceptos clave del JSON:

```text
Variable objetivo: el número continuo que queremos predecir.
Predicción: valor estimado por el modelo.
Residuo (o error): diferencia entre el valor predicho y el valor real.
```

Ejemplos reales del contenido:

- Predecir el precio de una casa (312.000 € vs 313.000 € — el número exacto importa).
- Estimar el tiempo de entrega en minutos para un pedido de comida.
- Pronosticar el consumo de electricidad del próximo mes en kilovatios-hora.
- Probabilidad de abandono: un valor continuo entre 0 y 1.

### Cómo aprenden (tutorial.json, lesson 2)

El objetivo del entrenamiento es minimizar el error. Cada modelo de regresión intenta reducir la brecha entre sus valores predichos y los valores verdaderos. Esta brecha se cuantifica mediante una **función de pérdida**.

Explicar el ciclo iterativo (textual del JSON):

1. **Predecir**: el modelo hace predicciones basadas en los parámetros actuales.
2. **Medir**: calcula los residuos — diferencias entre predicciones y valores reales.
3. **Ajustar**: usando **descenso por gradiente**, el modelo actualiza sus parámetros para reducir estos residuos.
4. **Repetir**: el ciclo continúa refinando gradualmente las predicciones.

Anécdota del JSON: *"Es como afinar un instrumento musical: se hacen pequeños ajustes repetidamente hasta que el sonido (la predicción) es el correcto."*

## 20-32 min: algoritmos de regresión

### De la clasificación a la regresión (tutorial.json, lessons 3-5)

Explicar que los mismos árboles de decisión y ensamblajes usados en clasificación se adaptan para regresión:

- Un **árbol de regresión** ya no vota por una clase en cada hoja; predice un valor numérico (el promedio de los valores de entrenamiento que caen en esa hoja).
- Cada división busca **minimizar la varianza** de los valores objetivo en los nodos hijos.

### Regresión Lineal (tutorial_2.json, lesson 3)

| Aspecto | Descripción |
| --- | --- |
| Suposición | Relación lineal entre características y objetivo |
| Fortalezas | Rápido, altamente interpretable (coeficientes) |
| Debilidades | Dificultad con relaciones no lineales, sensible a outliers |
| Cuándo usarla | Como modelo base, datasets pequeños, cuando se necesita explicabilidad |

### Random Forest Regressor (tutorial.json, lessons 5-6)

- Construye muchos árboles de forma independiente, cada uno con una muestra bootstrap y un subconjunto aleatorio de características.
- Para predecir, **promedia** las predicciones numéricas de todos los árboles.
- No requiere escalado de características.
- Maneja bien relaciones no lineales y es robusto frente a outliers.

El JSON lo explica con el ejemplo de predicción de precios de casas: varios árboles capturan patrones distintos, y el promedio produce una estimación estable.

### XGBoost (tutorial.json, lesson 6)

Del JSON: "XGBoost comienza con una suposición simple — el promedio de todos los valores objetivo — y luego construye su modelo añadiendo árboles uno tras otro, cada uno enfocado en corregir los errores (residuos) dejados por el conjunto anterior."

Proceso:
1. Inicializar predicciones: usualmente el valor medio objetivo.
2. Calcular residuos: diferencia entre valores reales y predicciones actuales.
3. Entrenar un nuevo árbol que predice estos residuos.
4. Actualizar predicciones añadiendo las salidas del nuevo árbol.
5. Repetir hasta convergencia.

### Marco de decisión: Random Forest vs XGBoost (tutorial.json, lesson 7)

El JSON presenta cinco preguntas para decidir entre ambos:

| Pregunta | Si la respuesta es sí... |
| --- | --- |
| ¿Necesitas línea base rápida? | Random Forest |
| ¿Tiempo de entrenamiento limitado? | Random Forest |
| ¿Es importante la interpretabilidad? | Random Forest |
| ¿Tienes tiempo para ajustar hiperparámetros? | XGBoost |
| ¿Máxima precisión es prioridad con datos limpios? | XGBoost |

**Heurística del JSON**: datasets con menos de 10.000 filas → Random Forest; datasets grandes, limpios y estructurados de 100.000+ filas → XGBoost.

**Antipatrón del JSON**: "Optar por defecto por XGBoost porque 'gana competencias' es un error. Los datos de competencias suelen estar limpios y preprocesados; en aplicaciones reales los datos son más desordenados y el sobreajuste puede superar las ganancias de precisión."

Tabla comparativa del JSON:

| Algoritmo | Fortaleza clave | Principal debilidad | ¿Escalado necesario? |
| --- | --- | --- | --- |
| Regresión Lineal | Rápido, interpretable | Asume linealidad | Sí |
| Random Forest | Maneja no linealidad | Menos interpretable | No |
| XGBoost | Alta precisión | Ajuste complejo | No |

## 32-45 min: preparación de datos para regresión (tutorial_2.json, lesson 2)

### ¿Qué cambia respecto a clasificación?

| Aspecto | Clasificación | Regresión |
| --- | --- | --- |
| Estratificación | Sí, para preservar proporciones de clases | No tiene sentido (objetivo continuo) |
| Escalado | Opcional según el modelo | Crucial para modelos lineales |
| Split | `train_test_split` con `stratify=y` | `train_test_split` **sin** `stratify` |

### Código correcto del JSON

```python
from sklearn.model_selection import train_test_split

# Forma correcta para regresión (sin stratify)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### Conjuntos de entrenamiento, validación y prueba

El JSON describe tres conjuntos con propósito único:

- **Entrenamiento**: datos de los que el modelo aprende.
- **Validación**: separado del entrenamiento, se usa para comparar modelos y ajustar configuraciones. Se observa repetidamente.
- **Prueba**: se toca solo una vez al final para estimar rendimiento real.

Proporción común del JSON: 60 % entrenamiento, 20 % validación, 20 % prueba.

Código de división en dos pasos (del JSON):

```python
# Separar el conjunto de prueba, luego dividir el resto
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42
)
```

### Escalado con StandardScaler

El JSON explica que para regresión lineal el escalado es más crítico porque si las características tienen escalas muy diferentes (ingresos en miles vs. número de habitaciones en dígitos simples), los coeficientes se vuelven incomparables y el descenso por gradiente tiene dificultades.

Los modelos basados en árboles (Random Forest) son invariantes a la escala.

Pipeline completa de preparación del JSON:

1. Eliminar o imputar valores nulos.
2. Separar características (X) y objetivo (y).
3. Dividir en entrenamiento, validación y prueba (sin estratificación).
4. Escalar características con StandardScaler (ajustar en entrenamiento, transformar los demás).

## 45-57 min: métricas de evaluación (tutorial_2.json, lessons 4-5)

Explicar que las métricas de clasificación (accuracy, precisión, recall) no funcionan para regresión porque la variable objetivo es continua: no hay una "clase correcta".

### R² (Coeficiente de Determinación)

- **Qué mide**: proporción de la varianza en el objetivo que el modelo explica, comparado con predecir siempre la media.
- **Rango**: 1.0 es ajuste perfecto; 0 significa que el modelo no mejora respecto a la media.
- Es la métrica más reportada en regresión.

### Error Absoluto Medio (MAE)

- Media de los errores absolutos (sin signo).
- Fácil de interpretar en la misma unidad que el objetivo.

### Error Cuadrático Medio (MSE)

- Media de los errores al cuadrado.
- **Penaliza más los errores grandes**: los eleva al cuadrado, por lo que un error de 200 € se penaliza 4 veces más que uno de 100 € (no 2 veces).

Pregunta conceptual del JSON para lanzar a la clase:

> Un modelo predice 200 € para un artículo que cuesta 100 €, y 105 € para otro que cuesta 100 €. ¿Cómo trata el MSE estos errores?

Respuesta: "MSE penaliza 100 veces más la predicción de 200 € porque el error se eleva al cuadrado (100² vs 5²)."

## 57-68 min: entrenar y evaluar un modelo de regresión con scikit-learn (tutorial_2.json, lesson 5)

Este bloque es práctico. El JSON describe una tarea completa que los estudiantes deben implementar.

### Pipeline del ejercicio

1. **Cargar datos**: dataset de precios de casas (ya cargado, columna `price` como objetivo).
2. **Limpiar**: eliminar filas con valores nulos.
3. **Separar**: X (características) e y (columna `price`).
4. **Dividir**: 80/20 entrenamiento/prueba con `random_state=42`.
5. **Escalar**: `StandardScaler` — ajustar solo en entrenamiento, transformar ambos.
6. **Entrenar**:
   - `LinearRegression()`
   - `RandomForestRegressor(n_estimators=100, random_state=42)`
7. **Predecir** en el conjunto de prueba.
8. **Evaluar**: imprimir MSE y R² de cada modelo.

### Código del JSON

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Limpiar nulos
df = df.dropna()

# Separar X e y
X = df.drop('price', axis=1)
y = df['price']

# Dividir
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Escalar
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Modelo 1: Regresión Lineal
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)

print(f"Linear Regression MSE: {mean_squared_error(y_test, y_pred_lr):.2f}, "
      f"R2: {r2_score(y_test, y_pred_lr):.2f}")

# Modelo 2: Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)

print(f"Random Forest MSE: {mean_squared_error(y_test, y_pred_rf):.2f}, "
      f"R2: {r2_score(y_test, y_pred_rf):.2f}")
```

El resultado esperado del JSON es que Random Forest tenga MSE más bajo y R² más cercano a 1.0 que la regresión lineal, demostrando que los ensamblajes capturan mejor las relaciones complejas.

### Qué observar en los resultados

- Un MSE más bajo y un R² más cercano a 1.0 significan que el modelo se aproxima mejor a los precios reales.
- Comparar los dos modelos: el Random Forest suele superar a la regresión lineal cuando hay relaciones no lineales.

## 68-75 min: cierre y monitoreo de deriva con PSI

### Monitoreo en producción (tutorial_2.json, lesson 6)

Explicar que R², MAE y MSE responden a la pregunta "¿qué tan bien funcionó el modelo con los datos de prueba?" — una pregunta que se responde una vez, el día que se entrena. Pero un modelo en producción se ejecuta sobre datos que **cambian** (clientes, precios, mercado).

**PSI (Population Stability Index)** mide cuánto se ha movido la distribución de los datos desde el entrenamiento. Compara dos distribuciones de la misma variable:

- **Población base**: conjunto de entrenamiento o período de referencia estable.
- **Ventana actual**: tráfico de la última semana o mes.

Se puede aplicar a las puntuaciones de salida del modelo o a las variables de entrada. Un PSI alto alerta de que el mundo del que aprendió el modelo ya no existe.

### Checklist de cierre

Preguntar a la clase:

1. ¿Qué diferencia fundamental hay entre el objetivo de clasificación y el de regresión?
2. ¿Por qué no se usa `stratify` en regresión?
3. ¿Qué métrica penaliza más los errores grandes, MSE o MAE?
4. ¿Por qué un bosque aleatorio suele superar a una regresión lineal?
5. ¿Para qué sirve el PSI si ya tenemos R² y MSE?

## Puntos clave para reforzar

- La regresión predice **números**, no categorías; la magnitud del error importa.
- Los modelos aprenden minimizando residuos mediante descenso por gradiente (ciclo predecir-medir-ajustar).
- Los mismos algoritmos de clasificación (árboles, random forest) se adaptan a regresión, pero cambia cómo dividen (minimizar varianza) y cómo predicen (promedio).
- La regresión lineal es rápida e interpretable; Random Forest maneja no linealidades; XGBoost ofrece alta precisión con más ajuste.
- En regresión no hay estratificación al dividir datos.
- R² mide proporción de varianza explicada; MSE penaliza errores grandes al cuadrado.
- El PSI monitorea si la distribución de los datos en producción ha cambiado respecto a los datos de entrenamiento.

## Bloque opcional: series temporales (lectura 4Geeks)

Los contenidos de las lecturas sobre series temporales están disponibles en `class_57/time_series.json` (3 lecciones) y `class_57/exploring_time_series.json` (notebook interactivo). El profesor debe:

1. **Acceder en vivo** a las URLs de 4Geeks para mostrar el contenido directamente desde la plataforma.
2. **Explicar** que las series temporales son un tipo especial de datos donde el tiempo es la dimensión fundamental: cada observación está asociada a un instante específico y existe correlación temporal entre puntos consecutivos.
3. **Relacionar** la regresión con predicción temporal: un modelo de regresión puede usarse para pronosticar valores futuros en una serie temporal si se construyen características basadas en rezagos (lags), tendencia y estacionalidad. Los modelos ARIMA combinan autorregresión (AR), diferenciación (I) y media móvil (MA).
4. **Cubrir** los conceptos del análisis exploratorio de series temporales:
   - **Tendencia**: ¿los datos aumentan/disminuyen con el tiempo? (lineal o no lineal)
   - **Estacionalidad**: ¿hay patrones que se repiten en intervalos regulares?
   - **Variabilidad**: ¿cambia la dispersión de los datos a lo largo del tiempo?
   - **Outliers**: valores extremos que se desvían del patrón general
   - **Autocorrelación**: dependencia entre observaciones pasadas y actuales
   - **Puntos de inflexión**: cambios bruscos en la tendencia
5. **Presentar** los modelos de forecasting:
   - **ARIMA**: autorregresivo, integrado, media móvil — versátil para tendencias y estacionalidad
   - **Suavizado Exponencial**: pesos decrecientes para observaciones más antiguas — simple y eficiente
   - **RNN/LSTM**: deep learning para patrones complejos y relaciones a largo plazo
6. **Recomendar** abrir el notebook de "Exploring Time Series" en Google Colab para la parte práctica: [Colab](https://colab.research.google.com/github/4GeeksAcademy/machine-learning-content/blob/master/06-ml_algos/exploring-time-series.es.ipynb)

