# Clase 51: Procesamiento en segundo plano, disparadores y cronjobs

## Hilo de continuidad

Esta clase conecta el procesamiento de datos de las clases anteriores con una pregunta operativa: ¿quien inicia el trabajo y como garantizamos que termine correctamente? El alumnado pasa de ejecutar tareas en una solicitud a delegarlas en segundo plano, elegir el disparador adecuado y programar el script nocturno del proyecto.

**Transicion literal**

> Hasta ahora hemos pensado en lo que hace nuestro pipeline. Hoy pensamos en cuando empieza, quien lo inicia y como sabemos si termino bien. Un trabajo automatico no es confiable solo porque se ejecute: debe estar desacoplado, ser observable, evitar solapamientos y poder recuperarse de fallos.

## Fuentes y trazabilidad

El contenido tecnico de esta guia procede exclusivamente de `tutorial.json`, `tutorial_2.json`, `tutorial_3.json` y `ai-eng-cronjobs_project_README.es.md`.

La agenda, las frases literales, las preguntas de chequeo y la organizacion temporal son estructura docente añadida. Los tutoriales no contienen prompts de OpenClaw; por eso esta guia no inventa ninguno.

## Objetivos

Al finalizar, el alumnado podra:

1. Explicar la diferencia entre ejecucion sincronica y procesamiento en segundo plano.
2. Decidir cuando delegar una tarea fuera del ciclo solicitud-respuesta.
3. Identificar los cinco tipos de disparador: usuario, maquina/telemetria, cronjob, terceros y encadenado.
4. Leer expresiones cron de cinco campos.
5. Diseñar un cronjob con observabilidad, prevencion de solapamientos y manejo de fallos.
6. Relacionar esos principios con el script `scripts/nightly_export.py` del proyecto.

## Agenda de 60 minutos

| Tiempo | Bloque | Resultado |
| --- | --- | --- |
| 0-7 min | Problema y procesamiento en segundo plano | Separar solicitud y trabajo largo |
| 7-17 min | Principios de confiabilidad | Delegacion, idempotencia, desacoplamiento, observabilidad y durabilidad |
| 17-27 min | Disparadores | Clasificar el evento que inicia un trabajo |
| 27-39 min | Cron y expresiones | Leer y proponer horarios |
| 39-52 min | Cronjob confiable | Estado, logs, solapamientos y excepciones |
| 52-58 min | Proyecto DEV-53 | Diseñar el flujo del script nocturno |
| 58-60 min | Cierre | Comprobar decisiones y riesgos |

Para llegar a 75 minutos, ampliar el ejercicio de clasificación y leer en vivo el ejemplo de trabajo de reporte con `APScheduler`. Para recortar a 60, omitir la implementación detallada de FastAPI y centrarse en el script independiente del proyecto.

## Preparacion del profesor

- Tener disponible esta guia y el proyecto de la clase.
- Pedir la copia del monorepo sobre la que trabaja cada estudiante.
- Confirmar que el proyecto contiene las tablas de telemetria y el pipeline del Hito 6.
- No mezclar `job_runs` con `pipeline_runs`: pertenecen a capas distintas.
- Recordar que el CSV es backup/auditoria; el pipeline lee desde `telemetry_events` en la base de datos.

## Guion docente

### 0-7 min: Por que sacar trabajo de la solicitud

**Que decir (literal)**

> Una solicitud web tiene un contrato: el usuario envia una peticion y espera una respuesta rapida. Enviar un correo, generar un PDF o redimensionar una imagen puede tardar demasiado o depender de un servicio externo. Si hacemos ese trabajo dentro del manejador, bloqueamos la respuesta. El procesamiento en segundo plano permite reconocer la solicitud, delegar el trabajo y continuar de forma independiente.

Explicar el flujo:

```text
Solicitud sincronica:
solicitud -> manejador ejecuta todo -> respuesta

Procesamiento en segundo plano:
solicitud -> manejador delega -> respuesta inmediata
                         -> trabajador ejecuta el trabajo
```

La pregunta de diseño es: **¿puede el usuario esperar a que termine antes de recibir la respuesta?** Si la respuesta es si, puede mantenerse sincronica. Si la respuesta es no, se envia al segundo plano.

**Pregunta de chequeo:** "¿Generar un informe PDF pesado dentro del endpoint puede retrasar la respuesta?"

**Respuesta esperada:** Si. Es una tarea computacionalmente costosa y debe delegarse.

### 7-17 min: Cinco principios de confiabilidad

**Que decir (literal)**

> Delegar no basta. Un trabajo separado tambien puede ejecutarse dos veces, fallar sin registro o quedar a medias. Por eso usamos cinco principios: delegacion, idempotencia, desacoplamiento, observabilidad y durabilidad.

- **Delegacion:** el manejador recibe y valida; el ejecutor hace el trabajo largo.
- **Desacoplamiento:** productor y consumidor son independientes.
- **Idempotencia:** repetir una tarea produce el mismo resultado que ejecutarla una vez; evita correos duplicados, cargos dobles y registros repetidos.
- **Observabilidad:** registrar estado, marcas de tiempo y error hace visible el trabajo.
- **Durabilidad:** persistir la tarea y su resultado permite continuar frente a fallos.

Usar esta secuencia de estados para una tarea:

```text
pending -> processing -> completed
                     \-> failed
```

En el material de cronjobs, un registro de ejecucion incluye `job`, `started_at`, `status`, `error` y `finished_at`. Para fragmentos de datos, la secuencia es `pending -> processing -> done` o `failed`.

**Pregunta de chequeo:** "Si un reintento puede duplicar un cobro, ¿que propiedad falta?"

**Respuesta esperada:** Idempotencia.

### 17-27 min: Que inicia un trabajo

**Que decir (literal)**

> Un disparador es el evento que hace que comience un trabajo en segundo plano. El disparador dice cuando y por que iniciar; el trabajo ejecuta la tarea. Estan conectados, pero el disparador no espera a que el trabajo termine.

Presentar las cinco categorias:

| Señal | Disparador | Ejemplo |
| --- | --- | --- |
| Accion humana | Usuario | Clic en "Descargar informe" |
| Condicion del sistema | Maquina/telemetria | Tasa de error superior al umbral |
| Hora programada | Cronjob | Resumen cada lunes a las 8:00 |
| Evento externo | Terceros | Webhook `payment.succeeded` |
| Finalizacion previa | Encadenado | Trabajo B empieza al terminar A |

Pseudocodigo del tutorial:

```javascript
function determinarTipoDisparador(evento) {
  if (evento.esAccionUsuario) return 'disparado por usuario';
  if (evento.esCondicionSistema) return 'disparado por máquina/telemetría';
  if (evento.esTiempoProgramado) return 'disparado por cronjob';
  if (evento.esWebhookExterno) return 'disparado por terceros';
  if (evento.esFinalizacionTrabajo) return 'procesamiento encadenado';
}
```

**Ejercicio oral:** clasificar estos casos: exportar al pulsar un boton, alertar cuando la API supera el 10% de errores, enviar un resumen semanal y procesar un webhook de Stripe.

**Respuestas:** usuario, maquina/telemetria, cronjob y terceros, respectivamente.

### 27-39 min: Cronjobs y expresiones

**Que decir (literal)**

> Un cronjob es un trabajo en segundo plano activado por tiempo. No empieza porque una persona hizo clic ni porque llego un webhook: empieza porque el reloj indica que toca ejecutarlo.

La expresion cron del material tiene cinco campos:

```text
minuto hora dia_del_mes mes dia_de_la_semana
```

Valores indicados en el tutorial:

- Minuto: `0-59`
- Hora: `0-23`
- Dia del mes: `1-31`
- Mes: `1-12`
- Dia de la semana: `0-6`, domingo es `0`
- `*` significa "cada"

Ejemplos exactos:

```text
0 9 * * 1   # 9:00 todos los lunes
0 * * * *   # al inicio de cada hora
0 0 * * *   # medianoche todos los dias
0 0 1 * *   # medianoche del primer dia de cada mes
@daily      # una vez al dia
@hourly     # una vez por hora
@weekly     # una vez por semana
```

**Preguntas de chequeo:**

- "¿Que tipo de disparador usar para el resumen semanal?" Respuesta: cronjob.
- "¿Que expresion representa medianoche diaria?" Respuesta: `0 0 * * *`.
- "¿Que campo representa el dia de la semana?" Respuesta: el quinto.

### 39-52 min: Construir un cronjob confiable

**Que decir (literal)**

> Programar el horario es solo el comienzo. Un cronjob confiable debe responder tres preguntas: ¿se ejecuto?, ¿tuvo exito? y ¿que hizo exactamente? Para responderlas necesitamos observabilidad, prevencion de solapamientos y manejo explicito de fallos.

Mostrar el registro minimo:

```json
{
  "started_at": "2024-06-01T00:00:00Z",
  "status": "running"
}
```

Al terminar correctamente:

```json
{
  "started_at": "2024-06-01T00:00:00Z",
  "status": "completed",
  "finished_at": "2024-06-01T00:10:00Z"
}
```

Si ocurre una excepcion, el tutorial exige capturarla, registrar el contexto, marcar `failed` y decidir si corresponde reintentar o alertar. La forma conceptual mostrada es:

```python
try:
    # ejecutar el trabajo
    pass
except Exception as e:
    execution = {
        "status": "failed",
        "error": str(e),
        "finished_at": datetime.now().isoformat()
    }
```

El solapamiento ocurre cuando una ejecucion nueva empieza antes de que termine la anterior. Puede duplicar procesamiento, aumentar la carga y producir inconsistencias. Con APScheduler, el ejemplo del tutorial usa:

```python
@scheduler.scheduled_job('cron', hour=0, minute=0, max_instances=1)
def daily_report():
    pass
```

`max_instances=1` permite una sola instancia del mismo trabajo a la vez. El tutorial tambien presenta locks de archivo como alternativa para cronjobs independientes del programador de la aplicacion.

**Pregunta de chequeo:** "Un trabajo tarda 8 minutos y se programa cada 5. ¿Que riesgo aparece?"

**Respuesta esperada:** Solapamiento: dos instancias pueden procesar los mismos datos.

### 52-58 min: Proyecto DEV-53, script nocturno de telemetria

**Que decir (literal)**

> El proyecto combina todo lo anterior. El trabajo es nocturno y por tanto su disparador es un cronjob. Debe vivir fuera del ciclo de FastAPI, registrar su estado, evitar una segunda instancia, ser idempotente por fecha y dejar un resultado observable aunque falle.

Requisitos que deben aparecer en el diseño:

- Crear `job_runs` con `id`, `job_name`, `target_date`, `status`, `started_at`, `finished_at`, `error_message` y `created_at`.
- Añadir un indice en `(job_name, target_date)`.
- Resolver `target_date` desde `TARGET_DATE` o desde ayer en UTC.
- Exportar `telemetry_events` a `data/raw/telemetry_YYYY-MM-DD.csv` solo si no existe.
- Lanzar el pipeline como subproceso despues de exportar:

```bash
python -m data.pipelines.telemetry_kpi_daily.run --no-prefect
```

- Guardar el resultado en `job_runs` y usar `pending -> processing -> completed | failed`.
- Usar el estado `processing` como lock: si ya existe una ejecucion `processing` de `nightly_export`, abortar silenciosamente.
- Si ya existe `completed` para `(job_name='nightly_export', target_date)`, omitir la exportacion y el pipeline.
- Capturar excepciones y asegurar que ninguna ejecucion fallida quede en `processing`.
- Mantener `job_runs` separado de `pipeline_runs`.
- Configurar el disparador en `crontab` o en un scheduler dedicado, nunca dentro del hilo principal de FastAPI.
- Registrar en nivel `INFO` los eventos normales y en `ERROR` las excepciones; cada linea debe incluir timestamp, job y estado.

**Mini plan en pseudocodigo**

```text
resolver target_date
si existe job_runs processing para nightly_export:
    registrar omision y terminar
si existe job_runs completed para target_date:
    registrar duplicado y terminar
crear job_run pending
actualizar job_run a processing
intentar:
    si no existe el CSV:
        exportar telemetry_events a data/raw/
    ejecutar el pipeline como subprocess
    actualizar job_run a completed
except Exception:
    actualizar job_run a failed con el mensaje
    registrar ERROR
```

La justificacion del PR debe indicar la expresion cron y la opcion elegida, incluir un log exitoso, uno fallido o bloqueado y una muestra del CSV.

## Cierre de 58-60 min

**Que decir (literal)**

> Un sistema asincrono confiable no se define solo por hacer trabajo mas tarde. Se define por saber quien lo inicia, separar el trabajo de la solicitud, registrar cada transicion, evitar duplicados y dejar un estado recuperable cuando algo falla.

Preguntas finales:

1. ¿Por que el script nocturno debe ser independiente de FastAPI? Porque no debe bloquear endpoints ni ejecutarse en el hilo principal.
2. ¿Que propiedad evita exportar y lanzar dos veces el pipeline para la misma fecha? Idempotencia mediante `target_date`.
3. ¿Que estado funciona como lock en el proyecto? `processing`.
4. ¿A que estado pasa una ejecucion con excepcion? `failed`, con el mensaje del error.
5. ¿Lee el pipeline el CSV de backup? No; lee `telemetry_events` desde la base de datos.

## Checklist de salida

- [ ] El alumnado distingue solicitud sincronica y trabajo en segundo plano.
- [ ] Puede clasificar los cinco tipos de disparador.
- [ ] Puede leer `0 0 * * *` y `0 9 * * 1`.
- [ ] Explica observabilidad, solapamiento y manejo de fallos.
- [ ] Puede dibujar `pending -> processing -> completed | failed`.
- [ ] El diseño del proyecto incluye `TARGET_DATE`, lock por `processing`, idempotencia por fecha y `job_runs` separado de `pipeline_runs`.

## Plan de contingencia

Si no se puede ejecutar el proyecto en vivo, resolver el flujo con el pseudocodigo y pedir que cada estudiante justifique el disparador, el lock, la condicion de idempotencia y la transicion de error. Si sobra tiempo, comparar el lock de `processing` del proyecto con `max_instances=1` de APScheduler y preguntar que capa controla cada mecanismo.