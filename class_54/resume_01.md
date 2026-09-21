# Clase 54: aprendizaje automatico, redes neuronales y modelos preentrenados

## Trazabilidad y hilo de continuidad

Esta clase introduce el aprendizaje automatico, presenta las redes neuronales y termina con la integracion de un modelo preentrenado en un proyecto de analisis de sentimiento. El hilo conductor es: «Primero entendemos que aprende un modelo, despues vemos una familia de modelos neuronales y finalmente usamos un modelo ya entrenado sin construirlo desde cero».

Esta guia se basa exclusivamente en `tutorial.json`, `tutorial_2.json`, `tutorial_3.json` y `ai-eng-sentiment-analysis-reviews_project_README.es.md`. La agenda, las preguntas, las frases literales y la organizacion temporal son estructura docente añadida. Los materiales no contienen prompts de OpenClaw ni comandos de ejecucion concretos; por eso no se inventan.

## Objetivos

- Explicar que es el aprendizaje automatico y como aprende una maquina a partir de datos.
- Distinguir aprendizaje supervisado, no supervisado y otros paradigmas.
- Describir una red neuronal y relacionarla con tareas practicas.
- Explicar que es un modelo preentrenado, como encontrarlo y como evaluarlo.
- Integrar `nlptown/bert-base-multilingual-uncased-sentiment` para clasificar reseñas.
- Comparar el sentimiento escrito con el promedio de 4.5 estrellas e identificar falsos negativos.

## Agenda de 60-75 minutos

| Tiempo | Bloque | Resultado |
| --- | --- | --- |
| 0-8 | Pregunta de negocio y aprendizaje automatico | Enmarcar el problema |
| 8-20 | Como aprenden las maquinas | Datos, patrones y prediccion |
| 20-30 | Tipos de aprendizaje | Elegir el paradigma |
| 30-41 | Redes neuronales | Entender la familia de modelos |
| 41-55 | Modelos preentrenados | Buscar, evaluar y usar |
| 55-70 | Proyecto WeLoveReviews | Diseñar notebook e inferencia |
| 70-75 | Cierre y comprobacion | Verificar decisiones |

Para 60 minutos, reducir la parte de redes neuronales y hacer el proyecto como recorrido de requisitos. Para 75, detenerse en los falsos negativos, la muestra manual de 15-20 reseñas y la extension opcional de comparar otro modelo.

## Preparacion

- Tener disponibles los tres contenidos de la clase y el brief del proyecto.
- Presentar la pregunta del cliente: hay 500 reseñas escritas y una puntuacion media de 4.5/5; se quiere saber si el texto expresa el mismo sentimiento.
- Recordar que el proyecto usa un notebook ejecutado como documento de comunicacion y una aplicacion para la logica de produccion.
- No presentar el proyecto como entrenamiento de un modelo: el brief pide integrar un modelo existente.

## Guion docente

### 0-8 min: abrir con la pregunta del cliente

**Que decir (literal)**

> Hoy vamos a pasar de la pregunta «¿que dicen los datos?» a una prediccion reproducible. El cliente tiene una media de 4.5 estrellas, pero quiere saber si las reseñas escritas cuentan la misma historia. La clase nos llevara desde los fundamentos del aprendizaje automatico hasta el uso responsable de un modelo preentrenado.

Presentar el caso WeLoveReviews: una consultora recibe 500 reseñas de un negocio con promedio 4.5/5. La account manager necesita el numero de reseñas positivas, neutrales y negativas, y una explicacion si la distribucion no coincide con las estrellas.

Pregunta de chequeo: «¿La media de estrellas y el sentimiento escrito son exactamente la misma medida?». Respuesta esperada: no; son señales distintas que deben compararse.

### 8-20 min: que es el aprendizaje automatico

**Que decir (literal)**

> El aprendizaje automatico busca que una maquina aprenda patrones a partir de datos para producir predicciones. El trabajo no termina cuando aparece una prediccion: tenemos que observar los datos, evaluar el modelo y comprobar si el resultado tiene sentido para el problema real.

Usar la secuencia oral:

```text
datos -> aprendizaje de patrones -> modelo -> prediccion -> evaluacion
```

Relacionar esta secuencia con el proyecto: primero se exploran las reseñas, despues se decide como limpiar y analizar los datos, luego se integra el modelo, se calculan bandas de sentimiento y se revisan manualmente casos dudosos.

Preguntar: «¿Que parte del flujo nos permite descubrir que el modelo puede equivocarse?». Respuesta: la evaluacion, incluida la inspeccion manual y el analisis de falsos negativos.

### 20-30 min: paradigmas de aprendizaje

**Que decir (literal)**

> No todos los problemas de aprendizaje usan los datos de la misma manera. Hoy distinguimos el aprendizaje supervisado, el no supervisado y otros paradigmas. La decision depende de la informacion disponible y del objetivo de la tarea.

En el proyecto, el modelo devuelve una puntuacion de 1 a 5 estrellas y esa salida se transforma en una banda:

| Prediccion | Banda |
| --- | --- |
| 1-2 estrellas | Negativo |
| 3 estrellas | Neutral |
| 4-5 estrellas | Positivo |

No confundir el promedio humano de 4.5 estrellas con la salida individual del modelo: el primero describe el negocio y la segunda describe cada reseña.

Pregunta: «¿Por que necesitamos definir el mapeo 1-2, 3 y 4-5 antes de contar resultados?». Respuesta: porque las predicciones son estrellas y el informe solicitado usa tres bandas de sentimiento.

### 30-41 min: redes neuronales

**Que decir (literal)**

> Una red neuronal es una familia de modelos que podemos estudiar antes de usar modelos de lenguaje ya entrenados. La pregunta practica no es solo que puede representar una red, sino como evaluamos su comportamiento en la tarea concreta.

Conectar con los contenidos de la clase: primero se introduce que es una red neuronal, despues se revisan redes neuronales en la practica y finalmente se discute su evaluacion. Mantener el foco en la tarea: texto de reseñas, puntuacion predicha y comparacion con una referencia humana.

Pregunta de chequeo: «¿Basta con que un modelo produzca una salida para considerarlo adecuado?». Respuesta esperada: no; hay que evaluarlo en el contexto de uso y revisar ejemplos concretos.

### 41-55 min: encontrar, evaluar y usar modelos preentrenados

**Que decir (literal)**

> Un modelo preentrenado permite empezar desde un modelo que ya ha aprendido con otros datos. Nuestra responsabilidad cambia: debemos encontrarlo, entender que salida produce, evaluar si encaja con nuestro dominio y documentar sus limitaciones.

El proyecto fija este modelo:

```text
nlptown/bert-base-multilingual-uncased-sentiment
```

Reglas de integracion que el profesor debe remarcar:

- Cargarlo mediante `pipeline()` o `from_pretrained()`.
- Cargarlo una sola vez antes del loop de inferencia.
- Fijar el nombre o version del modelo; no depender silenciosamente de `latest`.
- No descargar los pesos y subirlos al repositorio.
- Procesar las 500 reseñas y conservar una prediccion por reseña.

**Que decir (literal)**

> Este modelo fue ajustado con reseñas de productos, pero nuestro dataset contiene reseñas de servicios. Ese desajuste de dominio puede producir falsos negativos: texto que una persona interpreta como positivo, o que tiene una puntuacion humana alta, pero que el modelo clasifica con 1 o 2 estrellas.

La evaluacion debe incluir ejemplos de esos falsos negativos y una hipotesis sobre los patrones que comparten. Tambien se debe revisar manualmente una muestra de 15-20 reseñas.

### 55-70 min: proyecto WeLoveReviews

**Que decir (literal)**

> El notebook cuenta la historia del analisis y la aplicacion contiene la logica de inferencia de produccion. El resultado no es solo una etiqueta: necesitamos una comparacion comprensible entre texto, estrellas y promedio del negocio.

Flujo exigido por el brief:

```text
objetivos
-> EDA, insights y limpieza
-> plan de accion y justificacion del modelo
-> inferencia sobre 500 reseñas
-> bandas positivo/neutral/negativo
-> comparacion con 4.5 estrellas
-> falsos negativos y muestra manual
-> conclusiones para la account manager
```

Entregables que revisar con el grupo:

- `src/explore.ipynb`, ejecutado y con markdown breve entre bloques de codigo.
- `src/app.py`, con la logica de inferencia migrada a produccion.
- `data/processed/reviews_with_sentiment.csv`, con la salida enriquecida.
- `requirements.txt`, con versiones fijadas para `transformers` y `torch` o el backend elegido.
- `data/raw/reviews.csv`, con las reseñas proporcionadas por la plataforma.

El proyecto empieza desde `machine-learning-python-template`. La integracion debe usar `pipeline()` o `from_pretrained()`, cargar el modelo una sola vez y guardar tanto las estrellas predichas como la banda de sentimiento.

### Plan de trabajo para el estudiante

Leer este pseudocodigo en voz alta y pedir que cada persona señale donde valida su decision:

```text
colocar reviews.csv en data/raw/reviews.csv
explorar columnas, volumen, calidad y posibles problemas
escribir objetivos en src/explore.ipynb
decidir limpieza a partir de la EDA
fijar nlptown/bert-base-multilingual-uncased-sentiment
cargar el modelo una sola vez
inferir las 500 reseñas
mapear 1-2 a negativo, 3 a neutral y 4-5 a positivo
calcular porcentajes por banda
comparar la distribucion con 4.5 estrellas
buscar falsos negativos
revisar manualmente 15-20 reseñas
migrar la inferencia a src/app.py
escribir data/processed/reviews_with_sentiment.csv
documentar conclusiones en el notebook
```

No se añade un comando de terminal en esta guia porque el brief extraido no proporciona comandos concretos de ejecucion. El profesor debe ejecutar las instrucciones del repositorio plantilla y del entorno elegido, manteniendo los nombres de rutas y entregables anteriores.

### Extension opcional para 75 minutos

El brief propone probar `tabularisai/multilingual-sentiment-analysis` sobre las mismas 500 reseñas, comparar la tasa de falsos negativos y escribir un addendum dentro del mismo notebook recomendando si conviene cambiar de modelo. Esta extension no se evalua, pero sirve para discutir seleccion de modelos.

## Cierre y preguntas de chequeo

**Que decir (literal)**

> Un modelo preentrenado acelera la integracion, pero no elimina la evaluacion. La conclusion util para el cliente debe conectar la distribucion de sentimiento, el promedio de 4.5 estrellas, los ejemplos revisados a mano y las limitaciones causadas por el desajuste entre reseñas de productos y reseñas de servicios.

Preguntas finales:

1. ¿Que diferencia hay entre la puntuacion humana de 4.5 y la prediccion de estrellas por reseña?
2. ¿Como se convierten las estrellas predichas en tres bandas?
3. ¿Por que el modelo puede producir falsos negativos en este proyecto?
4. ¿Por que se carga una sola vez antes del loop?
5. ¿Que evidencia debe aparecer en el notebook para sostener una conclusion?
6. ¿Que archivo contiene la logica de produccion y que archivo contiene la historia del analisis?

Respuesta de cierre esperada: `src/explore.ipynb` comunica el analisis completo; `src/app.py` ejecuta la inferencia de produccion; el CSV procesado permite entregar resultados por reseña; y la conclusion debe reconocer tanto la señal encontrada como los errores observados.

## Recorte a 60 minutos

- 0-6 min: pregunta de negocio.
- 6-16 min: fundamentos y flujo de aprendizaje automatico.
- 16-25 min: paradigmas.
- 25-34 min: redes neuronales.
- 34-46 min: modelos preentrenados y reglas de integracion.
- 46-58 min: requisitos del proyecto y pseudocodigo.
- 58-60 min: dos preguntas finales.

Omitir la extension opcional y dejar la muestra manual como trabajo del proyecto.

## Contingencias

- Si el grupo se atasca con la arquitectura, volver al flujo `datos -> modelo -> prediccion -> evaluacion`.
- Si preguntan por entrenamiento desde cero, recordar que este proyecto no lo evalua: integra un modelo existente.
- Si la distribucion no coincide con 4.5 estrellas, no corregirla artificialmente; documentar la diferencia y revisar falsos negativos.
- Si no se puede ejecutar la inferencia durante la sesion, evaluar la estructura del notebook, la carga unica del modelo, el mapeo de estrellas, la muestra manual y la separacion entre notebook y app.