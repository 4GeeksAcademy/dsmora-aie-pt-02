# Clase 58: Evaluar y desplegar modelos de machine learning

## Hilo de continuidad

En la clase 56 se entrenaron clasificadores y se interpretaron métricas como precisión, recall y F1; en la clase 57 se pasó a regresión y a sus métricas. Esta sesión responde dos preguntas que vienen después del entrenamiento: **¿tenemos evidencia de que el modelo generaliza?** y **¿cómo lo trasladamos del experimento a un flujo utilizable?**

La secuencia de esta clase es:

```text
entrenamiento (clases previas)
-> evaluación con datos no vistos
-> diagnóstico de subajuste/sobreajuste
-> elección de métrica y validación cruzada
-> empaquetar modelo + preprocesamiento
-> elegir lote o API y orquestar predicciones
```

Frase de transición sugerida: «Hasta ahora entrenamos modelos; hoy vamos a exigirles evidencia en datos que no han visto y luego veremos qué necesita el modelo para poder usarse fuera del notebook».

## Objetivos

Al finalizar, el estudiante podrá:

- Explicar por qué la puntuación de entrenamiento no basta y distinguir error de entrenamiento de error de generalización.
- Diagnosticar subajuste y sobreajuste comparando errores de entrenamiento y validación, y leer esas señales en curvas de aprendizaje.
- Elegir métricas en función del costo del error: matriz de confusión, precisión, recall, F1, RMSE y R².
- Describir validación cruzada de cinco pliegues y calcular media y desviación estándar de sus puntuaciones.
- Explicar por qué el despliegue incluye preprocesamiento reproducible, serialización, estrategia de servicio y un flujo de ejecución confiable.
- Completar el recorrido del material: guardar y cargar una `Pipeline` de scikit-learn y organizar predicción por lotes con tareas y flujo de Prefect.

## Agenda sugerida: 70 minutos

| Minutos | Bloque | Resultado |
| --- | --- | --- |
| 0–6 | Puente: entrenar no es demostrar | Diferenciar puntuación de entrenamiento y generalización |
| 6–17 | Subajuste, sobreajuste y curvas | Leer las dos brechas de error |
| 17–34 | Métricas que responden al costo del error | Elegir métrica para clasificación y regresión |
| 34–42 | Validación cruzada | Comprender cinco pliegues y su variabilidad |
| 42–49 | De entrenamiento a producción | Identificar cambios de entrada, reproducibilidad, latencia y errores |
| 49–55 | Lotes frente a API | Escoger patrón según cómo se necesitan las predicciones |
| 55–65 | Pipeline serializada y Prefect | Recorrer las tareas prácticas de los dos módulos |
| 65–70 | Síntesis y chequeo | Cerrar con una decisión justificada |

**Versión de 60 minutos:** limitar la sección de métricas a la elección conceptual y la matriz de confusión, tratar validación cruzada en una sola explicación, y recorrer la práctica de despliegue como lectura guiada del flujo sin escribir todo el código.

**Versión de 75 minutos:** añadir cinco minutos para que el grupo resuelva en parejas la elección de métrica y cinco minutos para que complete y explique las tareas `load_model` y `predict_batch`.

## Preparación del instructor

- Tener a mano `class_58/tutorial.json` y `class_58/tutorial_2.json` como evidencia del contenido fuente.
- Para la demostración de evaluación, usar el ejemplo de spam de la introducción: si 98 % de los correos son legítimos, un clasificador que siempre responde «no spam» puede tener 98 % de precisión y no detectar ningún spam.
- Para la actividad de métricas, conservar en pantalla las fórmulas y el caso de cáncer/spam/casas descritos en el material.
- Para el módulo práctico de despliegue, seguir el ejercicio del dataset de cáncer de mama y los nombres de archivo indicados: `app.py` y `model_pipeline.joblib`.
- La fuente presenta retos de código con archivos de ejercicio. No presupone comandos de instalación o una configuración local concreta; si no existe ese entorno, conducir la implementación como lectura de pseudocódigo y recorrido por funciones.

## 0–6 min: abrir el problema — la puntuación de entrenamiento engaña

### Qué decir (literal)

«Un modelo puede obtener 98 % de precisión en entrenamiento y aun así no servir en el mundo real. Si el 98 % de los correos son legítimos, un filtro que diga siempre “no spam” obtiene esa cifra, pero no detecta ni un correo spam. Por eso hoy no vamos a preguntar solamente si el modelo se entrenó: vamos a preguntar qué ocurre con datos nuevos que nunca vio».

Definir con el grupo:

- **Error de entrenamiento:** error sobre los ejemplos usados para ajustar el modelo.
- **Error de generalización:** error sobre datos nuevos y no vistos; es el que interesa para anticipar el comportamiento real.

### Preguntar

- «¿Qué nos dice el 98 % del ejemplo y qué no nos dice?»
- «¿Qué datos necesitamos reservar para estimar cómo va a funcionar el modelo con casos nuevos?»

Respuesta que se busca: el resultado de entrenamiento no demuestra generalización; hace falta evaluar con datos reservados/no vistos.

## 6–17 min: diagnosticar subajuste y sobreajuste

### Explicación y guion

«Comparemos el error del modelo en entrenamiento con el error de validación. Si ambos son altos y cercanos, el modelo puede ser demasiado simple: eso es subajuste. Si el error de entrenamiento es bajo y el de validación alto, hay una brecha grande: el modelo está aprendiendo demasiado bien los ejemplos vistos y no generaliza; eso es sobreajuste».

| Diagnóstico | Entrenamiento | Validación | Lectura del material |
| --- | --- | --- | --- |
| Subajuste | Error alto | Error alto, cercano al de entrenamiento | Modelo demasiado simple para capturar los patrones |
| Sobreajuste | Error bajo | Error alto | Memoriza ruido o ejemplos específicos; falla en datos nuevos |

El material propone como primer remedio del subajuste aumentar la complejidad o mejorar características. Para el sobreajuste, reducir complejidad, usar regularización o reunir más datos de entrenamiento. No presentar esos remedios como garantía automática: primero se diagnostica la forma del error.

### Curvas de aprendizaje

Una curva de aprendizaje grafica el error (o precisión) de entrenamiento y validación frente al tamaño del conjunto de entrenamiento. El eje horizontal es el número de muestras utilizadas y el vertical el error o la pérdida. Se observan dos líneas:

- **Señal de subajuste:** ambas curvas quedan altas y cercanas y se estabilizan temprano; añadir datos no muestra mejora suficiente.
- **Señal de sobreajuste:** el error de entrenamiento baja, pero el de validación permanece alto; persiste una brecha.
- Si la curva de validación sigue mejorando cuando se añaden muestras, el material sugiere que más datos podrían ayudar.

### Qué preguntar

- «Entrenamiento alto y validación alta, casi iguales: ¿subajuste o sobreajuste?» → Subajuste.
- «Entrenamiento bajo y validación alto: ¿qué brecha observas?» → Sobreajuste.
- «¿Qué representan los ejes de una curva de aprendizaje?» → Tamaño del conjunto de entrenamiento y error/pérdida (o precisión).

## 17–34 min: escoger la métrica según el costo del error

### Qué decir (literal)

«Una métrica no es solo un número: define qué llamamos equivocarse. En detección de cáncer puede ser muy costoso dejar pasar un positivo; en spam quizá moleste más mandar un correo legítimo a spam; para precios de casas, un error enorme puede costar mucho más que varios errores pequeños. La métrica se elige por el costo del error antes de comparar resultados».

### Clasificación: matriz de confusión

La matriz de confusión agrupa las predicciones en cuatro cantidades:

- **VP (verdadero positivo):** positivo predicho correctamente.
- **FP (falso positivo):** predicho positivo, pero en realidad negativo.
- **FN (falso negativo):** positivo real que el modelo no detectó.
- **VN (verdadero negativo):** negativo predicho correctamente.

A partir de esos conteos:

```text
precisión = VP / (VP + FP)
recall    = VP / (VP + FN)
F1        = media armónica de precisión y recall
```

- **Precisión** responde: de todos los casos que marqué como positivos, ¿cuántos realmente lo eran?
- **Recall** responde: de todos los positivos reales, ¿cuántos logré detectar?
- **F1** resume precisión y recall mediante su media armónica.

Caso para discutir: en detección de cáncer, pasar por alto un caso positivo (FN) puede ser mortal, así que interesa capturar tantos positivos como sea posible (recall). En un filtro de spam, marcar un mensaje legítimo como spam (FP) perjudica al usuario, así que el material destaca la precisión.

### Regresión: RMSE y R²

La regresión no se resume con acierto/error de clase. Si la casa vale 300.000 y la predicción es 310.000, el error tiene magnitud 10.000. El material propone reportar juntas:

- **RMSE:** raíz del promedio de los errores al cuadrado. Elevar al cuadrado hace que los errores grandes pesen mucho más; la raíz devuelve el resultado a la unidad original (por ejemplo, dólares). Es apropiado cuando los errores grandes cuestan especialmente caro.
- **R²:** indica cuánto mejora el modelo respecto a usar la media como predicción de referencia. Un valor cercano a 1 indica mejor ajuste; 0 equivale a no mejorar esa referencia; puede ser negativo si el modelo es peor que predecir siempre la media.

El RMSE responde «¿qué tan grandes son los errores, penalizando con fuerza los grandes?»; R² responde «¿es bueno el modelo frente a la referencia de la media?». El material señala que conviene acordar la métrica antes del entrenamiento: cambiarla después de ver resultados puede conducir a conclusiones engañosas.

### Mini actividad de decisión (3 minutos)

Pedir al grupo escoger la prioridad y justificar la métrica:

1. Detector de cáncer: evitar falsos negativos → recall.
2. Filtro de spam: reducir correos legítimos marcados como spam → precisión.
3. Precio de vivienda, donde un gran error es catastrófico → RMSE, junto con R² para contexto.

No buscar una métrica «ganadora» para todo: pedir que expliquen qué costo están priorizando.

## 34–42 min: validación cruzada de cinco pliegues

### Qué decir (literal)

«Una sola división de entrenamiento y prueba puede ser un caso afortunado o desafortunado. En validación cruzada k-fold se divide el conjunto en k partes: se entrena y evalúa repetidamente, dejando cada parte fuera una vez. Aquí el ejercicio pide cinco pliegues y una puntuación por pliegue; resumimos las puntuaciones con media y desviación estándar».

En el reto del material, `cross_val_score` recibe el modelo y `X`, `y`, con `cv=5`; devuelve las puntuaciones de los cinco pliegues. `evaluate_model(model, X, y)` debe regresar una tupla `(media, desviación estándar)`, ambas redondeadas a tres decimales. El ejemplo de la lección usa `DecisionTreeClassifier(random_state=0)` con Iris y muestra un resultado de la forma `Accuracy: 0.953 +/- 0.027`.

Código de referencia basado en los requisitos explícitos del ejercicio:

```python
from sklearn.model_selection import cross_val_score


def evaluate_model(model, X, y):
    scores = cross_val_score(model, X, y, cv=5)
    return round(scores.mean(), 3), round(scores.std(), 3)
```

Explicar cada parte: `cross_val_score` obtiene la puntuación de cada pliegue; `cv=5` establece cinco pliegues; `mean()` calcula la media; `std()` resume la dispersión; `round(..., 3)` cumple el formato solicitado. La desviación estándar ayuda a no esconder la variación detrás de un único promedio.

### Preguntar

- «¿Qué información se perdería si reportamos solo la media?» → La dispersión de los resultados entre pliegues.
- «¿Qué significa `cv=5` en el ejercicio?» → Cinco pliegues.

## 42–49 min: qué cambia al pasar a producción

### Qué decir (literal)

«Una buena evaluación es un punto de control, no el despliegue. En producción ya no controlamos las entradas como en el cuaderno, los pasos de preprocesamiento deben repetirse exactamente, la latencia importa y los errores pueden convertirse en respuestas incorrectas silenciosas. El modelo debe viajar con lo necesario para comportarse de forma consistente».

Cuatro cambios que identifica el módulo:

1. **Control de entrada:** en entrenamiento se controla el formato; en producción, los datos llegan de llamadores o sistemas externos y pueden variar.
2. **Preprocesamiento reproducible:** los mismos pasos exactos del entrenamiento deben aplicarse en producción.
3. **Latencia:** en producción puede haber límites estrictos de tiempo para responder.
4. **Manejo de errores:** un fallo puede manifestarse como una respuesta incorrecta silenciosa, no solo como una excepción visible.

Despliegue significa poner el modelo entrenado a disposición de otros sistemas o usuarios para que puedan utilizarlo. La práctica recalca que no basta con guardar los pesos: el artefacto debe incluir los pasos de preprocesamiento.

### Preguntas

- «¿Qué riesgo aparece si producción usa un preprocesamiento distinto del entrenamiento?» → Las entradas dejan de transformarse de forma consistente.
- «¿Qué requisito nuevo aparece cuando el sistema debe responder a solicitudes en vivo?» → Latencia.

## 49–55 min: elegir servicio por lotes o API

Comparar según las tres dimensiones del material:

| Dimensión | Por lotes | Por API |
| --- | --- | --- |
| Latencia | Minutos u horas; el resultado no tiene que ser inmediato | Milisegundos para responder a solicitudes en tiempo real |
| Rendimiento | Alto; puede procesar millones de registros en un trabajo | Menor por instancia; atiende una solicitud a la vez y debe responder rápidamente |
| Disparador | Programa (por ejemplo, nocturno) o evento de datos | Solicitud en vivo de usuario o sistema |

### Qué decir (literal)

«No elegimos por moda. Si necesitamos procesar un gran conjunto a intervalos programados y podemos esperar, lote encaja con ese patrón. Si un usuario o sistema hace una solicitud y espera una predicción inmediata, el patrón descrito es una API».

Pedir a estudiantes que clasifiquen «predicciones nocturnas de un conjunto grande» y «una aplicación pide una predicción ahora». Respuestas: lotes y API, respectivamente.

## 55–65 min: serializar el pipeline y orquestar predicciones

### A. Pipeline serializada (5 minutos)

El ejercicio con cáncer de mama pide cargar el conjunto de scikit-learn, separar entrenamiento/prueba, crear una `Pipeline` con `StandardScaler` (`scaler`) seguido de `RandomForestClassifier` (`clf`), ajustar ambos pasos juntos, guardar el artefacto como `model_pipeline.joblib`, cargarlo de nuevo y medir precisión en la prueba reservada. El resultado esperado de ejemplo termina con una línea similar a `Test accuracy: 0.9649`.

Recorrido del profesor, sin ocultar los pasos:

```text
load_breast_cancer() -> X e y
train_test_split(..., test_size=0.2, random_state=42)
Pipeline([('scaler', StandardScaler()), ('clf', RandomForestClassifier())])
pipe.fit(X_train, y_train)
joblib.dump(pipe, 'model_pipeline.joblib')
loaded_pipe = joblib.load('model_pipeline.joblib')
loaded_pipe.score(X_test, y_test)
```

En la fuente se especifican explícitamente los componentes, nombres de pasos, división, nombre de archivo, guardado/carga y evaluación en el test. El punto de enseñanza es que la tubería incluye escalador y clasificador, de modo que el preprocesamiento se aplica junto con el modelo al reutilizar el artefacto. No interpretar el número de precisión como garantía universal: es el resultado ilustrativo de la división indicada.

### B. Prefect: tarea, tarea, flujo (5 minutos)

El segundo ejercicio define estas responsabilidades:

- `load_model(path)`: deserializar con `joblib` el pipeline guardado en la ruta y devolverlo.
- `predict_batch(model, data)`: ejecutar `model.predict(data)` y devolver las predicciones.
- `run_predictions(model_path, data)`: flujo que invoca primero la carga y después la predicción; imprime una línea por muestra, etiquetando `1` como «benigno» y `0` como «maligno».

El ejemplo del curso marca `load_model` y `predict_batch` con `@task`, y `run_predictions` con `@flow`, importados desde `prefect`. Prefect presenta los pasos como tareas reintentables y observables dentro de un flujo.

Código de referencia, completando las responsabilidades y las etiquetas literalmente indicadas en el ejercicio:

```python
from prefect import flow, task
import joblib


@task
def load_model(path):
    return joblib.load(path)


@task
def predict_batch(model, data):
    return model.predict(data)


@flow
def run_predictions(model_path, data):
    model = load_model(model_path)
    predictions = predict_batch(model, data)
    for index, prediction in enumerate(predictions, start=1):
        label = "benigno" if prediction == 1 else "maligno"
        print(f"Muestra {index}: {label}")
```

Aclarar que es un patrón de ejercicio basado en el material, y que los datos y el pipeline previamente guardado deben estar disponibles para ejecutar un ejemplo real. La fuente muestra `sample_data = [[...]]` como marcador para reemplazar por datos reales: no presentarlo como dato ejecutable.

### Preguntas de comprobación

- «¿Por qué guardar solo el clasificador podría dejar fuera un paso necesario?» → El preprocesamiento que debe reproducirse.
- «¿Qué devuelve `load_model(path)` según el ejercicio?» → El pipeline cargado.
- «¿Qué devuelve `predict_batch(model, data)`?» → Las predicciones del modelo para los datos.
- «¿Qué organiza `run_predictions`?» → Carga, predicción e impresión de una etiqueta por muestra.

## 65–70 min: síntesis y cierre

### Qué decir (literal)

«La evaluación nos da evidencia sobre generalización; las métricas traducen el costo del error; la validación cruzada muestra qué tan estable es la puntuación entre pliegues. Y para llevar el modelo a uso real debemos preservar el preprocesamiento, elegir cómo se servirán las predicciones y organizar los pasos de carga y predicción. Evaluar no es el final: es el control que permite decidir el siguiente paso con evidencia».

### Ticket de salida: una frase por pregunta

1. ¿Qué combinación de errores caracteriza el sobreajuste?
2. ¿Qué métrica priorizarías si lo más costoso es no detectar positivos reales? ¿Por qué?
3. ¿Qué resume la desviación estándar en validación cruzada?
4. ¿Cuándo escogerías lote y cuándo API?
5. ¿Qué debe viajar junto con el modelo para que el preprocesamiento sea consistente?

## Checklist de preparación y contingencia

- [ ] Abrir los dos JSON de clase y ubicar las lecciones de subajuste/sobreajuste, métricas, validación cruzada, serialización y Prefect.
- [ ] Dibujar una tabla de dos filas para contrastar error de entrenamiento/validación.
- [ ] Tener preparadas las tres situaciones de elección de métricas (cáncer, spam, precio de vivienda).
- [ ] Mostrar el esquema de cinco pliegues y el ejemplo de salida media ± desviación estándar.
- [ ] Revisar que los nombres citados sean `model_pipeline.joblib`, `load_model`, `predict_batch`, `run_predictions`, `@task` y `@flow`.
- [ ] Si no está disponible el entorno de ejecución, impartir el código como recorrido de responsabilidades: qué recibe cada función, qué hace y qué devuelve. No inventar instalación, dependencias, resultados ni datos de prueba.
- [ ] Si el tiempo se reduce, mantener el hilo evaluación → decisión de despliegue y recortar la implementación, no la explicación de generalización y elección de métricas.

## Ideas clave para reforzar

- Un resultado alto en entrenamiento no garantiza generalización; la evaluación relevante usa datos no vistos.
- Errores altos y cercanos en entrenamiento/validación sugieren subajuste; bajo en entrenamiento y alto en validación sugieren sobreajuste.
- Las curvas de aprendizaje representan error o precisión frente al tamaño de entrenamiento y permiten observar esas brechas.
- La métrica debe elegirse por el costo real: recall atiende a positivos omitidos; precisión, a falsos positivos; RMSE castiga con fuerza errores grandes; R² compara con la referencia de la media.
- Cinco pliegues producen varias puntuaciones; media y desviación estándar comunican rendimiento y variabilidad.
- Un despliegue necesita el preprocesamiento reproducible y un patrón de servicio que concuerde con la latencia y el volumen.
- La práctica empaqueta el `StandardScaler` y el clasificador en una `Pipeline`; la práctica de Prefect organiza carga y predicción como tareas dentro de un flujo.

## Fuentes de contenido

- `class_58/tutorial.json`: evaluación, ajuste, curvas de aprendizaje, métricas y validación cruzada.
- `class_58/tutorial_2.json`: transición a producción, lotes/API, serialización de pipeline y orquestación con Prefect.
