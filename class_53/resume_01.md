# Clase 53: Redis, workers y Celery con FastAPI

## Hilo de continuidad

La clase 52 separó productor y consumidor y diseñó colas para prioridad, servicio y fallos. Ahora se implementa ese patrón: Redis será el broker, un worker consumirá mensajes y Celery añadirá ACK después del procesamiento, estados, reintentos, colas nombradas y Flower. La transición literal es: «La clase anterior nos dio el modelo; hoy lo conectamos a procesos reales y observamos su ciclo de vida».

Esta guía se basa exclusivamente en `tutorial.json`, `tutorial_2.json`, `tutorial_3.json` y `ai-eng-message-queue_project_README.es.md`. La estructura docente y las frases literales son organización añadida. Los JSON no contienen prompts de OpenClaw; por eso no se inventan.

## Objetivos

- Explicar Redis como broker y distinguirlo del backend de resultados.
- Implementar una cola FIFO con `RPUSH` y `BLPOP`.
- Entender la entrega atómica con múltiples workers.
- Conectar FastAPI con Celery usando `.delay()`.
- Consultar estados `PENDING`, `STARTED`, `SUCCESS`, `FAILURE` y `RETRY`.
- Configurar Flower, reintentos con backoff, prioridad, colas nombradas y chains.
- Relacionar todo con el ticket DEV-55 del monorepo.

## Agenda de 60-75 minutos

| Tiempo | Bloque | Resultado |
| --- | --- | --- |
| 0-8 | Redis y arquitectura | Broker, cola y worker |
| 8-20 | Listas FIFO | Productor y consumidor |
| 20-30 | Múltiples workers | Entrega atómica y timeout |
| 30-43 | Docker y Redis | Levantar y verificar infraestructura |
| 43-58 | FastAPI + Celery | Encolar y consultar tareas |
| 58-70 | Producción | Flower, reintentos, prioridad y chains |
| 70-75 | Proyecto y cierre | DEV-55 y comprobación |

Para 60 minutos, omitir la comparación detallada con Streams y mostrar solo `add_numbers`. Para 75, ejecutar también el pipeline `step_one -> step_two` y revisar Flower.

## Preparación

- Tener Docker disponible y abrir el monorepo de cada estudiante.
- Instalar `redis`, `celery` y `flower` según los comandos del material.
- Mantener separadas las bases Redis 0 para broker y Redis 1 para resultados.
- Preparar dos procesos: API y worker; el worker no vive dentro de FastAPI.

## Guion docente

### 0-8 min: arquitectura

**Qué decir (literal)**

> Redis es un almacén en memoria que también puede actuar como broker: mantiene las tareas hasta que un worker pueda procesarlas. El productor crea el mensaje, Redis lo almacena y el consumidor lo extrae. El flujo es Cliente → API/productor → Redis/broker → worker/consumidor → resultado.

Redis cumple dos roles en Celery: la base 0 transporta mensajes como broker y la base 1 almacena estados y resultados como backend. Una lista cruda con `BRPOP` puede perder silenciosamente una tarea si el worker falla después de extraerla; Celery añade ACK después del procesamiento, reintentos, seguimiento de estado, colas nombradas y Flower.

Pregunta: «¿Qué componente transporta el mensaje y cuál guarda el resultado?». Respuesta: Redis como broker transporta; Redis como backend guarda estado y resultado.

### 8-20 min: productor y consumidor con Redis

**Qué decir (literal)**

> Para una cola FIFO de lista insertamos por la derecha con `RPUSH` y extraemos por la izquierda con `BLPOP`. `BLPOP` bloquea hasta que hay un mensaje o vence el timeout, y su extracción es atómica.

Código del tutorial:

```python
import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
QUEUE = "tasks"

def produce(task: dict):
    task_json = json.dumps(task)
    r.rpush(QUEUE, task_json)

def consume(timeout: int = 30):
    result = r.blpop(QUEUE, timeout=timeout)
    if result:
        _, task_json = result
        return json.loads(task_json)
    return None
```

`produce(task)` recibe un diccionario, lo serializa a JSON y lo añade al extremo derecho. `consume(timeout)` espera como máximo el número de segundos indicado, extrae desde la izquierda, deserializa y devuelve el diccionario; si no llega nada, devuelve `None`.

El timeout finito permite detectar problemas de conexión. No usar `timeout=0` para bloquear indefinidamente: puede dejar al worker colgado y consumir una conexión sin trabajar.

### 20-30 min: varios workers y Streams

**Qué decir (literal)**

> Varios workers pueden competir por la misma lista. Redis garantiza que cada `BLPOP` entregue un mensaje único a exactamente un worker; por eso no se necesita un lock para impedir que dos workers reciban el mismo elemento.

Una lista sirve para una cola FIFO simple donde cada tarea se procesa una vez y el resultado se descarta. Redis Streams es la opción del material cuando los eventos deben reconocerse, volver a entregarse o procesarse con grupos de consumidores, como una canalización de pagos.

Pregunta: «Si hay diez tareas y cinco workers bloqueados en `BLPOP`, ¿cuántos workers reciben cada tarea?». Respuesta: exactamente uno.

### 30-43 min: Redis con Docker

Ejecutar exactamente:

```bash
docker run -d -p 6379:6379 --name redis-broker redis
docker exec -it redis-broker redis-cli ping
```

La segunda orden debe mostrar `PONG`. Para el cliente Python, el tutorial indica:

```bash
pip install redis
```

El material también pide un `docker-compose` mínimo con Redis y el puerto `6379`; en el proyecto DEV-55 se exige además política `noeviction` y Flower en `5555`.

### 43-58 min: FastAPI y Celery

**Qué decir (literal)**

> Celery no es el broker. Es la capa de orquestación que usa Redis para transportar mensajes y que permite observar y reintentar tareas. FastAPI encola y devuelve el ID; el worker ejecuta.

Configuración exacta mostrada:

```python
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

@celery_app.task
def process_report(user_id: int):
    return f"Reporte para el usuario {user_id} generado"
```

Para la demo mínima, la tarea `add_numbers(a, b)` devuelve `a + b`. El endpoint usa `.delay()` y recibe un `task_id` inmediatamente. Después consulta el resultado mediante `AsyncResult`; los estados del material son `PENDING`, `STARTED`, `SUCCESS`, `FAILURE` y `RETRY`.

Comando del worker indicado por el proyecto:

```bash
celery -A services.celery_app worker
```

La API debe responder antes de que termine la tarea. Preguntar: «¿Cuándo responde `generate_report.delay(user_id=42)`?». Respuesta: inmediatamente después de enviar la tarea a Redis.

### 58-70 min: observabilidad y patrones de producción

Instalar y levantar Flower:

```bash
pip install flower
celery -A celery_app flower
```

Abrir `http://localhost:5555`. Mostrar tareas activas, reservadas, historial, workers y profundidad de cola.

**Qué decir (literal)**

> Un reintento no debe golpear inmediatamente un servicio que acaba de fallar. `autoretry_for` selecciona las excepciones, `max_retries` limita intentos y `retry_backoff=True` activa retroceso exponencial con jitter.

Ejemplo del material:

```python
@celery_app.task(
    autoretry_for=(requests.Timeout, ConnectionError),
    max_retries=3,
    retry_backoff=True,
)
def call_external_api(url: str):
    pass
```

Para priorizar, se usan colas nombradas. Para encadenar, el material define `step_one(value)` que multiplica por 2 y `step_two(value)` que suma 10; ambas usan la cola `pipeline`, reintentan ante `ValueError` y pueden formar `step_one | step_two`.

### 70-75 min: proyecto DEV-55

**Qué decir (literal)**

> El ticket pide desacoplar una operación pesada de la API. La API es productor, Redis broker, Celery worker consumidor y el cliente consulta el resultado mediante `task_id`.

Checklist del proyecto:

- Redis en Docker, puerto `6379`, política `noeviction`; Flower en `5555`.
- API y workers comparten `REDIS_URL`.
- Una operación lenta se convierte en tarea Celery.
- El endpoint devuelve `202 Accepted` y `{"task_id": "..."}` sin esperar.
- `GET /tasks/{task_id}` devuelve estado `pending`, `started`, `success` o `failure` y resultado disponible.
- Tras hasta tres fallos, registrar en DLQ `task_id`, intento, error y timestamp.
- Worker separado de FastAPI.
- Logs con ID, intento, estado, duración y error completo.
- Mensajes con identificadores o referencias, nunca blobs voluminosos.

Mini plan de entrega:

```text
añadir Redis y Flower al docker-compose
leer REDIS_URL desde entorno
crear services/celery_app.py
identificar el endpoint más lento
encapsularlo en @app.task
encolar desde FastAPI y devolver 202 con task_id
crear GET /tasks/{task_id}
configurar max_retries=3 y backoff
registrar fallos agotados en DLQ
levantar worker separado y Flower
probar éxito, fallo, reintento y DLQ
documentar comandos y abrir PR con etiqueta async-tasks
```

## Cierre y preguntas

1. ¿Por qué `BLPOP` es más seguro que `GET` seguido de comprobación?
2. ¿Qué diferencia hay entre broker y backend de resultados?
3. ¿Por qué el endpoint devuelve un ID y no el informe?
4. ¿Qué significa `SUCCESS` frente a `FAILURE`?
5. ¿Qué resuelve `retry_backoff=True`?
6. ¿Qué debe contener la DLQ tras tres fallos?
7. ¿Por qué el worker debe ser un proceso independiente?

Respuestas esperadas: extracción y eliminación atómicas; transporte frente a estado/resultado; evita bloquear la respuesta; éxito frente a excepción; separa reintentos y reduce sobrecarga; ID, intento, error y timestamp; permite que API y procesamiento fallen o escalen de forma separada.

## Comandos y prompts

Los JSON y el README contienen los comandos Docker, `pip install`, Celery y Flower incluidos arriba. No contienen prompts de OpenClaw ni un guion de prompt para el proyecto; por trazabilidad no se inventa ninguno.

## Checklist del profesor

- [ ] Redis responde `PONG`.
- [ ] Se mostró `RPUSH`/`BLPOP` y el timeout finito.
- [ ] Se distinguieron lista y Streams.
- [ ] Se separaron broker y backend.
- [ ] Se ejecutó un worker fuera de FastAPI.
- [ ] Se explicó `202`, `task_id` y consulta de estado.
- [ ] Se abrió Flower y se revisaron estados.
- [ ] Se cubrieron reintentos, backoff, DLQ y mensajes ligeros.
