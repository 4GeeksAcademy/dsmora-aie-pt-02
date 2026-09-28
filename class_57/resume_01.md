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

### Contraste con clasificación

Recordar que en clasificación las métricas (accuracy, precisión, recall) comparan si la predicción coincide exactamente con la clase real. Eso no funciona en regresión porque la variable objetivo es continua: ningún modelo acierta el valor exacto, la pregunta es **qué tan cerca** estuvo.

### R² (Coeficiente de Determinación)

**Fórmula** (mostrarla en la pizarra o pantalla):

```
R² = 1 - (SS_res / SS_tot)

SS_res = Σ(y_i - ŷ_i)²     ← suma de cuadrados de los residuos
SS_tot = Σ(y_i - ȳ)²       ← suma de cuadrados respecto a la media
```

Donde:
- `y_i` = valor real
- `ŷ_i` = valor predicho por el modelo
- `ȳ` = media de todos los valores reales

**Intuición pedagógica paso a paso**:

1. **Modelo naive (línea base)**: Imagina que no tienes modelo y solo dices "el precio medio de todas las casas". Eso es `SS_tot` — cuánto error tendrías si siempre predijeras la media.
2. **Tu modelo**: `SS_res` es el error que comete tu modelo.
3. **R² responde**: ¿qué fracción del error del modelo naive eliminaste?

**Ejemplo concreto para la pizarra**:

| Casa | Precio real | Precio medio (naive) | Predicción del modelo |
|------|-------------|---------------------|----------------------|
| A | 200.000 € | 180.000 € | 195.000 € |
| B | 160.000 € | 180.000 € | 165.000 € |
| C | 180.000 € | 180.000 € | 178.000 € |

- `SS_tot` = (200k-180k)² + (160k-180k)² + (180k-180k)² = 400M + 400M + 0 = **800M**
- `SS_res` = (200k-195k)² + (160k-165k)² + (180k-178k)² = 25M + 25M + 4M = **54M**
- `R² = 1 - 54M/800M = 1 - 0.0675 = **0.9325`**

El modelo explica el **93,25 %** de la variabilidad de los precios.

**Posibles valores de R²**:

| Valor | Significado |
|-------|-------------|
| **1.0** | El modelo predice perfectamente (sin errores). |
| **0.9** | El modelo explica el 90 % de la variabilidad. Muy bueno. |
| **0.0** | El modelo no mejora respecto a predecir siempre la media. |
| **Negativo** | El modelo es peor que predecir siempre la media. ¡Algo va mal! |

**Pregunta para la clase**: "Si R² = 0.75, ¿qué porcentaje de la variabilidad NO explica el modelo?" → 25 %.

### MAE (Error Absoluto Medio)

**Fórmula**:

```
MAE = (1/n) * Σ|y_i - ŷ_i|
```

**Intuición**: "En promedio, ¿por cuánto me equivoco?"

**Ejemplo concreto**: Si el MAE de un modelo de precios de casas es 12.500 €, significa que en promedio el modelo se equivoca por 12.500 € — a veces por encima, a veces por debajo.

**Ventaja**: Está en la misma unidad que la variable objetivo (euros, kilovatios, minutos), lo que facilita la interpretación.

**Desventaja**: Trata todos los errores por igual (no penaliza más los errores grandes).

### MSE (Error Cuadrático Medio)

**Fórmula**:

```
MSE = (1/n) * Σ(y_i - ŷ_i)²
```

**Intuición**: Promedio de los errores al cuadrado. No tiene una interpretación directa en euros porque las unidades están al cuadrado (€²).

**Propiedad clave**: penaliza desproporcionadamente los errores grandes.

**Ejemplo comparativo MAE vs MSE** (mostrar en pizarra):

Dos modelos A y B para el mismo problema (predecir 3 casas):

| Casa | Real | Modelo A | Error A | Modelo B | Error B |
|------|------|----------|---------|----------|---------|
| 1 | 100 € | 105 € | 5 € | 100 € | 0 € |
| 2 | 100 € | 95 € | 5 € | 100 € | 0 € |
| 3 | 100 € | 100 € | 0 € | 200 € | 100 € |

```
MAE_A = (5+5+0)/3 = 3.33 €
MAE_B = (0+0+100)/3 = 33.33 €

MSE_A = (25+25+0)/3 = 16.67
MSE_B = (0+0+10000)/3 = 3333.33
```

El MAE dice que B es 10 veces peor que A. El MSE dice que B es **200 veces peor**. ¿Cuál métrica tiene razón? Las dos, pero el MSE castiga severamente ese error catastrófico de 100 €, mientras que MAE lo trata como "10 veces peor". Depende del caso de negocio: si un error de 100 € puede significar una pérdida inasumible, el MSE captura mejor ese riesgo.

**Pregunta conceptual del JSON para lanzar a la clase**:

> Un modelo predice 200 € para un artículo que cuesta 100 €, y 105 € para otro que cuesta 100 €. ¿Cómo trata el MSE estos errores?

**Respuesta**: "MSE penaliza 100 veces más la predicción de 200 € porque el error se eleva al cuadrado (100² = 10.000 vs 5² = 25)."

### RMSE (Raíz del MSE) — mención breve

```
RMSE = √(MSE)
```

Vuelve a las unidades originales (euros). Es el "desvío típico de los errores". Si el RMSE es 15.000 €, en promedio los errores rondan los 15.000 €, pero con mayor sensibilidad a outliers que el MAE.

### Tabla resumen de métricas

| Métrica | Fórmula | Unidad | Sensible a outliers | Fácil de interpretar |
|---------|---------|--------|---------------------|---------------------|
| **R²** | 1 - SS_res/SS_tot | Sin unidad (proporción) | No directamente | Sí (es un %) |
| **MAE** | promedio de \|error\| | Misma que objetivo | No | Sí |
| **MSE** | promedio de error² | Objetivo al cuadrado | **Mucho** | No tanto |
| **RMSE** | √(MSE) | Misma que objetivo | Sí | Bastante |

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
- R² responde: ¿qué fracción de la variabilidad total explica mi modelo? Va de 1.0 (perfecto) a negativo (peor que la media). Fórmula: 1 - SS_res/SS_tot.
- MSE penaliza errores grandes al cuadrado: un error de 100 € se penaliza 10.000 veces más que uno de 1 €. Ideal cuando errores grandes son inaceptables.
- MAE es el error promedio absoluto en las mismas unidades que el objetivo. Fácil de interpretar pero trata todos los errores por igual.
- RMSE es la raíz cuadrada del MSE — vuelve a unidades originales pero mantiene sensibilidad a outliers.
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

