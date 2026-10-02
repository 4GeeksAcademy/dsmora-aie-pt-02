# Clase 59: Hiperparámetros y optimización de modelos

> Guía docente elaborada a partir de `tutorial.json` y `tutorial_2.json`, generados con `scripts/scraper.py`. La primera fuente contiene 6 lecciones y la segunda 8. Las actividades, tiempos y frases docentes organizan el material; los conceptos, APIs, valores de ejemplo y ejercicios técnicos que aparecen abajo proceden de esos JSON.

## Hilo de continuidad

La secuencia comienza distinguiendo qué aprende el modelo de qué configuración elige quien entrena. El primer LearnPack explica hiperparámetros por familia de modelo y cómo solicitar a un LLM un espacio de búsqueda útil. El segundo lleva esa idea a búsquedas ejecutables sobre el dataset de cáncer de mama: primero `GridSearchCV`, después `RandomizedSearchCV`, selección del mejor estimador, `Pipeline` para el preprocesamiento y evaluación sobre datos de prueba.

Frase de transición sugerida: «Hasta ahora hemos entrenado modelos y evaluado su rendimiento. Hoy vamos a pasar de los valores predeterminados y la conjetura a una búsqueda de hiperparámetros que tenga una métrica, un espacio y un costo que podamos explicar».

## Objetivos

Al finalizar, el estudiante podrá:

- Diferenciar los parámetros aprendidos durante `fit` de los hiperparámetros elegidos antes del entrenamiento.
- Reconocer ejemplos de hiperparámetros para árboles, Random Forest, Gradient Boosting/XGBoost y modelos lineales mencionados en el material.
- Definir qué contexto proporcionar a un LLM para que proponga un espacio de búsqueda pertinente y revisar críticamente la propuesta.
- Explicar cómo `GridSearchCV` y `RandomizedSearchCV` prueban candidatos y cómo estimar el costo de la búsqueda.
- Ejecutar el patrón de búsqueda de malla indicado en el reto: `RandomForestClassifier`, cáncer de mama, cinco pliegues y métrica F1.
- Describir por qué el reto de búsqueda aleatoria pone `StandardScaler` y el modelo dentro de una `Pipeline`.
- Interpretar `best_params_`, `best_score_`, `best_estimator_` y `cv_results_`, y usar el conjunto de prueba para evaluar el ganador.

## Agenda sugerida: 70 minutos

| Minutos | Bloque | Resultado |
| --- | --- | --- |
| 0–5 | Apertura: de los valores predeterminados a la sintonización | Enmarcar la necesidad de ajustar sistemáticamente |
| 5–15 | Parámetros e hiperparámetros | Distinguir lo aprendido de lo configurado |
| 15–25 | Hiperparámetros por familia y espacio de búsqueda | Relacionar controles, efecto y contexto del problema |
| 25–35 | LLM como ayuda para proponer candidatos | Preparar una solicitud con contexto y revisar su respuesta |
| 35–47 | `GridSearchCV` y costo | Comprender la búsqueda exhaustiva y el reto de cinco pliegues |
| 47–58 | `RandomizedSearchCV` y `Pipeline` | Comparar estrategia y mantener el preprocesamiento dentro de CV |
| 58–66 | Selección y evaluación del ganador | Interpretar atributos y reservar test para evaluación |
| 66–70 | Cierre | Verificar comprensión y resumir el flujo |

**Para 60 minutos:** reducir el bloque de familias de modelos y hacer la revisión del prompt del LLM en formato oral. Mantener el ejemplo `GridSearchCV`, el flujo de búsqueda aleatoria con `Pipeline` y la diferencia entre validación y prueba.  
**Para 75 minutos:** ampliar la actividad de espacio de búsqueda y dedicar tiempo a leer `cv_results_` y contrastar media F1 con variabilidad entre pliegues.

## Preparación del profesor

- Ejecutar/revisar los cursos en los enlaces proporcionados y tener a mano `class_59/tutorial.json` y `class_59/tutorial_2.json`.
- El reto `1.1 Ejecutar búsqueda en malla` indica trabajar en `solution.py`; el reto `2.2 Ejecutar búsqueda aleatoria y seleccionar el mejor` también usa `solution.py`.
- El primer reto pide cáncer de mama, división train/test con `test_size=0.2` y `random_state=42`, `RandomForestClassifier`, rejilla sobre `n_estimators` y `max_depth`, `cv=5` y `scoring='f1'`; solicita imprimir mejores parámetros y mejor F1 CV a cuatro decimales.
- El segundo reto pide `Pipeline` con pasos llamados `'scaler'` y `'model'`, hiperparámetros prefijados por `model__`, y `RandomizedSearchCV(n_iter=20, scoring='f1', cv=5, random_state=42)`. Pide imprimir parámetros, F1 CV a cuatro decimales y precisión en test.
- Los JSON presentan resultados orientativos como `0.96xx` y `0.95xx`; no fijar una cifra exacta: depende de la ejecución y de los valores de la distribución.
- Hay una limitación del scraping: el título guardado para el índice 3 de `tutorial_2.json` dice «Búsqueda aleatoria», pero el texto de esa entrada está desalineado y contiene la lección «Seleccionando el mejor modelo». El índice 4 tiene la misma lección repetida. Para esta parte, usar el reto índice 5 y el texto de cierre/selección registrado en los JSON, y no atribuir contenido distinto a esa lección duplicada.

## 0–5 min: apertura

### Qué decir (literal)

«Los valores predeterminados permiten empezar, pero el curso nos recuerda que no necesariamente son la mejor opción para el dataset o el objetivo de negocio. Ajustar a mano puede convertirse en conjetura. Hoy vamos a definir qué queremos probar y a comparar configuraciones de forma sistemática».

El primer tutorial ilustra esta idea con `RandomForestClassifier` y `n_estimators=100`, que podría ser demasiado grande para un conjunto pequeño, y con Ridge y `alpha=1.0`, que podría regularizar demasiado o demasiado poco según los datos.

### Preguntar

- «¿Por qué un valor predeterminado razonable no garantiza el mejor rendimiento para nuestro problema?»
- «¿Qué información hace falta antes de decidir qué explorar?»

## 5–15 min: parámetros vs. hiperparámetros

### Explicación para el profesor

- **Parámetros del modelo:** valores que el algoritmo aprende de los datos durante el entrenamiento (`fit`); el JSON da como ejemplos los coeficientes de regresión lineal y los umbrales de división de un árbol.
- **Hiperparámetros:** configuraciones que se eligen antes del entrenamiento para orientar cómo aprende el modelo; el JSON da `max_depth` para limitar un árbol, `n_estimators` para indicar cuántos árboles tendrá un Random Forest y `alpha` para la fuerza de regularización de Ridge.

El curso de optimización da ejemplos adicionales: SVM usa `C` y `kernel`; gradient boosting añade `learning_rate`. Los controles disponibles dependen del algoritmo; no son intercambiables entre todos los modelos.

### Qué decir (literal)

«El algoritmo descubre los parámetros a partir de los datos. En cambio, nosotros configuramos los hiperparámetros para influir en cómo aprende. Por eso un umbral aprendido en un árbol no es lo mismo que el límite `max_depth` que damos antes de entrenarlo».

### Chequeo rápido

- «¿Los coeficientes de una regresión lineal son parámetros o hiperparámetros?» → Parámetros aprendidos.
- «¿Y `max_depth` establecido antes del ajuste?» → Hiperparámetro.

## 15–25 min: qué controles importan según el modelo

Usar las relaciones descritas por el curso, no convertirlas en una lista universal de valores:

- **Árboles y Random Forest:** `max_depth` controla profundidad; demasiado alto puede memorizar (sobreajuste), demasiado bajo puede dejar al modelo simple (subajuste). `n_estimators` indica cuántos árboles; más árboles pueden estabilizar, con rendimientos decrecientes y más cómputo. `min_samples_split` y `min_samples_leaf` elevan el mínimo de muestras para divisiones/hojas y añaden regularización.
- **Gradient Boosting/XGBoost:** el curso incluye esta familia entre los tipos de modelo a considerar al seleccionar hiperparámetros.
- **Modelos lineales:** `alpha` en Ridge controla la fuerza de regularización.
- **SVM:** el curso menciona `C` y `kernel`.

### Preguntar

- «¿Qué riesgo plantea una profundidad demasiado alta y cuál una demasiado baja?» → Sobreajuste y subajuste, respectivamente.
- «¿Qué costo puede aumentar al añadir árboles?» → El cómputo; los beneficios tienen rendimientos decrecientes.

## 25–35 min: diseñar el espacio de búsqueda con ayuda de un LLM

El material define un **espacio de búsqueda** como el conjunto de valores candidatos para cada hiperparámetro que explorará el proceso de optimización. Para que el LLM proponga opciones contextualizadas, recomienda incluir:

1. Tipo de modelo (ejemplo fuente: `RandomForestClassifier`).
2. Tamaño del dataset y número de características.
3. Balance de clases en clasificación.
4. Objetivo de negocio y métrica (ejemplo: maximizar recall).
5. Restricciones, como presupuesto de tiempo de entrenamiento.

El primer tutorial da este prompt literal para una clasificación binaria de 50K filas, 30 características, 10% de clase positiva y prioridad de recall. Presentarlo como **ejemplo de prompt del curso**, no como datos del reto de cáncer de mama:

```text
Estoy entrenando un RandomForestClassifier en un problema de clasificación binaria con 50K filas, 30 características y un desequilibrio significativo de clases (10% positivo). Mi objetivo de negocio es maximizar el recall. ¿Qué hiperparámetros debería ajustar y qué rangos recomendarías?
```

El material muestra como posible respuesta un espacio de cuatro hiperparámetros; úsalo solo como el ejemplo de la lección:

```python
search_space = {
    "max_depth": [3, 5, 10, None],
    "n_estimators": [50, 100, 200],
    "class_weight": ["balanced", None],
    "min_samples_leaf": [1, 5, 10],
}
```

La lección dice que un LLM puede priorizar de 3 a 5 hiperparámetros; recomienda evitar rejillas demasiado amplias (da como advertencia cinco parámetros con cinco valores cada uno, que producen miles de combinaciones y largos tiempos). También subraya que la métrica de búsqueda debe reflejar el objetivo de negocio; para maximizar recall en detección de fraude, menciona `scoring='recall'` o un evaluador personalizado que penalice más los falsos negativos.

### Actividad guiada

Pedir al grupo que identifique qué elementos hacen útil la solicitud y qué debería revisar antes de aceptar la respuesta: que el hiperparámetro corresponda al estimador, que la métrica responda al objetivo, que el espacio sea acotado y que el cómputo quepa en el presupuesto. El material plantea el LLM como apoyo para proponer; la búsqueda y su evaluación son las que comparan candidatos.

### Qué decir (literal)

«No le pedimos al modelo de lenguaje una lista sin contexto. Le damos el algoritmo, el tamaño y forma de los datos, el balance, la métrica que importa y nuestras restricciones. La propuesta sigue siendo un espacio candidato que debemos evaluar».

## 35–47 min: búsqueda en cuadrícula (`GridSearchCV`)

### Idea

`GridSearchCV` recibe un estimador y una rejilla (diccionario de hiperparámetros), evalúa cada combinación con validación cruzada y permite localizar la combinación con mejor puntuación según el criterio elegido. La lección la describe como búsqueda exhaustiva dentro de una cuadrícula pequeña y definida.

### Ejercicio fuente: búsqueda de malla

El reto de LearnPack pide completar `solution.py` para:

- Cargar el dataset de cáncer de mama con `load_breast_cancer()` y separar entrenamiento/prueba usando `train_test_split(..., test_size=0.2, random_state=42)`.
- Usar `RandomForestClassifier` y definir una rejilla para `n_estimators` y `max_depth`.
- Crear `GridSearchCV` con `cv=5` y `scoring='f1'`.
- Ajustar la búsqueda con los datos de entrenamiento.
- Imprimir `best_params_` y el mejor F1 medio de validación cruzada redondeado a cuatro decimales.

El material muestra como salida ilustrativa: `Best parameters: {'max_depth': 5, 'n_estimators': 100}` y `Best CV score (F1): 0.96xx`. No tratar ese ejemplo como resultado que deba coincidir exactamente en todos los entornos.

### Costo de la búsqueda

La lección introductoria de optimización pide aprender a calcular el costo de búsquedas. Para explicarlo, contar las combinaciones explícitas de la rejilla y multiplicar por el número de pliegues. Ejemplo aritmético ilustrativo del docente: si la cuadrícula especifica 2 valores para `n_estimators` y 3 para `max_depth`, son 6 candidatos; con `cv=5`, son 30 evaluaciones de pliegue. No asignar a este ejemplo esos valores como la rejilla del reto: el JSON no especifica las listas concretas.

**Límite del contenido scrapeado:** el código del reto conserva `param_grid = { # your values here }`, y no se ven las listas de candidatos; el resumen no inventa rangos. El ejemplo de salida sí muestra la pareja ilustrativa `{'max_depth': 5, 'n_estimators': 100}`. El enunciado y el esqueleto anterior contienen los pasos completos para guiar la implementación sin fingir una solución exacta que no está en la fuente.

## 47–58 min: búsqueda aleatoria y pipeline

### Comparación

`RandomizedSearchCV` muestrea combinaciones aleatorias y el curso lo recomienda para espacios más grandes o continuos. Frente a evaluar exhaustivamente cada combinación de una cuadrícula, en el reto el presupuesto se controla con `n_iter=20`.

### Ejercicio fuente: búsqueda aleatoria, `Pipeline` y test

El reto `2.2` pide:

- Cargar cáncer de mama y dividir train/test.
- Construir una `Pipeline` con `StandardScaler` como paso `scaler` y `RandomForestClassifier` como paso `model`.
- Definir una distribución con `model__n_estimators`, `model__max_depth` y `model__min_samples_split`.
- Usar `RandomizedSearchCV` con `n_iter=20`, `scoring='f1'`, `cv=5` y `random_state=42`; ajustar con datos de entrenamiento.
- Tomar `best_estimator_`, evaluarlo en test e imprimir mejores parámetros, F1 CV a cuatro decimales y precisión en test.

El prefijo `model__` identifica hiperparámetros del paso llamado `model` en la tubería, según la convención que aparece explícitamente en el reto. La `Pipeline` empaca el escalador y el modelo para que el preprocesamiento forme parte de cada ajuste de validación cruzada; el curso indica que esto evita leakage en preprocessing y mantiene la validación honesta.

El esqueleto scrapeado además indica las piezas de implementación: `Pipeline([('scaler', StandardScaler()), ('model', RandomForestClassifier())])`, `RandomizedSearchCV(pipe, param_dist, n_iter=20, scoring='f1', cv=5, random_state=42)`, `fit(X_train, y_train)`, `best_estimator_` y `accuracy_score(y_test, best_estimator_.predict(X_test))`. Los rangos de `param_dist` aparecen como `# your values here`; no se completan con valores inventados.

### Qué decir (literal)

«La cuadrícula intenta todas las combinaciones que escribimos. La búsqueda aleatoria limita el número de candidatos muestreados. En este ejercicio, además, el escalador viaja dentro de la tubería con el modelo: así el preprocesamiento participa correctamente en cada pliegue de la validación».

### Qué preguntar

- «¿Qué fija `n_iter=20`?» → El número de candidatos muestreados para la búsqueda aleatoria.
- «¿Por qué los parámetros empiezan con `model__`?» → Porque son del paso `model` de la `Pipeline`.
- «¿Qué métrica optimiza este reto?» → F1 durante la búsqueda; después reporta también accuracy en test.

## 58–66 min: seleccionar el ganador y evaluarlo

Explicar las salidas que nombran los JSON:

- `best_params_`: diccionario de hiperparámetros ganadores.
- `best_score_`: mejor puntuación promedio de validación cruzada (en los retos, F1 porque `scoring='f1'`).
- `best_estimator_`: modelo con esos parámetros; con `refit=True`, valor predeterminado descrito por el curso, vuelve a ajustarse sobre todos los datos de entrenamiento entregados a la búsqueda.
- `cv_results_`: resultados de cada candidato y cada pliegue; permite observar media y variación/desviación estándar.

El curso recomienda no quedarse solo con la media: una puntuación media un poco menor con variabilidad mucho más ajustada puede reflejar mayor consistencia entre pliegues que un ganador de media alta pero variable. Luego, el reto evalúa `best_estimator_` sobre el conjunto de prueba. El material de cierre insiste en reservar test para la evaluación rigurosa y usar CV/métricas para la sintonización.

### Preguntas de comprobación

- «¿Qué atributo me devuelve el modelo entrenado que ganó?» → `best_estimator_`.
- «¿Dónde miro resultados por candidato y pliegue?» → `cv_results_`.
- «¿Por qué no debo usar el test para seleccionar repetidamente la búsqueda?» → Porque el curso lo reserva para evaluar la configuración ajustada, separado de la sintonización.

## 66–70 min: cierre

### Qué decir (literal)

«Hoy conectamos una idea con una práctica: los hiperparámetros son decisiones nuestras; el espacio de búsqueda expresa qué candidatos vamos a considerar; Grid Search prueba la cuadrícula y Random Search limita el muestreo. La `Pipeline` protege el preprocesamiento durante la validación, y los atributos de la búsqueda nos ayudan a entender tanto el ganador como su estabilidad. Cerramos evaluando el modelo elegido con los datos de prueba reservados».

### Ticket de salida

1. Da un ejemplo de parámetro aprendido y otro de hiperparámetro.
2. ¿Qué ventaja y qué costo tiene probar todos los puntos de una cuadrícula?
3. ¿Qué se fija con `n_iter` en el reto aleatorio?
4. ¿Qué información adicional aporta `cv_results_` frente a mirar solo el mejor resultado?
5. ¿Cuál es el papel del conjunto de prueba después de la búsqueda?

## Checklist docente

- [ ] Confirmar los rangos actuales del reto para `n_estimators`, `max_depth` y la distribución aleatoria; ambos códigos scrapeados muestran marcadores `your values here` en lugar de las listas.
- [ ] Distinguir claramente valores ejemplificados en la lección (50K/30/10% para el prompt LLM) de los datos del reto (dataset de cáncer de mama).
- [ ] Presentar la salida `0.96xx`/`0.95xx` como orientativa, no como cifra garantizada.
- [ ] Para mostrar fuga del preprocesamiento, mantenerse en lo dicho por la fuente: el escalador y el estimador se empaquetan en la `Pipeline` que participa en CV.
- [ ] Reconocer la duplicación/desalineación de la lección de selección de modelo en los índices 3 y 4 de `tutorial_2.json`; usar el contenido repetido como una sola explicación.
- [ ] Si no se puede ejecutar el entorno, recorrer las instrucciones y explicar el propósito de cada parámetro sin inventar una salida adicional.

## Nota de calidad de fuentes

- `tutorial.json`: 6 lecciones sobre valores predeterminados, parámetros vs. hiperparámetros, controles según familia de modelos, definición de espacio de búsqueda con LLM, assessment y conclusión.
- `tutorial_2.json`: 8 lecciones sobre Grid Search, búsqueda aleatoria, selección del mejor modelo, ejecución de los dos retos, evaluación y cierre.
- El scraper guardó en inglés los títulos de algunas lecciones del primer tutorial aunque el contenido textual está en español. En el segundo tutorial, la entrada con título «Búsqueda aleatoria» contiene texto de selección del mejor modelo, duplicado en la siguiente entrada; esa limitación se documenta arriba para no sobreinterpretar el orden.
