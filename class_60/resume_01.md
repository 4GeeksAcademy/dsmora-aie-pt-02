# Clase 60: Monitoreo de salud del modelo

> Guía docente elaborada únicamente a partir de `tutorial.json`, generado con `scripts/scraper.py`. El JSON contiene seis lecciones scrapeadas: introducción, dimensiones de monitoreo, métricas de Prefect, un ejercicio para instrumentar un flujo y dos lecciones de cierre con el mismo contenido. La secuencia, los tiempos, las preguntas y las frases docentes de esta guía organizan ese material; los conceptos y el ejemplo técnico proceden del JSON.

## Hilo de continuidad

La clase 59 trabajó la selección y evaluación de modelos mediante búsqueda de hiperparámetros. La clase 60 cambia el foco: una vez que un modelo está desplegado, ¿cómo observar si el flujo que lo ejecuta sigue funcionando como se espera y qué datos procesó? La fuente de esta clase concreta ese monitoreo en estados y duración del flujo, frescura y volumen de datos, y una práctica de instrumentación con Prefect.

**Frase de transición:** «En la clase anterior comparamos configuraciones y seleccionamos modelos. Hoy miraremos lo que ocurre cuando el flujo ya se ejecuta: que termine no basta; también nos importa cuánto tardó y qué datos procesó».

## Objetivos de aprendizaje

Al terminar la clase, el estudiante podrá:

- Explicar por qué un flujo completado puede aun así haber procesado datos obsoletos o cero filas.
- Identificar las cuatro dimensiones de salud presentadas: completaciones/fallos, duración, frescura y volumen de datos.
- Distinguir qué registra Prefect automáticamente y qué requiere instrumentación explícita.
- Instrumentar un flujo de Prefect para reportar el conteo de filas, manejar e informar un error de procesamiento y mostrar su duración.

## Agenda sugerida: 70 minutos

| Minutos | Bloque | Resultado |
|---|---|---|
| 0–7 | Apertura: la ceguera en producción | Reconocer las preguntas que el monitoreo debe responder |
| 7–20 | Cuatro dimensiones de salud | Separar señales de ejecución y de datos |
| 20–32 | Prefect: automático y explícito | Clasificar métricas y justificar qué instrumentar |
| 32–55 | Ejercicio: instrumentar `monitored_flow` | Completar y explicar el ejemplo de código |
| 55–65 | Lectura de señales y escenarios | Interpretar volumen cero, datos obsoletos y aumento de duración |
| 65–70 | Cierre y chequeo | Resumir el mínimo de señales útiles |

**Recorte a 60 minutos:** hacer el bloque de escenarios como preguntas orales y reducir la discusión de métricas a la tabla de automático/ explícito; mantener el ejercicio de instrumentación.
**Extensión a 75 minutos:** pedir al grupo que proponga cuál señal instrumentaría primero en uno de sus propios flujos y que explique qué problema podría revelar; no agregar métricas que no estén en la fuente.

## Preparación docente

- Tener a mano `class_60/tutorial.json`, creado mediante `scripts/scraper.py`.
- Usar el ejercicio scrapeado de `app.py` como demostración. La fuente indica las tareas `load_data` y `process_batch`, el flujo `monitored_flow`, la lista `[1, 2, 3, 4, 5]`, el procesamiento `x * 2` y los textos esperados para reportar conteo, error y duración.
- La lección de métricas también presenta como ejemplo `load_breast_cancer(return_X_y=True)` para obtener `X` y contar `len(X)`. No es necesario mezclar ese ejemplo con el ejercicio principal.
- El JSON no proporciona un comando de instalación ni un comando de terminal para ejecutar la práctica. No asumir ni agregar comandos de instalación; impartirla como lectura/corrección guiada del ejercicio en el entorno del curso.
- El material no incluye prompts para OpenClaw ni una demo de esa herramienta; esta guía no inventa uno.
- Nota de scraping: las dos últimas entradas tienen títulos distintos («Evaluación de monitoreo de modelos» y «Resumen de monitoreo») pero el contenido guardado es esencialmente el mismo resumen. Se utiliza una sola vez como cierre.

## 0–7 min | Apertura: la ceguera en producción

### Qué decir (literal)

«Desplegar un modelo es un hito, pero no responde por sí solo si hoy se ejecutó, si terminó bien, cuánto tardó ni cuántos datos procesó. Sin esas señales podemos enterarnos tarde de un fallo o de resultados obsoletos. Hoy vamos a hacer visible la salud del flujo con unas pocas métricas concretas».

La introducción propone cuatro preguntas: ¿se ejecutó hoy?, ¿completó o falló?, ¿cuánto tardó?, ¿procesó la cantidad esperada de datos? La lección de bienvenida agrupa la monitorización en salud del flujo, duración y volumen; la siguiente amplía el mapa con frescura de los datos.

### Preguntar

- «Si el flujo aparece como completado, ¿qué información importante todavía podría faltarnos?»
- «¿Qué efecto tendría descubrir varios días después que el flujo fallaba o tardaba mucho más?»

## 7–20 min | Las cuatro dimensiones de salud

Presentar y contrastar las dimensiones tal como aparecen en el material:

| Dimensión | Pregunta que responde | Qué indica la fuente |
|---|---|---|
| Completaciones y fallos | ¿Terminó el flujo con éxito o falló? | Prefect registra estados como `COMPLETADO` o `FALLIDO`, marcas de tiempo y rastros de error. |
| Duración | ¿Cuánto tardó? | Prefect registra inicio y fin. Un aumento repentino puede indicar dependencias lentas o problemas con los datos. |
| Frescura de los datos | ¿La entrada está actualizada? | No se rastrea automáticamente; requiere verificaciones de marcas de tiempo o actualidad de los datos. |
| Volumen de datos | ¿Cuántas filas se procesaron? | No se cuenta automáticamente; hay que exponer y registrar el conteo. Cero o un número inesperado puede señalar problemas en el origen. |

### Qué decir (literal)

«Las primeras dos dimensiones describen la ejecución. Las otras dos nos dicen algo sobre los datos que la ejecución consumió. Un estado exitoso no garantiza por sí mismo que la entrada fuera reciente ni que tuviera el volumen esperado».

Utilizar los dos casos de la fuente: un trabajo nocturno podría fallar porque se movió el archivo de entrada y dejar resultados obsoletos; un flujo de recomendaciones que tarda mucho más puede retrasar sistemas posteriores y hacer que sirvan datos desactualizados.

### Preguntar

- «¿Qué dimensión observarías si sospechas que se procesó el archivo de ayer?» (Frescura.)
- «¿Y si el flujo terminó como completado, pero procesó cero filas?» (Volumen.)
- «¿Qué señal revisarías ante una demora repentina?» (Duración.)

## 20–32 min | Qué registra Prefect y qué debes agregar

### Explicación para el profesor

Según el JSON, Prefect registra automáticamente:

- Estado de cada ejecución del flujo, incluidas completaciones y fallos.
- Tiempos de inicio y fin; estos permiten observar la duración.
- Excepciones no manejadas y sus rastros de error.

La instrumentación explícita se necesita para:

- Conteo de filas procesadas.
- Frescura de la entrada.
- Señales de salud personalizadas, como verificaciones específicas del dominio o validaciones de umbrales.

La fuente menciona que la duración también puede calcularse con un temporizador personalizado; eso es opcional porque Prefect ya registra marcas de tiempo.

### Qué decir (literal)

«Prefect conoce el estado de la ejecución y sus tiempos. No puede inferir cuántas filas tenían nuestros datos, si estaban actualizados o qué umbral de negocio nos importa. Esas señales dependen de nuestros datos y nuestra lógica; tenemos que exponerlas».

### Preguntar

- «¿El conteo de filas lo calcula Prefect automáticamente?» (No.)
- «¿Necesito agregar un temporizador propio para tener alguna medida de duración?» (No es imprescindible; Prefect registra inicio y fin. El ejemplo añade uno explícito para imprimir un resumen.)
- «¿Por qué Prefect no puede adivinar la frescura o las señales personalizadas?» (Dependen de la entrada y de la lógica específica del flujo.)

## 32–55 min | Práctica guiada: instrumentar un flujo Prefect

El ejercicio de la lección 1.2 pide modificar `load_data` para devolver datos y conteo, envolver `process_batch` con `try/except`, y medir e imprimir la duración en `monitored_flow`. Proyectar este ejemplo completo, resuelto siguiendo las instrucciones y el código proporcionados en el JSON:

```python
from prefect import flow, task
import time


@task
def load_data():
    data = [1, 2, 3, 4, 5]
    row_count = len(data)
    print(f"Filas cargadas: {row_count}")
    return data, row_count


@task
def process_batch(data):
    try:
        result = [x * 2 for x in data]
        return result
    except Exception as e:
        print(f"Error de procesamiento: {e}")
        return None


@flow
def monitored_flow():
    start = time.time()
    data, row_count = load_data()
    processed = process_batch(data)
    duration = time.time() - start
    print(f"Flujo completado: {row_count} filas procesadas en {duration:.2f}s")


if __name__ == "__main__":
    monitored_flow()
```

### Explicación del código para el profesor

- `@task` identifica las funciones `load_data` y `process_batch` como tareas de Prefect; `@flow` identifica `monitored_flow` como el flujo que las coordina.
- `load_data()` crea cinco valores, calcula `row_count` con `len(data)`, imprime `Filas cargadas: 5` y devuelve una tupla `(data, row_count)`. El flujo desempaqueta ambos valores.
- `process_batch(data)` multiplica cada valor por dos y devuelve la lista resultante. Si ocurre una excepción durante ese bloque, la captura, imprime `Error de procesamiento: ...` y devuelve `None`, según el enunciado.
- `time.time()` toma el inicio y, después de procesar, se resta el inicio para obtener el tiempo transcurrido. El formato `{duration:.2f}` muestra dos decimales.
- El resumen final incluye el conteo y la duración. La duración concreta depende de la ejecución; no fijar un número como resultado esperado.
- `processed` recibe el retorno de `process_batch`; en el ejercicio, la salida solicitada para el flujo es el conteo y la duración, no una impresión del resultado procesado.

### Guion docente

1. **Antes de mostrar la solución**, pedir que identifiquen qué devuelve la versión original de `load_data` y por qué eso no permite reportar el conteo en el flujo.
2. Añadir `row_count = len(data)`, imprimirlo y cambiar el retorno a `data, row_count`.
3. En `monitored_flow`, mostrar el desempaquetado `data, row_count = load_data()`.
4. Leer el `try/except` de `process_batch`: la fuente pide reportar el mensaje y retornar `None` si falla.
5. Añadir las dos lecturas de tiempo alrededor de las tareas y el resumen final con el formato indicado.
6. Comparar el resultado esperado del ejercicio: una línea `Filas cargadas: ...` y una línea resumen; un error de procesamiento se informa en vez de dejarse sin manejar dentro de esa tarea.

### Qué decir (literal)

«Estamos exponiendo una señal que Prefect no conoce por sí solo: el número de filas. Además, ponemos un temporizador alrededor del trabajo para dejar un resumen legible. El manejo explícito del error hace que el mensaje esperado quede visible en vez de depender de un fallo genérico».

### Preguntar

- «¿Qué dos cosas devuelve ahora `load_data`?» (Los datos y el conteo.)
- «¿Qué muestra el mensaje de error y qué valor devuelve el bloque `except`?» (Imprime la excepción y devuelve `None`.)
- «¿Qué representa `duration`?» (El tiempo transcurrido entre el inicio y el punto en que se calcula después del procesamiento.)
- «¿Por qué incluimos el conteo en el resumen final?» (Para observar el volumen procesado junto con la ejecución.)

## 55–65 min | Interpretar señales y límites

Proponer oralmente los escenarios de cierre recogidos en el JSON:

1. Un trabajo nocturno termina como `COMPLETADO`, pero procesa cero filas. **Lectura:** el estado no basta; el conteo puede revelar un problema con los datos de origen.
2. El flujo se completa, pero procesó una entrada obsoleta. **Lectura:** hay que instrumentar una verificación de frescura; el estado no certifica que los datos sean actuales.
3. La duración aumenta de forma repentina. **Lectura:** revisar esa señal; la fuente cita dependencias lentas o problemas con los datos como posibles indicios y advierte que puede retrasar sistemas posteriores.
4. Una excepción no manejada provoca un estado fallido y deja un rastro de error. **Lectura:** Prefect registra automáticamente esa información; una tarea también puede reportar explícitamente el error como en el ejercicio.

### Preguntar

- «¿Cuál de estos problemas podría permanecer oculto si solo miramos `COMPLETADO`?»
- «¿Qué señal agregarías para conocer el volumen? ¿Y para conocer la frescura?»

No presentar deriva, alertas o paneles como parte del ejercicio de hoy: el resumen fuente los menciona únicamente como posibles temas avanzados que se apoyan en esta base.

## 65–70 min | Cierre

### Cierre sugerido (literal)

«Para una primera línea de monitoreo no necesitamos registrar todo: hagamos visibles el estado y la duración de la ejecución, y agreguemos explícitamente el conteo y la frescura que Prefect no conoce. Así un flujo completado deja de ser una caja negra: también podemos preguntarnos qué procesó y cuánto tardó».

### Chequeo final

Pedir al grupo que responda, sin consultar la tabla:

1. ¿Qué dos dimensiones registra Prefect automáticamente como base?
2. ¿Cuáles dos requieren instrumentación explícita?
3. ¿Qué devuelve la tarea `load_data` instrumentada?
4. Si un flujo completado procesa cero filas, ¿qué señal permite detectar el problema?

**Siguiente paso sugerido por la fuente:** revisar uno de los propios flujos y añadir una sola señal, por ejemplo un conteo de filas o una impresión de duración, para comprobar cuánta más información ofrece una ejecución visible.

## Nota de trazabilidad

El contenido técnico de esta guía proviene de `class_60/tutorial.json`. Los tiempos, el orden de exposición, las preguntas, las frases literales y las adaptaciones 60/75 minutos son estructura docente. No se agregan comandos de ejecución, instalación, librerías, ejemplos ni prompts externos que no figuren en la fuente scrapeada.
