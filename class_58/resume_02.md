# Clase 58 — Resumen del tutorial 2: Despliegue de modelos

## Idea central

Entrenar y evaluar un modelo no basta para que genere valor: hay que ponerlo a disposición de usuarios o sistemas de forma confiable. El despliegue conecta el modelo experimental con su uso en producción. Para ello, el artefacto debe conservar el preprocesamiento, ofrecer una forma de entregar predicciones y contar con un flujo operativo reproducible.

## Del entrenamiento a producción

Al salir del cuaderno de experimentación cambian varias condiciones:

- **Las entradas son menos controlables:** llegan desde usuarios o sistemas externos y pueden variar.
- **El preprocesamiento debe ser reproducible:** producción debe aplicar los mismos pasos que se usaron durante el entrenamiento.
- **La latencia importa:** puede haber límites de tiempo para devolver una predicción.
- **Los errores requieren atención:** en producción un problema puede producir respuestas incorrectas sin una excepción evidente.

Por eso, el despliegue no consiste únicamente en guardar los pesos del modelo. También hay que empaquetar los pasos necesarios para transformar las entradas y ejecutar predicciones consistentemente.

## Elegir cómo servir las predicciones

El tutorial compara dos patrones:

| Aspecto | Servicio por lotes | Servicio por API |
| --- | --- | --- |
| Cuándo se ejecuta | Según un horario o cuando llega un evento de datos | Cuando un usuario o sistema envía una solicitud en vivo |
| Latencia esperada | Minutos u horas; no se necesita respuesta inmediata | Respuesta rápida, normalmente en milisegundos |
| Tipo de carga | Procesa grandes volúmenes, incluso millones de registros por trabajo | Atiende solicitudes individuales y prioriza responder pronto |

La elección depende de cómo se consumen las predicciones: lotes para trabajos programados y voluminosos; API para solicitudes que necesitan una respuesta inmediata.

## Empaquetar y serializar una pipeline

La práctica utiliza el conjunto de cáncer de mama de scikit-learn. El objetivo es crear una pipeline con dos pasos:

1. `StandardScaler` para escalar las características.
2. `RandomForestClassifier` para realizar la clasificación.

Se separan los datos en entrenamiento y prueba, se ajusta la pipeline con los datos de entrenamiento y se guarda el artefacto completo en `model_pipeline.joblib` mediante `joblib`. Después se carga desde disco y se evalúa con el conjunto de prueba reservado. El resultado esperado muestra una confirmación de guardado/carga y una precisión con cuatro decimales, por ejemplo `Test accuracy: 0.9649`.

La ventaja de serializar la pipeline completa es que el escalado acompaña al clasificador: al reutilizarla, las entradas pasan por el mismo preprocesamiento antes de obtener predicciones.

## Orquestar la predicción con Prefect

El último ejercicio divide el proceso en tareas y un flujo:

- `load_model(path)`: carga y devuelve la pipeline serializada con `joblib`.
- `predict_batch(model, data)`: ejecuta `model.predict(data)` y devuelve las predicciones.
- `run_predictions(model_path, data)`: coordina la carga y la predicción, e imprime una línea por muestra.

En Prefect, las dos primeras funciones se marcan como tareas con `@task` y la función coordinadora como flujo con `@flow`. El ejercicio muestra cómo etiquetar la predicción `1` como **benigno** y la `0` como **maligno**. Organizar los pasos así favorece la observabilidad y permite gestionar reintentos.

## Ejemplo completo para explicar en clase

Este ejemplo reúne el recorrido del tutorial en un solo archivo: carga los datos de cáncer de mama, entrena y guarda una pipeline, vuelve a cargarla, evalúa el conjunto de prueba y usa Prefect para predecir cinco muestras.

Instala las dependencias si el entorno aún no las tiene:

```bash
pip install scikit-learn joblib prefect
```

Guarda el siguiente código como `app.py` y ejecútalo con `python app.py`:

```python
import joblib
from prefect import flow, task
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_PATH = "model_pipeline.joblib"


@task
def load_model(path):
    """Carga desde disco la pipeline serializada."""
    return joblib.load(path)


@task
def predict_batch(model, data):
    """Predice las etiquetas para un grupo de muestras."""
    return model.predict(data)


@flow
def run_predictions(model_path, data):
    """Coordina la carga del modelo y la predicción del lote."""
    model = load_model(model_path)
    predictions = predict_batch(model, data)

    for number, prediction in enumerate(predictions, start=1):
        label = "benigno" if prediction == 1 else "maligno"
        print(f"Muestra {number}: {label}")


def main():
    # 1. Cargar los datos y reservar una parte para evaluar el modelo.
    dataset = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        dataset.data,
        dataset.target,
        test_size=0.2,
        random_state=42,
        stratify=dataset.target,
    )

    # 2. Empaquetar preprocesamiento y clasificador en una sola pipeline.
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(random_state=42)),
        ]
    )

    # 3. Ajustar la pipeline solo con los datos de entrenamiento.
    pipeline.fit(X_train, y_train)

    # 4. Guardar el artefacto completo y cargarlo de nuevo desde disco.
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Pipeline guardada en {MODEL_PATH}")
    loaded_model = joblib.load(MODEL_PATH)
    print("Pipeline cargada correctamente")

    # 5. Evaluar el modelo cargado con datos que no se usaron para entrenar.
    test_predictions = loaded_model.predict(X_test)
    accuracy = accuracy_score(y_test, test_predictions)
    print(f"Test accuracy: {accuracy:.4f}")

    # 6. Ejecutar el flujo de Prefect con las primeras cinco muestras de prueba.
    run_predictions(MODEL_PATH, X_test[:5])


if __name__ == "__main__":
    main()
```

### Cómo recorrerlo en clase

1. **Separación de datos:** `train_test_split` reserva ejemplos que el modelo no verá durante el ajuste. `random_state` permite repetir la misma división; `stratify` conserva la proporción de las clases.
2. **Pipeline:** al llamar a `fit`, `StandardScaler` aprende las transformaciones del conjunto de entrenamiento y el clasificador aprende a partir de los datos escalados. Al predecir, la pipeline aplica automáticamente ese mismo escalado.
3. **Serialización:** `joblib.dump` guarda tanto el escalador como el clasificador. `joblib.load` demuestra que el artefacto se puede recuperar.
4. **Evaluación:** la precisión se calcula sobre `X_test` y `y_test`, que quedaron fuera del entrenamiento.
5. **Prefect:** `@task` identifica las operaciones de carga y predicción; `@flow` las organiza y presenta una etiqueta por muestra. En este conjunto, `1` corresponde a benigno y `0` a maligno.

**Preguntas para el grupo:** ¿por qué guardamos la pipeline completa y no solo el clasificador? ¿Por qué evaluamos con `X_test`? ¿Qué cambiaríamos si las predicciones se solicitaran individualmente en tiempo real en vez de procesarse como un lote?

**Nota didáctica:** el archivo combina entrenamiento y predicción para que la demostración sea ejecutable de principio a fin. En un sistema real, el entrenamiento suele ejecutarse aparte; el servicio de producción carga un artefacto ya entrenado y predice con él.

## Recorrido completo

```text
Datos de entrenamiento
    → pipeline (escalado + clasificador)
    → ajuste y serialización: model_pipeline.joblib
    → carga del modelo
    → predicción por lotes
    → resultado etiquetado por muestra
```

## Para recordar

- Desplegar es hacer que un modelo entrenado pueda ser utilizado de manera confiable por otros sistemas o usuarios.
- El modelo debe viajar con su preprocesamiento para evitar diferencias entre entrenamiento y producción.
- Lotes y API responden a necesidades distintas de volumen, disparador y latencia.
- Serializar permite guardar y recuperar la pipeline completa.
- Prefect organiza la carga y la predicción en tareas dentro de un flujo observable y con capacidad de reintento.
