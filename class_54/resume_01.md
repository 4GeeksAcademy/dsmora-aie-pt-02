# Clase 54: aprendizaje automatico, redes neuronales y modelos preentrenados

## Trazabilidad y hilo de continuidad

Esta clase introduce el aprendizaje automatico, presenta las redes neuronales y termina con la integracion de un modelo preentrenado en un proyecto de analisis de sentimiento. El hilo conductor es: «Primero entendemos que aprende un modelo, despues vemos una familia de modelos neuronales y finalmente usamos un modelo ya entrenado sin construirlo desde cero».

Esta guia se basa exclusivamente en `tutorial.json`, `tutorial_2.json`, `tutorial_3.json` y `ai-eng-sentiment-analysis-reviews_project_README.es.md`. La agenda, las preguntas, las frases literales y la organizacion temporal son estructura docente añadida. Los ejemplos (correo spam, fraude en transacciones, segmentacion de clientes, prediccion de la siguiente palabra, ajedrez por refuerzo, k-means en Netflix, PCA en Spotify, prestamos bancarios, radiologia, transcripcion de audio, el flujo iris/GaussianNB y el quiz de seleccion de modelos) provienen literalmente de los tres JSON. Los materiales no contienen prompts de OpenClaw ni comandos de ejecucion concretos para el proyecto; por eso no se inventan.

## Objetivos

- Explicar que es el aprendizaje automatico, su vocabulario basico (caracteristica, etiqueta) y su flujo de trabajo.
- Distinguir los cinco paradigmas de aprendizaje (supervisado, no supervisado, auto-supervisado, por refuerzo y aprendizaje profundo) con un ejemplo real de cada uno.
- Distinguir clasificacion y regresion dentro del aprendizaje supervisado.
- Diferenciar entrenamiento e inferencia, y reconocer el sobreajuste con un ejemplo numerico.
- Describir la estructura y el aprendizaje de una red neuronal, y decidir cuando usarla frente a un modelo mas simple.
- Explicar que es un modelo preentrenado, donde encontrarlo, que revisar antes de elegirlo y como usarlo con el flujo cargar-preparar-inferir.
- Integrar `nlptown/bert-base-multilingual-uncased-sentiment` para clasificar reseñas.
- Comparar el sentimiento escrito con el promedio de 4.5 estrellas e identificar falsos negativos.

## Agenda de 60-75 minutos

```text
| Tiempo | Bloque                                 | Resultado                             |
| ------ | -------------------------------------- | -------------------------------------- |
| 0-6    | Pregunta de negocio                    | Enmarcar el problema del cliente       |
| 6-14   | Que es el aprendizaje automatico       | Flujo datos, caracteristicas, etiqueta |
| 14-30  | Paradigmas de aprendizaje              | Elegir el paradigma correcto           |
| 30-38  | Entrenamiento, inferencia y sobreajuste| Separar entrenar de inferir            |
| 38-52  | Redes neuronales                       | Decidir cuando usarlas                 |
| 52-64  | Modelos preentrenados                  | Buscar, evaluar y usar un modelo       |
| 64-72  | Proyecto WeLoveReviews                 | Disenar notebook e inferencia          |
| 72-75  | Cierre y comprobacion                  | Verificar decisiones                   |
```

Para 60 minutos, usar solo un ejemplo por paradigma, omitir el marco de decision de redes neuronales frente a modelos simples y tratar el proyecto como recorrido de requisitos. Para 75, cubrir todos los ejemplos, el marco de decision completo, los falsos negativos, la muestra manual de 15-20 reseñas y la extension opcional de comparar otro modelo. El apendice final ("Material de apoyo ampliado") queda fuera del conteo de 75 minutos: es para profundizar si el grupo pide mas detalle o para preparar la clase.

## Preparacion

- Tener disponibles los tres contenidos de la clase y el brief del proyecto.
- Presentar la pregunta del cliente: hay 500 reseñas escritas y una puntuacion media de 4.5/5; se quiere saber si el texto expresa el mismo sentimiento.
- Recordar que el proyecto usa un notebook ejecutado como documento de comunicacion y una aplicacion para la logica de produccion.
- No presentar el proyecto como entrenamiento de un modelo: el brief pide integrar un modelo existente.
- Revisar el apendice "Material de apoyo ampliado" antes de la clase si se quiere ejecutar el ejemplo de codigo en vivo.

## Guion docente

### 0-6 min: abrir con la pregunta del cliente

**Que decir (literal)**

> Hoy vamos a pasar de la pregunta «¿que dicen los datos?» a una prediccion reproducible. El cliente tiene una media de 4.5 estrellas, pero quiere saber si las reseñas escritas cuentan la misma historia. La clase nos llevara desde los fundamentos del aprendizaje automatico hasta el uso responsable de un modelo preentrenado.

Presentar el caso WeLoveReviews: una consultora recibe 500 reseñas de un negocio con promedio 4.5/5. La account manager necesita el numero de reseñas positivas, neutrales y negativas, y una explicacion si la distribucion no coincide con las estrellas.

Pregunta de chequeo: «¿La media de estrellas y el sentimiento escrito son exactamente la misma medida?». Respuesta esperada: no; son señales distintas que deben compararse.

### 6-14 min: que es el aprendizaje automatico

**Que decir (literal)**

> El aprendizaje automatico busca que una maquina aprenda patrones a partir de datos para producir predicciones. El trabajo no termina cuando aparece una prediccion: tenemos que observar los datos, evaluar el modelo y comprobar si el resultado tiene sentido para el problema real.

Usar la secuencia oral:

```text
datos -> aprendizaje de patrones -> modelo -> prediccion -> evaluacion
```

Definir dos palabras que se usaran toda la clase:

- **Caracteristica**: una variable de entrada que describe una observacion (por ejemplo, el texto de una reseña).
- **Etiqueta**: la respuesta correcta asociada a un ejemplo cuando existe (por ejemplo, la puntuacion humana de estrellas de esa reseña).

Relacionar esta secuencia con el proyecto: primero se exploran las reseñas, despues se decide como limpiar y analizar los datos, luego se integra el modelo, se calculan bandas de sentimiento y se revisan manualmente casos dudosos.

Preguntar: «¿Que parte del flujo nos permite descubrir que el modelo puede equivocarse?». Respuesta: la evaluacion, incluida la inspeccion manual y el analisis de falsos negativos.

### 14-30 min: paradigmas de aprendizaje

**Que decir (literal)**

> El aprendizaje automatico es un campo diverso con varias formas en que las maquinas aprenden de los datos. Hoy vamos a los cinco paradigmas principales y nos enfocamos en los dos mas comunes en ciencia de datos: supervisado y no supervisado.

#### Aprendizaje supervisado

> En el aprendizaje supervisado aprendemos a partir de ejemplos etiquetados: cada entrada viene con la respuesta correcta. Es el mas comun en aplicaciones del mundo real.

Ejemplo del material: predecir si un correo electronico es spam o no, a partir de correos ya etiquetados como spam o no spam.

La estructura que debe escribir el profesor en la pizarra es:

```text
entrada + etiqueta conocida -> aprendizaje de una relacion -> prediccion
```

**Clasificacion frente a regresion dentro del supervisado**

> Dentro del aprendizaje supervisado, cuando la etiqueta es una categoria hablamos de clasificacion; cuando la etiqueta es un numero continuo hablamos de regresion.

Dos ejemplos del material para contrastar en clase:

- Clasificacion: un banco tiene 50.000 transacciones etiquetadas como "fraude" o "no fraude" y quiere predecir fraude en transacciones nuevas. Es clasificacion supervisada porque aprende de ejemplos etiquetados para predecir una categoria.
- Regresion: una empresa quiere predecir la demanda de electricidad de mañana en kilovatios-hora. Es regresion porque el objetivo es un valor numerico continuo, no una categoria.

Ejemplo docente conectado al proyecto: una reseña es la entrada y su puntuacion humana de estrellas es la etiqueta conocida. En el proyecto de esta clase, sin embargo, no se entrena un modelo desde cero: se integra uno ya preentrenado y se analiza su salida, que tambien llega como una puntuacion de 1 a 5.

#### Aprendizaje no supervisado

> En el aprendizaje no supervisado no entregamos una etiqueta correcta para cada ejemplo. El objetivo es descubrir estructura, agrupaciones o regularidades dentro de los datos.

Ejemplo del material: agrupar clientes en segmentos basados en su comportamiento de compra, sin categorias predefinidas. Una empresa con 2 millones de cuentas que no sabe cuantos tipos de clientes existen usa agrupamiento no supervisado para encontrar grupos naturales y personalizar marketing.

#### Aprendizaje auto-supervisado

> En el aprendizaje auto-supervisado, el propio modelo crea sus etiquetas a partir de la estructura de los datos, sin que una persona las asigne. Es comun en procesamiento de lenguaje natural y en modelos a gran escala.

Ejemplo del material: predecir la siguiente palabra en una oracion sin etiquetas puestas por humanos.

#### Aprendizaje por refuerzo

> En el aprendizaje por refuerzo, un agente aprende tomando acciones y recibiendo recompensas o penalizaciones. Se usa en juegos, robotica y toma de decisiones secuenciales.

Ejemplo del material: una inteligencia artificial que aprende a jugar ajedrez ganando o perdiendo partidas.

#### Aprendizaje profundo, una tecnica transversal

> El aprendizaje profundo no es un paradigma mas al lado de los otros cuatro: es una tecnica que usa redes neuronales multicapa y puede aplicarse dentro del aprendizaje supervisado, no supervisado o por refuerzo. Destaca con datos no estructurados como imagenes, audio y texto.

Tabla resumen para dejar visible durante el bloque:

```text
| Paradigma        | Informacion disponible                    | Ejemplo del material                          |
| ---------------- | ------------------------------------------ | ---------------------------------------------- |
| Supervisado      | Entradas y etiquetas conocidas             | Detectar correo spam con correos etiquetados   |
| No supervisado   | Entradas sin etiqueta                      | Agrupar clientes por comportamiento de compra  |
| Auto-supervisado | El modelo genera sus propias etiquetas     | Predecir la siguiente palabra en una oracion   |
| Por refuerzo     | Acciones, estados y recompensas            | Una IA que aprende a jugar ajedrez             |
| Aprendizaje profundo | Redes neuronales multicapa, cruza paradigmas | Se aplica dentro de los otros cuatro       |
```

No confundir el promedio humano de 4.5 estrellas del proyecto con la salida individual del modelo: el primero describe el negocio y la segunda describe cada reseña. El proyecto transforma la puntuacion de 1 a 5 en una banda:

```text
| Prediccion    | Banda    |
| ------------- | -------- |
| 1-2 estrellas | Negativo |
| 3 estrellas   | Neutral  |
| 4-5 estrellas | Positivo |
```

Pregunta: «¿Por que necesitamos definir el mapeo 1-2, 3 y 4-5 antes de contar resultados?». Respuesta: porque las predicciones son estrellas y el informe solicitado usa tres bandas de sentimiento.

Preguntas adicionales de comprobacion:

1. «Si tengo textos sin etiquetas y busco grupos, ¿que paradigma describo?». Respuesta: no supervisado.
2. «Si predigo la siguiente palabra de una oracion sin que un humano etiquete nada, ¿que paradigma describo?». Respuesta: auto-supervisado.
3. «Si predigo un numero continuo como la demanda de electricidad, ¿es clasificacion o regresion?». Respuesta: regresion.
4. «¿El proyecto entrena aqui un modelo nuevo?». Respuesta: no; integra un modelo preentrenado.

### 30-38 min: entrenamiento, inferencia y sobreajuste

**Que decir (literal)**

> Conviene separar tres momentos. Durante el entrenamiento, un modelo ajusta sus parametros usando datos. Durante la prediccion o inferencia, recibe una entrada nueva y produce una salida sin modificar esos parametros. Durante la evaluacion, comparamos esa salida con una referencia o la revisamos en el contexto real.

Aplicarlo al proyecto:

```text
modelo ya entrenado + texto de una reseña -> estrellas predichas -> banda de sentimiento
```

La inferencia no debe confundirse con el entrenamiento. El brief nos pide cargar el modelo, reutilizarlo para las 500 reseñas y guardar las predicciones. No nos pide ajustar sus pesos ni descargar los pesos para incluirlos en el repositorio.

**Que decir (literal)**

> Un modelo puede parecer excelente y en realidad haber memorizado los datos de entrenamiento en lugar de aprender un patron que generalice. Esto se llama sobreajuste.

Ejemplo del material: un modelo obtiene 98% de precision en el conjunto de entrenamiento y solo 61% en el conjunto de prueba. La causa mas probable es que el modelo esta sobreajustado: memorizo los datos de entrenamiento y no generaliza a datos nuevos.

Pregunta: «¿Que cambia cuando usamos un modelo preentrenado?». Respuesta: no empezamos el aprendizaje desde cero, pero seguimos siendo responsables de comprobar si sus salidas son adecuadas para nuestros datos, igual que comprobariamos el sobreajuste en un modelo propio.

### 38-52 min: redes neuronales

**Que decir (literal)**

> El termino "red neuronal" viene de una analogia aproximada con el cerebro humano: asi como nuestras neuronas se activan y se conectan, una red neuronal artificial esta formada por capas de nodos interconectados que procesan informacion. La analogia es simplificada: las neuronas artificiales son funciones matematicas, no celulas biologicas.

Estructura que hay que dibujar en la pizarra:

```text
capa de entrada -> una o mas capas ocultas -> capa de salida
```

- **Capa de entrada**: recibe los datos en bruto (por ejemplo, los pixeles de una imagen).
- **Capas ocultas**: transforman la entrada mediante conexiones ponderadas; cada conexion tiene un peso.
- **Capa de salida**: produce la prediccion o clasificacion final, tras aplicar una funcion de activacion a las entradas ponderadas combinadas.

**Como aprende una red neuronal**

> El aprendizaje ocurre ajustando los pesos para minimizar la diferencia entre la salida de la red y la respuesta correcta. Se presentan muchos ejemplos de entrenamiento, se calcula el error entre lo predicho y lo real, y un algoritmo llamado retropropagacion actualiza los pesos para reducir ese error con el tiempo.

**Donde encaja la red neuronal**

> El Aprendizaje Automatico es el campo amplio de algoritmos que aprenden de datos. El Aprendizaje Profundo es un subconjunto que usa redes neuronales con multiples capas ocultas. Las redes neuronales son las arquitecturas que impulsan el aprendizaje profundo. "Profundo" se refiere a tener multiples capas ocultas, que permiten aprender caracteristicas cada vez mas abstractas.

En una tarea de imagenes, las capas iniciales detectan caracteristicas simples como bordes, las capas intermedias combinan esas caracteristicas en formas, y las capas finales interpretan esos patrones para predecir. Este aprendizaje jerarquico es lo que hace poderosas a las redes neuronales cuando la ingenieria manual de caracteristicas es dificil: reconocer rostros en fotos, traducir idiomas o entender comandos hablados son ejemplos del material.

**Redes neuronales frente a otras familias de modelos**

> Las redes neuronales son una familia de modelos entre varias: arboles de decision, bosques aleatorios, maquinas de gradiente aumentado como XGBoost, maquinas de vectores de soporte y regresion lineal. Cada familia tiene fortalezas y debilidades.

**Cuando elegir un modelo simple**

Para datos tabulares estructurados con un conjunto de datos pequeño (cientos a unos pocos miles de registros), modelos como la regresion logistica o los arboles potenciados por gradiente suelen ser mas efectivos: se entrenan rapido, requieren menos datos y son interpretables. Ejemplo del material: un banco que predice incumplimientos de prestamos usando ingresos, puntaje crediticio e historial laboral se beneficia de un arbol potenciado por gradiente, porque se entrena rapido, maneja bien datos estructurados y ofrece explicaciones que los reguladores pueden entender.

**Cuando elegir una red neuronal**

Las redes neuronales sobresalen con datos complejos y no estructurados. Ejemplo del material: un hospital que analiza escaneres de radiologia para detectar tumores usa redes neuronales convolucionales (CNN), porque los patrones de pixeles que distinguen tumores benignos de malignos son demasiado complejos para definir manualmente. Otro ejemplo: ajustar un Transformer preentrenado para analisis de sentimiento en reseñas de clientes reduce el tiempo de entrenamiento y los recursos necesarios manteniendo el rendimiento — esto es exactamente lo que hace el proyecto de esta clase.

**Consideraciones en contra de las redes neuronales**

- Interpretabilidad: suelen ser opacas; si se requieren explicaciones claras, un modelo mas simple es preferible.
- Tamaño del conjunto de datos: necesitan datos grandes para generalizar bien.
- Presupuesto computacional: entrenarlas demanda recursos significativos.

Ejemplo adicional del material para reforzar la decision: una empresa con 500 registros de clientes y 8 caracteristicas estructuradas que quiere predecir la perdida de clientes deberia empezar con un arbol potenciado por gradiente o regresion logistica, porque los datos son estructurados, pequeños y la interpretabilidad probablemente importa; una red neuronal profunda no es la opcion por defecto solo porque exista.

Pregunta de chequeo: «¿Basta con que un modelo produzca una salida para considerarlo adecuado?». Respuesta esperada: no; hay que evaluar el contexto de uso, el tamaño y tipo de datos, la interpretabilidad requerida y el presupuesto computacional.

Segunda pregunta: «Un equipo quiere transcribir audio hablado a texto, ¿por que una red neuronal es apropiada?». Respuesta: porque el audio es un dato no estructurado donde los patrones relevantes no pueden definirse manualmente con reglas.

### 52-64 min: encontrar, evaluar y usar modelos preentrenados

**Que decir (literal)**

> Un modelo preentrenado permite empezar desde un modelo que ya ha aprendido con otros datos. Esto ahorra el entrenamiento inicial, pero no elimina el trabajo de ingenieria. Tenemos que encontrar un modelo, leer que tarea resuelve, conocer el formato de su salida, evaluar si encaja con nuestro dominio y documentar sus limitaciones.

**Donde buscar un modelo**

Repositorios que el material señala como principales:

- Hugging Face Hub (huggingface.co/models): el repositorio comunitario mas grande, con mas de 500.000 modelos; cubre PLN, vision por computadora, audio y mas; cada modelo tiene una tarjeta con sus detalles.
- Modelos integrados de scikit-learn: algoritmos preimplementados para datos tabulares (maquinas de vectores de soporte, bosques aleatorios, boosting de gradiente); son implementaciones listas para usar, no pesos preentrenados.
- TensorFlow Hub (tfhub.dev): modelos TensorFlow preentrenados, fuertes en vision por computadora.
- PyTorch Hub (pytorch.org/hub): modelos PyTorch seleccionados, a menudo de investigacion de vanguardia.
- Modelos de Kaggle: contribuidos por la comunidad, a menudo ganadores de competiciones.
- ONNX Model Zoo (onnx.ai/models): modelos en formato ONNX usables en distintos frameworks.

Cada repositorio permite filtrar por tarea (clasificacion de texto, clasificacion de imagenes, clasificacion de tokens, entre otras); se busca la tarea y se revisan los modelos mas populares o mejor valorados.

**Que revisar en la pagina de un modelo antes de elegirlo**

- Tarea: ¿realiza exactamente la tarea que necesitamos?
- Metricas: ¿que tan bien funciona? (precision, F1, BLEU u otros benchmarks relevantes)
- Conjunto de datos: ¿con que datos fue entrenado y que tan similar es a nuestro dominio?
- Licencia: ¿podemos usarlo legalmente? MIT o Apache 2.0 son permisivas; CC-BY-NC restringe el uso comercial.
- Popularidad: descargas o estrellas como señal de fiabilidad y apoyo comunitario.
- Ultima actualizacion: ¿se mantiene activamente?

**El flujo de trabajo cargar-preparar-inferir**

> Usar un modelo preentrenado sigue un patron simple y consistente: cargar el modelo en memoria, preparar la entrada en el formato exacto que espera, y ejecutar inferencia para obtener predicciones sin modificar los parametros del modelo.

```text
cargar el modelo -> preparar la entrada -> ejecutar inferencia -> interpretar la salida
```

La inferencia usa los parametros aprendidos para generar una salida; a diferencia del entrenamiento, no los actualiza. El ejemplo completo de este flujo con codigo ejecutable (dataset iris y `GaussianNB`) esta en el apendice "Material de apoyo ampliado" al final de esta guia, listo para mostrarlo en pantalla si el tiempo lo permite.

**Aplicando el flujo a este proyecto**

1. «¿Que tarea resuelve el modelo?»: sentimiento en reseñas.
2. «¿Que devuelve?»: una puntuacion de 1 a 5 estrellas, no directamente las palabras positivo, neutral o negativo.
3. «¿Con que tipo de datos fue ajustado?»: con reseñas de productos.
4. «¿Que ocurre cuando lo aplicamos aqui?»: nuestro dataset contiene reseñas de servicios, por lo que debemos buscar falsos negativos y revisar ejemplos manualmente.

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

Definir falso negativo para la sesion:

> En este proyecto buscamos especialmente una reseña que el modelo coloque en 1 o 2 estrellas, pero cuya puntuacion humana sea 4 o 5, o cuyo texto parezca positivo o neutral al leerlo. No basta con listar el caso: hay que mostrar la reseña, la salida del modelo y una hipotesis sobre el error.

La evaluacion debe incluir tres niveles:

- Distribucion: porcentaje positivo, neutral y negativo entre las 500 reseñas.
- Comparacion: relacion entre esa distribucion y el promedio de 4.5 estrellas.
- Revision cualitativa: falsos negativos y muestra manual de 15-20 reseñas.

Pregunta: «¿Que nos diria solo el porcentaje y que no nos diria?». Respuesta: el porcentaje resume la distribucion, pero no explica por que hay desacuerdos; para eso necesitamos ejemplos y revision manual.

Pregunta adicional: «Si una tarjeta de modelo dice licencia CC-BY-NC, ¿podemos usarlo en un producto de pago?». Respuesta: no; CC-BY-NC restringe el uso comercial, y esa es una razon real para descartar un modelo aunque su rendimiento sea bueno.

### 64-72 min: proyecto WeLoveReviews

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
7. ¿En que paradigma de aprendizaje encaja predecir una etiqueta de sentimiento a partir de texto etiquetado, y en que se diferencia de agrupar reseñas sin etiquetas?
8. ¿Por que la clase eligio integrar una red neuronal preentrenada en lugar de entrenar un arbol potenciado por gradiente para este proyecto?

Respuesta de cierre esperada: `src/explore.ipynb` comunica el analisis completo; `src/app.py` ejecuta la inferencia de produccion; el CSV procesado permite entregar resultados por reseña; la conclusion debe reconocer tanto la señal encontrada como los errores observados; el sentimiento en texto es un problema de clasificacion supervisada (frente a agrupar sin etiquetas, que seria no supervisado); y una red neuronal de lenguaje preentrenada es apropiada porque el texto es un dato no estructurado donde los patrones no pueden definirse manualmente con reglas.

## Recorte a 60 minutos

- 0-5 min: pregunta de negocio.
- 5-12 min: fundamentos, vocabulario y flujo de aprendizaje automatico.
- 12-24 min: paradigmas, con un solo ejemplo por paradigma y la tabla resumen.
- 24-30 min: entrenamiento, inferencia y el ejemplo de sobreajuste.
- 30-40 min: redes neuronales, usando solo el ejemplo del hospital y el del banco para la decision.
- 40-50 min: modelos preentrenados, repositorios, checklist de la tarjeta y reglas de integracion.
- 50-57 min: requisitos del proyecto y pseudocodigo.
- 57-60 min: dos preguntas finales.

Omitir la extension opcional, el apendice de codigo y el quiz de escenarios; dejar la muestra manual como trabajo del proyecto.

## Material de apoyo ampliado (fuera del guion de 75 minutos)

Esta seccion no forma parte del tiempo de clase contado en la agenda. Es material de referencia para que el profesor profundice si el grupo pregunta, para prepararse antes de la sesion o para una clase extendida.

### Ejemplo completo del flujo cargar-preparar-inferir (scikit-learn)

> El conjunto de datos iris es un clasico en aprendizaje automatico: contiene mediciones de flores de tres especies. El objetivo es predecir la especie a partir de cuatro caracteristicas: longitud del sepalo, ancho del sepalo, longitud del petalo y ancho del petalo. El clasificador Naive Bayes Gaussiano (`GaussianNB`) es un modelo simple que asume que las caracteristicas siguen una distribucion normal.

```python
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB

# Cargar el conjunto de datos iris
iris = load_iris()
X, y = iris.data, iris.target  # Caracteristicas y etiquetas

# Crear y entrenar el modelo Naive Bayes Gaussiano
# (en escenarios reales, cargarias un modelo preentrenado desde disco)
model = GaussianNB()
model.fit(X, y)  # Paso de entrenamiento

# Definir nuevas muestras para prediccion
new_samples = [
    [5.1, 3.5, 1.4, 0.2],  # Muestra 1
    [6.7, 3.0, 5.2, 2.3],  # Muestra 2
]

# Ejecutar inferencia: predecir indices de clase para nuevas muestras
predictions = model.predict(new_samples)

# Tambien obtener probabilidades de prediccion para confianza
probabilities = model.predict_proba(new_samples)

# Mapear indices predichos a nombres de especies e imprimir resultados
for i, (pred, proba) in enumerate(zip(predictions, probabilities)):
    species = iris.target_names[pred]      # Convertir indice a nombre
    confidence = max(proba) * 100           # Probabilidad mas alta de clase
    print(f"Muestra {i+1}: {species} ({confidence:.1f}% de confianza)")
```

Conceptos clave que remarcar al mostrar este codigo:

- Entrenamiento frente a inferencia: el entrenamiento actualiza los parametros del modelo; la inferencia usa esos parametros fijos para predecir.
- Preparacion de entrada: el orden y la escala de las caracteristicas deben coincidir con lo que el modelo espera.
- Interpretacion de salida: las predicciones son indices numericos; siempre hay que mapearlos a etiquetas legibles.
- Puntajes de confianza: `predict_proba()` ayuda a evaluar cuan fiable es cada prediccion.
- Para reutilizar un modelo entre proyectos sin volver a descargarlo o entrenarlo, el material recomienda guardarlo en disco con `joblib` y cargarlo despues.

### Quiz de seleccion de modelos (para profundizar o resolver dudas)

1. Necesitas añadir deteccion de spam a un correo electronico. ¿Que deberias hacer primero? Respuesta: buscar en Hugging Face un modelo de clasificacion de texto ya entrenado con datos de spam, en lugar de recopilar datos y entrenar desde cero.
2. Una tarjeta de modelo dice licencia "CC-BY-NC". ¿Puedes usarlo en un producto SaaS de pago? Respuesta: no, CC-BY-NC restringe el uso comercial.
3. El Modelo A tiene 95% de precision en un benchmark que coincide con tu dominio; el Modelo B tiene 99% pero fue entrenado con datos de otro dominio. ¿Con cual empezar? Respuesta: con el Modelo A, porque la adecuacion al dominio importa mas que la precision bruta del benchmark.
4. Una tarjeta de modelo dice "alcanza 99.5% de precision en el conjunto de entrenamiento". ¿Por que puede ser engañoso? Respuesta: la precision en el conjunto de entrenamiento mide memorizacion, no generalizacion; el modelo puede estar sobreajustado.
5. Descargaste un modelo y quieres reutilizarlo en otro proyecto sin descargarlo de nuevo. ¿Que hacer? Respuesta: guardarlo en disco con `joblib` y cargarlo en el nuevo proyecto.

## Contingencias

- Si el grupo se atasca con la arquitectura, volver al flujo `datos -> modelo -> prediccion -> evaluacion`.
- Si preguntan por entrenamiento desde cero, recordar que este proyecto no lo evalua: integra un modelo existente.
- Si la distribucion no coincide con 4.5 estrellas, no corregirla artificialmente; documentar la diferencia y revisar falsos negativos.
- Si no se puede ejecutar la inferencia durante la sesion, evaluar la estructura del notebook, la carga unica del modelo, el mapeo de estrellas, la muestra manual y la separacion entre notebook y app.
- Si el grupo confunde paradigmas, volver a la tabla de cinco paradigmas y pedir que cada persona clasifique el proyecto de la clase (supervisado, porque el modelo predice una etiqueta de sentimiento) antes de seguir.