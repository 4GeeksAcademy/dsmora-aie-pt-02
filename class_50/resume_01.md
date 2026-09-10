# Clase 50: Pipelines Prefect listos para producción

## Hilo de continuidad

En la clase 49 el alumnado implementó la Parte 2 del proyecto: un flow principal con tasks de extracción, transformación y carga, reintentos para servicios externos, caché para una transformación costosa, y `data/pipelines/pipeline.py` ejecutable como script, con endpoints separados en `services/reporting/`.

**Frase de transición para decir en clase**

> Ayer construimos un flow que funciona. Hoy nos preguntamos qué pasa cuando ese flow crece, cuando una task falla de verdad, o cuando nadie está mirando la terminal para dispararlo. Vamos a dividirlo en piezas más pequeñas, ponerle pruebas, programarlo para que corra solo, y — lo que de verdad le importa al liderazgo — poner los KPIs frente a un dashboard legible.

La clase añade la Parte 3 del proyecto: refactor del flow principal en subflows, tests unitarios de las tasks de transformación, preservación del entrypoint CLI y un dashboard de negocio en `uis/backoffice/`.

## Fuentes y límite de trazabilidad

Esta guía usa exclusivamente:

- `tutorial.json`: subflujos, manejo de fallas, caché de resultados, reintentos, programación de despliegues, pruebas locales y creación de despliegues.
- `ai-eng-milestone-data-pipeline-enhancement_project_README.es.md`: requisitos de la Parte 3 del proyecto.

El tutorial no contiene prompts para OpenClaw; por tanto, esta guía no incluye ninguno inventado. La agenda, los tiempos y las preguntas de chequeo son estructura pedagógica añadida por el agente; el contenido técnico procede solo de las fuentes anteriores.

## Objetivos de aprendizaje

Al finalizar, el alumnado podrá:

1. Distinguir las tres clases de fallas en una canalización (complejidad, datos, infraestructura) y elegir la herramienta correcta para cada una.
2. Extraer un subflujo (`@flow` anidado) con inputs y outputs explícitos para aislar una etapa del pipeline.
3. Configurar `retries` y `retry_delay_seconds` en una task para recuperarse de fallas transitorias de infraestructura.
4. Añadir caché de resultados a una task con `cache_policy`, `cache_expiration` y `persist_result`, y reconocer cuándo NO usarlo.
5. Registrar un flow como despliegue con `.serve()` usando programación por intervalo, cron o RRule, y pausar/reanudar esa programación.
6. Escribir pruebas unitarias de una task llamando directamente a `.fn(...)`, sin levantar el runtime de Prefect.
7. Refactorizar `data/pipelines/pipeline.py` en al menos tres subflows, añadir `tests/pipelines/test_pipeline.py`, preservar el entrypoint CLI y construir el dashboard de `uis/backoffice/`.

## Preparación del profesor

- Tener abierto `tutorial.json` y el README del proyecto.
- Pedir al alumnado su `data/pipelines/pipeline.py` de la Parte 2, ya funcional, y su `CONTEXT-company.md`.
- Confirmar que Prefect 3 sigue instalado (`uv add "prefect>=3"`, ya hecho en la clase 49).
- Confirmar que trabajan en su copia del monorepo, no en un repositorio nuevo.
- Recordar que `telemetry_events` y `services/telemetry/analysis.py` no se tocan durante todo el refactor.

## Agenda

| Tiempo | Bloque | Resultado visible |
| --- | --- | --- |
| 0-6 min | Continuidad y las tres fallas | Vocabulario compartido: falla de complejidad, de datos, de infraestructura |
| 6-20 min | Subflujos y manejo de fallas | Un flow principal que invoca subflujos y sobrevive al fallo de uno de ellos |
| 20-32 min | Reintentos y caché | Task con reintentos configurados y task con caché de resultados |
| 32-44 min | Despliegues y programación | `.serve()` con intervalo/cron, pausa y reanudación |
| 44-54 min | Pruebas unitarias locales | Tests que llaman `.fn(...)` sin runtime de Prefect |
| 54-59 min | Parte 3 del proyecto | Checklist de subflows, tests, CLI y dashboard |
| 59-60 min | Cierre | Preguntas de comprobación |

Para extender a 75 minutos, resolver en vivo el ejercicio completo de "1.1 Subflujos" y añadir el escenario de reintentos con backoff exponencial. Para recortar a 60, dejar la sección de programación (RRule) como lectura y enfocar solo intervalo y cron.

## Guion docente

### 0-6 min: Las tres clases de fallas

**Qué decir (literal)**

> En producción, las fallas son inevitables. Lo que cambia es que ya no las tratamos todas igual: hay fallas de complejidad, fallas de datos y fallas de infraestructura, y cada una necesita una herramienta distinta. Usar la herramienta equivocada desperdicia recursos o deja el problema sin resolver.

**Qué explicar:**
- **Fallas de complejidad**: surgen cuando una canalización crece demasiado para gestionarse como una sola unidad. Se resuelven descomponiéndola en piezas más pequeñas e independientemente observables (subflujos).
- **Fallas de datos**: ocurren cuando una task recibe una entrada mala o inesperada y lanza una excepción, haciendo fallar todo el flow por defecto. Se resuelven con manejo explícito de fallas.
- **Fallas de infraestructura**: problemas transitorios (timeouts de red, servicios caídos momentáneamente) que se resuelven solos. Se resuelven con reintentos.

**Pregunta de chequeo:** "¿Qué herramienta usarías si una API externa falla la mitad de las veces por un timeout?"

**Respuesta esperada:** reintentos (`retries`), porque es una falla de infraestructura transitoria, no un dato incorrecto.

### 6-20 min: Subflujos y manejo de fallas

**Qué decir (literal)**

> Un subflujo es un flow de Prefect llamado desde dentro de otro flow. Agrupa varias tasks relacionadas en una unidad lógica que se ejecuta, rastrea su estado y registra logs de forma independiente del flow padre.

**Ejemplo completo (del tutorial):**

```python
from prefect import flow, task

@task
def fetch_data(source: str) -> list:
    return [f"{source}_record_{i}" for i in range(3)]

@task
def process_data(data: list) -> int:
    return len(data)

@flow(name="process-source")
def process_source(source: str) -> int:
    data = fetch_data(source)
    return process_data(data)

@flow(name="daily-pipeline")
def daily_pipeline():
    sources = ["twitter", "instagram", "spotify"]
    results = [process_source(s) for s in sources]
    print(f"Total de registros procesados: {sum(results)}")
```

**Qué explicar:** `process_source` es el subflujo: tiene sus propias tasks, su propio estado en la interfaz de Prefect y sus propios logs. El flow padre `daily_pipeline` lo llama como cualquier función; cada llamada crea una ejecución de flow independiente, por lo que se puede depurar una fuente que falla sin revisar todos los logs de la canalización completa. Usar un subflujo cuando: la unidad anidada contiene varias tasks, se quiere seguimiento de estado separado, o la misma lógica se reutiliza desde distintos flows padre.

**Ejercicio guiado (del tutorial, "1.1 Subflujos"):** el archivo `pipeline.py` procesa datos de redes sociales de varias fuentes. Un subflujo `process_source` obtiene, filtra y cuenta registros para una fuente; un flow principal `daily_pipeline` lo ejecuta para cada fuente y suma los totales. Faltan dos partes:

```python
from prefect import flow, task

@task
def fetch_data(source: str) -> list:
    print(f"Fetching data from {source}")
    return [f"{source}_record_{i}" for i in range(3)]

@task
def filter_data(data: list) -> list:
    # TODO: mantener solo los registros que contienen 'record_1'
    return data

@task
def process_data(data: list) -> int:
    print(f"Processing {len(data)} records")
    # Falla deliberadamente para la fuente instagram
    if 'instagram' in data[0]:
        raise ValueError("Processing error for instagram data")
    return len(data)

@flow(name="process-source")
def process_source(source: str) -> int:
    data = fetch_data(source)
    filtered = filter_data(data)
    count = process_data(filtered)
    # TODO: envolver process_data para que, si lanza excepción,
    # el subflujo registre el error y devuelva 0 en vez de propagar el fallo
    return count
```

**Tareas del ejercicio:**
1. Implementar `filter_data` para mantener solo registros que contienen `"record_1"`.
2. Hacer que `process_source` sea resistente: si `process_data` lanza una excepción, el subflujo debe registrar el error y devolver `0` para esa fuente, en vez de que toda la tubería falle.

**Resultado esperado:** ejecutar `pipeline.py` corre `daily_pipeline` e imprime el conteo total de registros filtrados entre las fuentes exitosas, con la fuente que falló contribuyendo `0`.

**Pregunta de chequeo:** "¿Por qué la fuente que falla no debe detener el conteo de las otras dos?"

**Respuesta esperada:** porque cada subflujo se ejecuta y falla de forma independiente; aislar el fallo dentro de `process_source` evita que una falla de datos en una fuente colapse todo `daily_pipeline`.

### 20-32 min: Reintentos y caché

**Qué decir (literal)**

> Cuando la falla es transitoria — un timeout momentáneo, una conexión inestable — reintentar es la respuesta correcta. Cuando una task hace un trabajo costoso con las mismas entradas una y otra vez, cachear el resultado es la respuesta correcta. Son herramientas distintas para problemas distintos.

**Reintentos — ejemplo (del tutorial):**

```python
from prefect import task

@task(retries=3, retry_delay_seconds=2, name="call-api")
def call_api(url: str) -> dict:
    # Puede lanzar ConnectionError en problemas transitorios de red
    ...
```

Con `retries=3`, Prefect intenta la task hasta cuatro veces en total (el primer intento más tres reintentos), esperando dos segundos entre cada uno. Límite importante: los reintentos solo ayudan si el problema es temporal; si una task lanza `ValueError` por datos de entrada incorrectos, reintentar fallará las tres veces igual — la entrada no cambió.

**Ejercicio guiado (del tutorial, "1.4 Reintentos en la práctica"):** `app.py` tiene una task `call_api` que simula una API inestable (falla ~50% de las veces) y un flow `fetch_with_retry` que la llama. Actualmente se rinde demasiado pronto.

```python
from prefect import task, flow
import random
import time

@task(retries=2, retry_delay_seconds=1)
def call_api():
    # Simula una llamada de API inestable con 50% de probabilidad de fallo
    if random.random() < 0.5:
        raise Exception("API call failed")
    return "Success"

@flow
def fetch_with_retry():
    result = call_api()
    return result

if __name__ == "__main__":
    result = fetch_with_retry()
    print(f"API call result: {result}")
```

**Tarea:** configurar `call_api` para que reintente hasta 4 veces con 3 segundos de retraso entre intentos (ajustar `retries` y `retry_delay_seconds`).

**Resultado esperado:** al ejecutar `app.py` varias veces, cuando los primeros intentos fallen, los logs de Prefect muestran cada reintento y su retraso, y el flow termina con éxito una vez que un intento funciona.

**Caché — ejemplo (del tutorial):**

```python
from prefect import task
from prefect.cache_policies import INPUTS
from datetime import timedelta

@task(
    cache_policy=INPUTS,                  # clave de caché a partir de las entradas de la task
    cache_expiration=timedelta(hours=1),  # resultado en caché válido por 1 hora
    persist_result=True,                  # el caché requiere que el resultado se persista
)
def load_large_dataset(date: str) -> list:
    print(f"Cargando datos para {date}")
    return ["data"]
```

**Qué explicar:** el caché permite a Prefect omitir la ejecución de una task si ya se ejecutó recientemente con las mismas entradas, devolviendo el resultado guardado al instante. `INPUTS` construye la clave de caché a partir de los argumentos; también existen `DEFAULT` (entradas + código de la task + id de ejecución del flow), `TASK_SOURCE` (solo el código) y `NO_CACHE`. El caché depende de que el resultado se persista: `persist_result=True` por task, o `prefect config set PREFECT_RESULTS_PERSIST_BY_DEFAULT=true` globalmente.

**Cuándo usarlo:** funciones puras, operaciones de E/S costosas (archivos grandes, APIs, bases de datos), transformaciones idempotentes.

**Cuándo NO usarlo:** tasks con efectos secundarios (escribir en BD, enviar correos) — en un acierto de caché la task se omite completamente y el efecto secundario no ocurre; o tasks que dependen de estado externo no capturado en los parámetros (hora actual, datos en vivo).

**Pregunta de chequeo:** "¿Por qué no se debe cachear una task que escribe en la base de datos?"

**Respuesta esperada:** porque un acierto de caché omite la ejecución completa de la task, así que el efecto secundario (la escritura) nunca ocurriría en las reejecuciones cacheadas.

### 32-44 min: Despliegues y programación

**Qué decir (literal)**

> Programar un flow permite que se ejecute solo, sin que nadie tenga que activarlo a mano. Prefect soporta tres cadencias: intervalo, cron y RRule, y todas se registran llamando a `.serve()` sobre el flow.

**Programación por intervalo (del tutorial):**

```python
from prefect import flow
from datetime import timedelta, date

@flow(name="daily-report")
def daily_report():
    print(f"Ejecutando reporte diario para {date.today()}")

if __name__ == "__main__":
    daily_report.serve(name="daily-report-deployment", interval=timedelta(hours=24))
```

`interval` acepta cualquier `timedelta`; `.serve()` registra el flow como despliegue y arranca un proceso ligero que dispara una ejecución cada 24 horas.

**Programación cron (del tutorial):**

```python
if __name__ == "__main__":
    daily_report.serve(name="weekday-morning-report", cron="0 9 * * 1-5")
```

Útil cuando se necesita una hora exacta del reloj (por ejemplo, cada día laborable a las 9 AM) en vez de un intervalo fijo. Para fijar zona horaria (importante en cambios de horario de verano), pasar un objeto de programación con `timezone` en vez de la cadena cron simple.

**Programación RRule (del tutorial):**

```python
if __name__ == "__main__":
    # Último viernes de cada mes
    daily_report.serve(name="end-of-month-report", rrule="FREQ=MONTHLY;BYDAY=-1FR")
```

Basada en el estándar RFC 5545; se usa cuando el patrón de negocio no se puede expresar con intervalo o cron simples (ej. "el último viernes de cada mes").

**Pausar y reanudar (del tutorial):**

```bash
prefect deployment pause my-flow/daily-report-deployment
prefect deployment resume my-flow/daily-report-deployment
```

Pausar detiene que el servidor cree nuevas ejecuciones programadas; las ejecuciones ya en cola siguen corriendo. Es seguro pausar durante un despliegue de código actualizado: pausar, enviar la actualización, reanudar.

**Ejercicio guiado (del tutorial, "3.1 Creación y ejecución de despliegues"):**

```python
from prefect import flow

@flow
def hello_flow():
    # TODO: imprimir exactamente "Hello, Prefect!"
    pass

if __name__ == "__main__":
    # TODO: registrar hello_flow como despliegue llamado "prod-pipeline"
    # llamando a .serve() sobre el flow.
    pass
```

**Tarea:** completar `hello_flow` para que imprima exactamente `"¡Hola, Prefect!"` y registrarlo como despliegue `"prod-pipeline"` con `.serve()`.

**Resultado esperado:** al ejecutar `app.py` se sirve el despliegue `prod-pipeline`, visible en la interfaz de Prefect, donde se puede disparar una ejecución (o esperar su programación) y observar su finalización.

**Pregunta de chequeo:** "Si necesito que un reporte corra el último viernes de cada mes, ¿qué tipo de programación uso?"

**Respuesta esperada:** RRule, porque cron e intervalo no pueden expresar directamente ese patrón.

### 44-54 min: Pruebas unitarias locales

**Qué decir (literal)**

> Antes de que un pipeline llegue a producción, queremos saber si sus tasks de transformación funcionan sin tener que levantar todo el runtime de Prefect. Para eso llamamos directamente a `.fn(...)` sobre la task.

**Ejemplo (del tutorial, "2.2 Prueba de flujos localmente"):** `test_app.py` ya define una task `filter_retweets` que elimina retweets (texto que empieza con `"RT"`) de una lista de diccionarios de tweets:

```python
from prefect import task

@task
def filter_retweets(tweets: list) -> list:
    """Task bajo prueba: elimina retweets (texto que empieza con "RT")."""
    return [tweet for tweet in tweets if not tweet.get("text", "").startswith("RT")]

def test_filter_retweets_mixed():
    tweets = [
        {"text": "Hello world!"},
        {"text": "RT This is a retweet"},
        {"text": "Another tweet"}
    ]
    result = filter_retweets.fn(tweets)
    assert len(result) == 2
    # Añadir más aserciones aquí

def test_filter_retweets_empty():
    tweets = []
    result = filter_retweets.fn(tweets)
    assert result == []

def test_filter_retweets_no_text():
    # TODO: completar según el tutorial
    ...
```

**Tarea:** crear `test_app.py` con pruebas unitarias que cubran:
1. Un caso normal: lista mixta de tweets y retweets, verificando que solo queden los no-retweets.
2. Una lista vacía: el resultado debe ser vacío.
3. Una clave `text` faltante: los tweets sin campo `text` no deben hacer fallar el filtro.

**Resultado esperado:** `pytest test_app.py` pasa todas las pruebas sin errores.

**Qué explicar:** llamar a `filter_retweets.fn(tweets)` en vez de `filter_retweets(tweets)` ejecuta la función interna directamente, sin crear una ejecución de task registrada en Prefect — por eso el test no necesita el runtime del servidor.

**Pregunta de chequeo:** "¿Por qué usamos `.fn(...)` en vez de llamar la task directamente en el test?"

**Respuesta esperada:** porque `.fn(...)` ejecuta la lógica pura de la función sin pasar por el motor de orquestación de Prefect, lo que hace la prueba rápida y aislada.

### 54-59 min: Parte 3 del proyecto — Pipeline a producción

**Resumen del reto:** el pipeline básico de la Parte 2 (`data/pipelines/pipeline.py`) ya funciona. El ticket de mejora pide cuatro cosas antes de la entrega a operaciones:

1. Refactorizar el flow principal en subflows para que cada fase sea independiente, testeable y reutilizable.
2. Añadir tests unitarios para las tasks de transformación.
3. Que `python data/pipelines/pipeline.py` siga corriendo sin errores tras el refactor (conservando el entrypoint de la Parte 2).
4. Un dashboard donde el liderazgo pueda ver los KPIs, no un endpoint que nadie va a consultar con curl.

**Cómo hilar con lo anterior:** los subflows de hoy (`process_source` en el ejemplo) son la misma pieza que se usa para dividir extracción, transformación y carga en el pipeline real de cada equipo; los reintentos y el caché se aplican a las tasks costosas o inestables dentro de esos subflows; las pruebas con `.fn(...)` son las mismas que van en `tests/pipelines/test_pipeline.py`; la programación con `.serve()` es la misma mecánica que sostiene el entrypoint CLI.

**Checklist de la Fase 1 — Subflows:**
- Dividir el flow principal en al menos tres subflows (`@flow`): extracción (desde `telemetry_events` y otras tablas de dominio), transformación, carga (en la tabla destino del `CONTEXT-company.md`). El flow principal los invoca en secuencia.
- Cada subflow con inputs y outputs explícitos, sin depender de variables globales entre subflows.
- Pasos opcionales (notificaciones, exportaciones secundarias) también como subflows, invocados con `return_state=True` desde el flow principal.

**Checklist de la Fase 2 — Tests unitarios:**
- Crear `tests/pipelines/test_pipeline.py` con tests para al menos tres tasks de transformación (las que calculan los KPIs del `CONTEXT-company.md`).
- Cada test aislado: sin base de datos ni APIs externas, con datos de prueba en memoria con la forma de los eventos de telemetría.
- Al menos un test de comportamiento defensivo ante input inválido o malformado.
- Al menos un test que confirme que un KPI calculado coincide con la definición del `CONTEXT-company.md` para un input conocido, calculado a mano.
- `python -m pytest tests/pipelines/test_pipeline.py` debe pasar sin errores.

**Checklist de la Fase 3 — CLI preservado:**
- Tras dividir en subflows, `python data/pipelines/pipeline.py` sigue ejecutando el ETL completo sin errores; el entrypoint `__main__` de la Parte 2 no se reconstruye desde cero.

**Checklist de la Fase 4 — Dashboard de negocio (obligatorio):**
- Página en `uis/backoffice/` (ej. `/reporting`) que consume el endpoint de `services/reporting/` y muestra cada KPI de la sección "KPIs a medir" del `CONTEXT-company.md` (un gráfico o tabla por KPI).
- Cada KPI etiquetado con el mismo nombre que en `CONTEXT-company.md`, mostrando el período (semana o mes) que cubren los datos.
- Dashboard legible para el stakeholder de negocio nombrado en `CONTEXT-company.md`, sin necesitar traducción técnica.

**Mini plan en pseudocódigo:**

```text
1. Abrir pipeline.py de la Parte 2 y localizar las etapas actuales del flow principal
2. Para cada etapa (extracción, transformación, carga):
   a. Extraerla a su propio @flow con nombre de dominio (no "extract_data" genérico)
   b. Definir sus inputs y outputs explícitos
   c. Verificar que el flow principal la invoca en secuencia
3. Escribir tests/pipelines/test_pipeline.py:
   a. Fixture en memoria con forma de telemetry_events del CONTEXT-company.md
   b. Test de caso válido para al menos 3 tasks de transformación
   c. Test de input inválido/malformado (comportamiento defensivo)
   d. Test que valida un KPI calculado a mano contra la definición del CONTEXT
4. Ejecutar python -m pytest tests/pipelines/test_pipeline.py y corregir hasta que pase
5. Ejecutar python data/pipelines/pipeline.py y confirmar que el ETL completo sigue corriendo
6. Construir la página de uis/backoffice/ que consulta services/reporting/
   y renderiza cada KPI etiquetado con su nombre y período
7. (Opcional) Si PIPELINE_DESIGN.md señaló mejoras de resiliencia/observabilidad
   no cubiertas aún, implementarlas y anotar qué pregunta de diseño responden
8. Commit: "feat: refactor business performance pipeline into subflows,
   add unit tests, and add reporting dashboard"
9. Abrir Pull Request y compartir la URL con el tech lead
```

**Nota importante (del brief):** los nombres de subflows, tasks y tests deben seguir el vocabulario de dominio de `PIPELINE_DESIGN.md` y `CONTEXT-company.md`. Un subflow llamado `extract_data` no es aceptable si la empresa tiene entidades concretas y nombres de KPI — nombrarlo según la métrica de negocio real que produce.

**Qué vamos a evaluar (del brief):**
- El flow principal invoca al menos tres subflows en vez de contener toda la lógica directamente.
- Cada subflow tiene inputs/outputs explícitos y puede ejecutarse de forma independiente.
- `tests/pipelines/test_pipeline.py` existe con al menos tres tests unitarios de tasks de transformación, aislados (sin BD ni APIs externas).
- Al menos un test de input inválido y al menos un test que valida un KPI contra su definición en el CONTEXT.
- `python -m pytest tests/pipelines/test_pipeline.py` pasa sin errores.
- `python data/pipelines/pipeline.py` sigue corriendo el ETL completo tras el refactor.
- Nombres de subflows/tasks/tests reflejan el vocabulario de dominio y los KPI del CONTEXT.
- `telemetry_events` y `services/telemetry/analysis.py` permanecen sin modificar.
- Existe el dashboard en `uis/backoffice/` con cada KPI correctamente etiquetado, alimentado desde `services/reporting/`, legible para un stakeholder no técnico.

**Cómo entregar (del brief):**
1. Confirmar que `data/pipelines/pipeline.py`, `tests/pipelines/test_pipeline.py` y la página del dashboard estén commiteados en la copia del monorepo.
2. Commit: `feat: refactor business performance pipeline into subflows, add unit tests, and add reporting dashboard`.
3. Abrir un Pull Request (puede construirse sobre el PR de la Parte 2 o ser uno nuevo). En la descripción, mencionar si se implementó alguna mejora adicional de las preguntas de diseño. Compartir la URL con el tech lead.

### 59-60 min: Cierre

**Preguntas de comprobación para el grupo:**
1. ¿Qué clase de falla resuelve un subflujo, y cuál resuelven los reintentos?
2. ¿Por qué no se debe cachear una task que escribe en base de datos?
3. ¿Qué diferencia hay entre llamar `mi_task(x)` y `mi_task.fn(x)` en un test?
4. ¿Qué programación usarías para "cada día laborable a las 9 AM" y cuál para "el último viernes de cada mes"?

**Cierre sugerido (literal):**

> Con esto, el pipeline deja de ser un script que alguien tiene que acordarse de correr. Tiene piezas que se pueden probar por separado, se recupera solo de fallos transitorios, corre según una programación, y — lo más importante para el negocio — sus resultados están en un dashboard que alguien va a mirar de verdad.

## Plan de contingencia

- Si Prefect no está disponible o falla la instalación, avanzar solo con los ejemplos de código del tutorial en pizarra/pantalla, sin ejecutar, y dejar la ejecución como tarea.
- Si no hay tiempo para el bloque de despliegues, cubrir solo programación por intervalo y dejar cron/RRule como lectura, priorizando subflujos, manejo de fallas y tests (son los evaluados en el proyecto).
- Si un equipo no tiene aún su `CONTEXT-company.md` completo de la Parte 1, usar nombres de KPI y tabla destino genéricos temporales, dejando claro que deben reemplazarse antes de la entrega.
