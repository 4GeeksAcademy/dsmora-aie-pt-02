# Resumen de la clase 52 para impartir la clase 53

## Idea central

La clase 52 enseñó a pasar de una ejecución directa a un sistema donde un componente produce trabajo, una cola lo conserva temporalmente y otro componente lo consume:

```text
Productor -> Cola -> Consumidor
```

La clase 53 implementa ese modelo con Redis, workers, Celery y FastAPI.

## Lo imprescindible que debe recordar el profesor

### 1. FIFO y operaciones de una cola

Una cola FIFO respeta «primero en entrar, primero en salir».

- `enqueue`: añade una tarea al final.
- `dequeue`: retira la tarea del inicio.
- `peek`: consulta la siguiente tarea sin retirarla.

Este orden es la base de la cola de Redis que se verá en la clase 53.

### 2. Por qué usar una cola

Una cola es útil cuando:

- El productor genera trabajo más rápido que el consumidor.
- Queremos separar la creación de una tarea de su ejecución.
- Varios workers pueden procesar tareas de forma independiente.
- Necesitamos absorber picos de carga.
- No queremos bloquear la respuesta al usuario.

Frase de transición:

> En la clase 52 vimos que la cola funciona como una sala de espera. En la clase 53 Redis será esa sala de espera y los workers serán quienes llamen al siguiente trabajo.

### 3. Productor y consumidor

- **Productor:** crea y encola la tarea.
- **Cola o broker:** mantiene la tarea hasta que haya un consumidor disponible.
- **Consumidor o worker:** extrae y procesa la tarea.

La API de FastAPI actuará como productor. Redis actuará como broker. El worker de Celery será el consumidor.

### 4. Cola FIFO frente a cola de prioridad

La cola FIFO atiende por orden de llegada. Una cola de prioridad atiende primero las tareas urgentes, aunque hayan llegado después. Esta diferencia se trabajó con el proyecto `triage-queue`.

En la clase 53 se volverá al orden FIFO para explicar `RPUSH` y `BLPOP`. Después se mostrará que Celery permite dirigir tareas a colas nombradas cuando se necesita separar o priorizar trabajo.

### 5. Cuándo una tarea debe ser asíncrona

Una tarea es candidata a procesamiento asíncrono cuando cumple estas tres condiciones:

1. Tarda lo suficiente para que el usuario no deba esperar.
2. Puede fallar y reintentarse independientemente de la solicitud actual.
3. Su resultado no es necesario inmediatamente para continuar.

Ejemplo: generar un informe pesado. La API debe devolver un identificador de trabajo y permitir consultar el estado, en lugar de mantener abierta la solicitud hasta terminar.

### 6. CPU frente a I/O

- **CPU-bound:** la mayor parte del tiempo se dedica a cálculos, como transcodificación, redimensionamiento de imágenes o hashing.
- **I/O-bound:** la mayor parte del tiempo se espera una red, una base de datos o un disco.

Esta clasificación ayuda a decidir cómo ejecutar workers. En la clase 53 el foco estará en desacoplar y observar el trabajo, no en profundizar en la estrategia de paralelismo.

### 7. Diseñar para fallos

En sistemas asíncronos los fallos son esperables. Si un worker cae durante una tarea, el mensaje puede volver a procesarse. Sin protección, eso puede provocar cobros o correos duplicados.

El patrón estado-antes-del-trabajo es:

```text
verificar estado
si está pendiente: marcar procesando
realizar trabajo
marcar hecho
si está procesando o hecho: omitir
```

Esta idea conecta directamente con los ACK de Celery: el mensaje no debe considerarse completado antes de que el worker termine correctamente.

### 8. Reintentos y jitter

El retroceso exponencial separa los reintentos: por ejemplo, `1s`, `2s`, `4s`, `8s`. El jitter añade aleatoriedad para que muchos workers que fallaron a la vez no vuelvan a intentarlo exactamente en el mismo momento.

En la clase 53 se verá esta idea con:

- `autoretry_for` para seleccionar errores reintentables.
- `max_retries` para limitar los intentos.
- `retry_backoff=True` para activar el retroceso.

## Puente directo hacia la clase 53

Usar esta explicación literal:

> Hasta ahora hemos hablado de colas como una estructura y como un patrón de arquitectura. Ahora vamos a implementarlas. Redis guardará los mensajes, `RPUSH` los añadirá al final, `BLPOP` extraerá uno del principio y un worker lo procesará. Después añadiremos Celery para obtener ACK, estados, reintentos y monitorización.

## Preguntas rápidas antes de empezar

1. Si el productor es más rápido que el consumidor, ¿qué componente absorbe la diferencia? La cola.
2. ¿Qué patrón separa a quien crea trabajo de quien lo procesa? Productor-cola-consumidor.
3. ¿Qué debe recibir el cliente si el informe tarda mucho? Una confirmación o un ID de trabajo.
4. ¿Qué riesgo existe si un worker falla después de comenzar? Procesamiento duplicado o pérdida del mensaje.
5. ¿Qué evita el jitter? Reintentos sincronizados que sobrecarguen el servicio.
6. ¿Qué será Redis en la clase 53? El broker que conserva y entrega mensajes.

Con estas respuestas activadas, la clase puede comenzar directamente con Redis y el comando `BLPOP`.
