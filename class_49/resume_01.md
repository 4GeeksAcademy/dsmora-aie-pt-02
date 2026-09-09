# Clase 49: Construir un pipeline de datos resiliente con Prefect

## Hilo de continuidad

En la clase 48 el alumnado documento el diseno de un pipeline de desempeno de negocio. La fuente sigue siendo `telemetry_events`, pero el destino es una tabla nueva bajo `reporting`; el reporte tecnico y `GET /telemetry/report` no se modifican.

**Frase de transicion para decir en clase**

> Ayer decidimos que datos mover, como transformarlos y donde dejarlos. Hoy convertimos ese diseno en un sistema que puede ejecutarse sin supervision: Prefect coordina las etapas, registra lo que ocurre y nos permite reintentar o continuar cuando una parte falla.

La clase anade la implementacion de la Parte 2 del proyecto: flows y tasks, resiliencia, idempotencia, caché, ejecucion por linea de comandos y endpoints separados para reporting.

## Fuentes y limite de trazabilidad

Esta guia usa exclusivamente:

- `tutorial.json`: recorrido de los datos desde fuentes hasta almacenamiento y entrega.
- `tutorial_2.json`: Prefect, flows, tasks, estados, logs, bloques, reintentos, caché y ejecucion.
- `ai-eng-data-pipeline-build_project_README.es.md`: requisitos de la Parte 2 del proyecto.

La agenda, las preguntas, la secuenciacion y los tiempos son estructura docente. Los tutoriales no contienen prompts para OpenClaw; por tanto, no se incluye ningun prompt inventado.

## Objetivos de aprendizaje

Al finalizar, el alumnado podra:

1. Separar ejecucion de datos y orquestacion.
2. Definir un `@flow` y tasks `@task` con entradas, salidas y dependencias explicitas.
3. Configurar reintentos para servicios externos y caché para una transformacion costosa.
4. Permitir que una task opcional falle sin detener el flujo principal.
5. Implementar una carga idempotente y registrar la metadata de cada corrida.
6. Ejecutar `data/pipelines/pipeline.py` como script y exponer estado, disparo manual y KPIs desde `services/reporting/`.

## Preparacion del profesor

- Tener abiertos `tutorial.json`, `tutorial_2.json` y el README del proyecto.
- Pedir al alumnado su `data/pipelines/PIPELINE_DESIGN.md` aprobado en la clase anterior.
- Recordar que `CONTEXT-company.md` es la fuente de verdad para nombres de KPI, tabla destino, campos y frecuencia.
- Confirmar que trabajan en su copia del monorepo, no en un repositorio nuevo.
- Avisar que la instalacion de Prefect indicada por el proyecto es:

```bash
uv add "prefect>=3"
```

## Agenda

| Tiempo | Bloque | Resultado visible |
| --- | --- | --- |
| 0-8 min | Continuidad y arquitectura | El diseno de la clase 48 convertido en etapas ejecutables |
| 8-20 min | Fuentes, ingesta y transformacion | Separacion entre dato bruto, dato limpio y consumo |
| 20-34 min | Flows y tasks | Un flow Prefect con extraccion, transformacion y carga |
| 34-47 min | Resiliencia | Reintentos, estados, fallo opcional y caché |
| 47-59 min | Implementacion del proyecto | Checklist de `pipeline.py`, idempotencia, logs y endpoints |
| 59-60 min | Cierre | Preguntas de comprobacion |

Para extender a 75 minutos, usar los escenarios de fallo y el ejercicio completo de tasks. Para recortar a 60, omitir la demostracion de la interfaz y dejar los endpoints como checklist de implementacion.

## Guion docente

### 0-8 min: Del diseno aprobado al pipeline

**Que decir (literal)**

> Un pipeline de datos es una serie de etapas que transforma datos en bruto en un formato limpio y estructurado que un modelo de IA o una API puede usar. Las etapas que vamos a conservar son recolectar, ingerir, transformar, consumir y entregar. La diferencia de hoy es que ya no las describimos solamente: las organizamos para que se puedan observar y recuperar.

**Que explicar:** el tutorial distingue cinco partes: fuentes, ingesta, transformacion, entrenamiento o inferencia, y almacenamiento o entrega por API. La ingesta mueve los datos sin modificarlos; la transformacion limpia, normaliza y estructura. Separar ambas permite reprocesar si cambia la logica de transformacion.

**Pregunta de chequeo:** "En que etapa se limpian los datos?"

**Respuesta esperada:** en transformacion, no durante la ingesta.

**Enlace:** el pipeline ya tiene etapas; ahora necesitamos una capa que decida el orden, registre estados y gestione fallos. Esa capa es la orquestacion.

### 8-20 min: Fuentes, ingesta y transformacion

**Que decir (literal)**

> Una fuente puede ser comportamiento de usuario, una integracion externa o almacenamiento interno. Cada fuente tiene distinto formato, volumen y frecuencia. La ingesta trae el dato al almacenamiento bruto exactamente como se recibe. Despues, la transformacion elimina duplicados, trata valores faltantes y normaliza tipos y marcas de tiempo.

Relacionar el contenido con el proyecto:

- `telemetry_events` es la fuente que lee la task de extraccion.
- La extraccion debe ser de solo lectura.
- La transformacion prepara los datos para los KPIs definidos en `CONTEXT-company.md`.
- La carga escribe en la tabla nueva bajo `reporting`, nunca en `telemetry_events`.

Mostrar el pseudocodigo de ingesta que aparece en el tutorial:

```javascript
function batchIngest() {
  const newEvents = queryPostgres('SELECT * FROM user_events WHERE ts > last_run');
  writeToDataLake('raw/user_events/' + currentDate() + '.json', JSON.stringify(newEvents));
}
```

**Que explicar:** este ejemplo representa ingesta por lotes: consulta los eventos posteriores a `last_run`, los almacena en bruto y no los transforma en esa etapa. El tutorial tambien contrasta streaming, que procesa los datos a medida que llegan y es adecuado cuando se necesita baja latencia.

**Pregunta de chequeo:** "Por que guardar el dato bruto sin limpiarlo primero?"

**Respuesta esperada:** porque permite reprocesar los datos si cambia la logica de transformacion.

### 20-34 min: Prefect, flows y tasks

**Que decir (literal)**

> Ejecutar es hacer el trabajo: leer, transformar y escribir. Orquestar es definir el orden, rastrear exito o fallo, manejar reintentos y dar visibilidad del progreso. Prefect agrega esa capa sobre funciones Python existentes sin obligarnos a reescribir la logica principal.

Presentar un flow minimo basado en el ejemplo del tutorial:

```python
from prefect import flow

@flow(name="telemetry-ingestion", description="Ingiere eventos diarios de telemetria")
def ingest_telemetry(date: str) -> int:
    count = 42
    return count

result = ingest_telemetry(date="2024-06-01")
print(result)
```

**Que explicar:** `@flow` convierte una funcion Python en el limite de orquestacion. `name` aparece como etiqueta legible y `description` documenta la intencion. Los argumentos se convierten en parametros registrados; el valor de retorno queda asociado a la ejecucion.

Mostrar la task del tutorial:

```python
from prefect import task

@task(name="load-events", description="Persiste los eventos procesados en la base de datos")
def load_events(events: list[dict]) -> int:
    print(f"Cargando {len(events)} eventos")
    return len(events)
```

**Que explicar:** una task es una unidad discreta y rastreable. Tiene su propio estado, logs y comportamiento opcional de reintento. Las tasks reciben entradas Python, devuelven salidas y Prefect infiere dependencias a partir de esos valores; no se debe depender de estado mutable compartido.

**Aplicacion al proyecto:** el flow principal debe conectar, como minimo, una task de extraccion, una de transformacion y una de carga. Las funciones de negocio permanecen en `data/pipelines/`; los endpoints de `services/reporting/` importan esas funciones y no duplican el ETL.

### 34-47 min: Resiliencia, estados y observabilidad

**Que decir (literal)**

> Un pipeline resiliente no es uno que nunca falla. Es uno que falla bien: reintenta lo transitorio, deja registro de lo ocurrido y permite que un paso opcional falle sin tumbar el trabajo principal.

Explicar los tres requisitos del README del proyecto:

1. **Fallos parciales:** una task critica detiene el flow; una task opcional se invoca con `return_state=True`, se registra su fallo y el flow continua.
2. **Reintentos:** toda task que contacte una base de datos o API externa debe definir `retries` y `retry_delay_seconds`. El proyecto pide justificar el numero elegido en un comentario.
3. **Caché:** una transformacion costosa puede usar `cache_key_fn` y `cache_expiration` para reutilizar un resultado valido reciente.

**Que explicar sobre estados:** Prefect muestra estados como Running, Completed y Failed. La interfaz lista nombre, estado, hora de inicio y duracion del flow. En el detalle aparecen parametros, ejecuciones de tasks y una linea temporal de logs.

Comando exacto del tutorial para abrir la interfaz local:

```bash
prefect server start
```

La interfaz se abre en `http://localhost:4200`.

**Ejecucion local y conectada**

**Que decir (literal)**

> El mismo flow puede ejecutarse directamente en Python o conectado a un servidor Prefect. En local, Prefect conserva el estado en memoria y muestra los logs en la consola. Si configuramos `PREFECT_API_URL`, el flow envia el estado y los logs a un servidor local o a Prefect Cloud sin cambiar el codigo del flow.

Comandos exactos para la demostracion conectada:

```bash
prefect server start
export PREFECT_API_URL=http://localhost:4200/api
python mi_pipeline.py
unset PREFECT_API_URL
```

**Que explicar:** sin `PREFECT_API_URL`, la ejecucion es local y el estado es efimero; con `http://localhost:4200/api`, la ejecucion aparece en la interfaz con historial y logs centralizados. Al quitar la variable se vuelve a la ejecucion local.

**Prefect Blocks y secretos**

**Que decir (literal)**

> Un Prefect Block es un objeto de configuracion reutilizable y versionado que se guarda en el servidor de Prefect. Sirve para conectar el flow con servicios externos sin escribir la configuracion directamente en el codigo. Los datos sensibles, como claves API, contrasenas o tokens, deben mantenerse en bloques secretos y no en el repositorio.

**Pregunta de chequeo:** "Que deberia ir en un bloque y que no deberia quedar escrito en `pipeline.py`?"

**Respuesta esperada:** la configuracion reutilizable y las credenciales de servicios externos; no los secretos en texto plano dentro del codigo.

**Pregunta de chequeo:** "Que diferencia hay entre reintentar una task externa y usar caché en una transformacion?"

**Respuesta esperada:** el reintento absorbe un fallo transitorio de un servicio externo; la caché evita repetir un calculo cuyo resultado reciente sigue siendo valido.

### 47-59 min: Implementacion del proyecto

**Que decir (literal)**

> El documento aprobado es nuestra especificacion. No vamos a inventar una tabla, un KPI ni un nombre de campo: los tomamos del `CONTEXT-company.md`. La implementacion debe reflejar exactamente ese diseno.

Checklist que el profesor debe recorrer con el alumnado:

- Ejecutar `git pull`.
- Crear o completar `data/pipelines/pipeline.py`.
- Implementar un flow con tasks independientes de extraccion, transformacion y carga.
- Leer `telemetry_events` en modo solo lectura.
- Escribir en la tabla de destino bajo `reporting` que indica el contexto.
- Configurar `retries` y `retry_delay_seconds` en las tasks externas.
- Invocar una task no critica con `return_state=True`.
- Configurar `cache_key_fn` y `cache_expiration` en una transformacion costosa.
- Hacer idempotente la carga usando la estrategia y el constraint unico del diseno.
- Registrar hora de inicio, hora de fin, registros procesados, estado final y errores.
- Permitir la ejecucion directa como script y comprobar:

```bash
python data/pipelines/pipeline.py
```

- Mantener los tres endpoints en `services/reporting/`: estado y metadata, disparo manual y consulta de filas de KPI.

**Mapa de endpoints y responsabilidades**

Explicar este reparto antes de que los equipos escriban endpoints:

| Endpoint de `services/reporting/` | Funcion que debe invocar | Resultado |
| --- | --- | --- |
| Estado de la ultima corrida | Funcion de lectura de metadata de corrida | Estado, hora de inicio, hora de fin, registros procesados y errores |
| Disparo manual | Flow principal de `data/pipelines/pipeline.py` | Inicia la corrida sin duplicar la logica ETL en el endpoint |
| Consulta de KPIs | Funcion de lectura de la tabla de destino | Filas de KPI con el contrato exacto del `CONTEXT-company.md` |

**Que decir (literal)**

> Los endpoints solo exponen el pipeline. El endpoint de estado lee la metadata, el endpoint manual llama al flow y el endpoint de KPIs consulta la tabla de reporting. Ninguno transforma datos por su cuenta ni escribe en `telemetry_events`.

**Mini plan en pseudocodigo para el proyecto**

```text
git pull
instalar prefect>=3
leer PIPELINE_DESIGN.md y CONTEXT-company.md
definir task extract: leer telemetry_events en solo lectura
definir task transform: limpiar, normalizar y preparar los KPIs
definir task load: escribir con la estrategia idempotente del diseño
definir task opcional: registrar una salida secundaria con return_state=True
definir flow: extract -> transform -> load y registrar metadata
configurar reintentos, caché y Prefect Blocks
crear endpoints separados en services/reporting/
ejecutar python data/pipelines/pipeline.py
verificar estados, logs, filas de KPI y ausencia de duplicados
```

**Preguntas de chequeo:** "Que endpoint llama al flow?" Respuesta: el de disparo manual. "Que endpoint consulta la tabla de destino?" Respuesta: el de KPIs. "Donde vive la transformacion?" Respuesta: en `data/pipelines/`, nunca en `services/reporting/`.

**Idempotencia: que preguntar**

> Si corremos dos veces el mismo rango, que evita que la tabla de reporting tenga duplicados?

La respuesta debe usar la estrategia documentada en la Parte 1: upsert, tabla de control, timestamp u otra, apoyada en el constraint unico del `CONTEXT-company.md`. No aceptar una respuesta generica que use `telemetry_events` como destino.

**Ejercicio guiado de 75 minutos:** pedir que cada equipo marque en su documento una task critica, una opcional, una externa con reintentos y una transformacion con caché. Despues deben indicar que ocurre si falla cada una y que campos quedan en el log.

### 59-60 min: Cierre

**Que decir (literal)**

> Hoy el diseno se convirtio en un flujo operable. Prefect no reemplaza la logica de extraccion, transformacion o carga: la coordina, la observa y permite recuperarla. La siguiente comprobacion es que el pipeline pueda ejecutarse como script, que la carga sea idempotente y que reporting quede separado de telemetria.

Preguntas finales:

1. "Que decorador convierte una funcion en un flow?" Respuesta: `@flow`.
2. "Que decorador convierte una funcion en una task rastreable?" Respuesta: `@task`.
3. "Que tres etapas son obligatorias en el flow del proyecto?" Respuesta: extraccion, transformacion y carga.
4. "Donde debe vivir la logica ETL?" Respuesta: en `data/pipelines/`, no en `services/reporting/`.
5. "Que comando demuestra la ejecucion por CLI?" Respuesta: `python data/pipelines/pipeline.py`.

## Variante de tiempo

- **60 minutos:** usar solo el flow minimo, la tabla de requisitos y las cinco preguntas finales.
- **75 minutos:** ejecutar la practica de tasks, abrir `prefect server start`, revisar estados y resolver los escenarios de task opcional, reintento, caché e idempotencia.

## Plan de contingencia

- Si no se puede iniciar la interfaz, continuar con los estados y logs descritos en el tutorial y revisar la ejecucion del script.
- Si el monorepo no esta disponible, trabajar sobre la estructura conceptual `data/pipelines/` y dejar pendientes los nombres exactos del contexto; no inventar KPIs ni tabla destino.
- Si falla una task externa, distinguir si corresponde reintentar o marcarla como opcional; no ocultar el error.
- Si no hay tiempo para endpoints, verificar primero el flow, la carga idempotente y la metadata de corrida; los endpoints quedan como el siguiente bloque de implementacion.

## Checklist final del profesor

- [ ] Se explico la continuidad con el diseno de la clase 48.
- [ ] Se distinguieron ejecucion y orquestacion.
- [ ] Se mostro un `@flow` y una `@task`.
- [ ] Se explicaron reintentos, `return_state=True`, caché y estados.
- [ ] Se reviso la ejecucion `python data/pipelines/pipeline.py`.
- [ ] Se insistio en la idempotencia y en los cinco campos de metadata.
- [ ] Se mantuvieron separados `services/reporting/` y `services/telemetry/`.
- [ ] Se aclaró que no hay prompts de OpenClaw en las fuentes de esta clase.