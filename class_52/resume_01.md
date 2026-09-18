# Clase 52: Diseño de colas y flujos asíncronos

## Hilo de continuidad

En la clase 51 identificamos trabajos que salen del ciclo solicitud-respuesta y vimos disparadores y cronjobs. Esta clase decide cuándo una tarea debe ir a segundo plano y qué estructura de cola representa mejor cada caso. La transición literal es: «Ya sabemos cuándo iniciar un trabajo; ahora vamos a decidir cómo esperar, ordenar y recuperar ese trabajo cuando los componentes avanzan a velocidades distintas».

Esta guía se basa exclusivamente en `tutorial.json`, `tutorial_2.json`, `triage-queue_project_README.es.md` y `branch-queue_project_README.es.md`. La agenda, las frases del profesor y las preguntas son organización docente añadida.

## Objetivos

- Explicar FIFO, `enqueue`, `dequeue` y el patrón productor-consumidor.
- Elegir entre cola simple, cola de prioridad y colas separadas por servicio.
- Aplicar la prueba de candidato asíncrono: duración, independencia de fallos e independencia del resultado.
- Diferenciar trabajo limitado por CPU y por I/O.
- Diseñar para duplicados, reintentos, jitter y estados persistentes.
- Traducir estos criterios a los proyectos `triage-queue` y `branch-queue`.

## Agenda de 60-75 minutos

| Tiempo | Bloque | Resultado |
| --- | --- | --- |
| 0-8 | Cola como sala de espera | FIFO y productor-consumidor |
| 8-18 | Tipos y usos | Selección de estructura |
| 18-30 | Candidato asíncrono y CPU/I/O | Decisión de diseño |
| 30-42 | Fallos, duplicados y jitter | Flujo resistente |
| 42-55 | Proyecto Triage Queue | Prioridad + FIFO |
| 55-67 | Proyecto Branch Queue | Cola independiente por servicio |
| 67-75 | Evaluación y cierre | Justificar decisiones |

Para 60 minutos, omitir la implementación oral de jitter y reducir cada proyecto a su modelo de datos. Para 75, pedir que el grupo compare una lista única con tres `deque` y escriba el flujo de estados.

## Preparación

- Tener abiertas esta guía y los dos READMEs de proyecto.
- Recordar que ambos proyectos exigen solo biblioteca estándar de Python.
- En `triage-queue`, usar `collections.deque`, `heapq` y `datetime` únicamente.
- En `branch-queue`, usar `collections.deque` y `datetime` únicamente.
- No añadir persistencia: ambos briefs indican que no se evalúa.

## Guion docente

### 0-8 min: FIFO y productor-consumidor

**Qué decir (literal)**

> Una cola es una estructura lineal FIFO: el primero que entra es el primero que sale. `enqueue` añade al final y `dequeue` retira del inicio. La cola funciona como una sala de espera: quien produce trabajo no tiene que esperar a quien lo consume, y el buffer absorbe picos cuando llegan tareas más rápido de lo que se procesan.

Flujo para dibujar:

```text
Productor -> Cola -> Consumidor
```

Una cola de mensajes añade durabilidad, reconocimiento y distribución. El productor y el consumidor pueden estar en procesos o servidores diferentes. La pregunta de chequeo es: «Si llegan 1.000 solicitudes por segundo y el trabajador procesa 100, ¿qué papel cumple la cola?». Respuesta: actúa como buffer y retiene el exceso hasta que los trabajadores puedan procesarlo.

### 8-18 min: elegir el tipo de cola

**Qué decir (literal)**

> FIFO es justo y predecible, pero no siempre representa la prioridad del negocio. Una cola de prioridad permite atender tareas urgentes antes que otras. Una cola circular sirve para secuencias repetidas, como reproducción. Una cola estática limita el tamaño; una dinámica crece según la necesidad.

| Caso | Estructura |
| --- | --- |
| Procesar en orden de llegada | Cola FIFO |
| Tareas críticas antes que tareas normales | Cola de prioridad |
| Canciones que vuelven al inicio | Cola circular |
| Capacidad fija | Cola estática |

Preguntar: «¿Qué cola necesita un sistema donde lo crítico siempre va primero?». Respuesta: cola de prioridad. «¿Quién produce un correo de confirmación después de un registro?». Respuesta: el servicio que crea la tarea de correo; el servicio de correo es el consumidor.

### 18-30 min: candidato asíncrono y CPU/I/O

**Qué decir (literal)**

> Una tarea es candidata a una cola cuando tarda lo suficiente para que el usuario no deba esperar, puede fallar y reintentarse de forma independiente, y su resultado no es necesario inmediatamente para continuar. El cliente recibe un ID de trabajo o una confirmación y consulta el estado más tarde.

Ejemplo de decisión: exportar un informe PDF que tarda 30 segundos debe devolver un ID y procesarse en segundo plano. En un pago, validar el carrito y cobrar son pasos cuyo resultado se necesita para continuar; enviar el correo de confirmación es independiente y puede reintentarse.

- CPU: redimensionamiento de imágenes, transcodificación, entrenamiento de modelos y hashing criptográfico. En Python, usar múltiples procesos para paralelismo real; el ejemplo del material usa ocho procesos en un servidor de ocho núcleos.
- I/O: llamadas de red, consultas de base de datos y lecturas de disco. El tiempo principal se pasa esperando recursos externos.

Pregunta: «¿Un PDF pesado que bloquea 30 segundos cumple las tres condiciones?». Respuesta: sí, si puede fallar de manera independiente y el cliente no necesita el resultado para seguir.

### 30-42 min: fallos, duplicados y jitter

**Qué decir (literal)**

> En un sistema asíncrono el fallo es un evento esperado. Si un worker cae después de empezar y el intermediario no recibe confirmación, la tarea puede volver a la cola. Sin una protección, dos workers podrían cobrar o enviar un correo dos veces.

Usar el patrón estado-antes-del-trabajo:

```text
verificar estado -> si pendiente, marcar procesando
                 -> realizar trabajo
                 -> marcar hecho
si está procesando o hecho, omitir
```

Los reintentos con retroceso exponencial reducen la sobrecarga de un servicio temporalmente caído. Si 500 workers fallan a la vez, aun con retrasos `1s, 2s, 4s, 8s` pueden reintentar sincronizados y crear una tormenta. El jitter añade aleatoriedad dentro de una ventana y distribuye los reintentos.

Pregunta: «¿Por qué no basta con reintentar todos cada dos segundos?». Respuesta: porque los reintentos sincronizados pueden sobrecargar el servicio que se está recuperando.

### 42-55 min: proyecto Triage Queue

**Qué decir (literal)**

> Este proyecto convierte la prioridad en una estructura comprobable. Cada paciente tiene nombre, nivel de triaje de 1 a 3 y momento de llegada. El nivel 1 siempre precede al 2 y el 2 al 3; dentro de un mismo nivel se conserva FIFO.

El proyecto exige `Patient` y `TriageQueue`, con `enqueue`, `dequeue`, `peek`, `list_queue` y `stats`. `dequeue()` y `peek()` sobre una cola vacía deben gestionarse con un error descriptivo sin romper el programa. El menú CLI permite añadir, llamar, listar, ver estadísticas y salir.

Mini plan:

```text
definir Patient(name, triage_level, arrived_at)
crear TriageQueue con estructura de prioridad y orden de llegada
enqueue: insertar respetando nivel y FIFO dentro del nivel
dequeue: retirar el siguiente o gestionar cola vacía
peek: consultar sin retirar
list_queue: devolver el orden de atención
stats: contar pacientes por nivel
crear menú CLI y rechazar entradas inválidas
documentar estructura y mutación concurrente
```

Prueba oral: encolar nivel 2, nivel 3 y después nivel 1. La lista debe empezar por nivel 1; dos pacientes del mismo nivel deben conservar su llegada. La nota de diseño debe explicar la elección frente a una `deque` única, una lista ordenada y tres colas separadas, además de indicar que la mutación que extrae o inserta debe evitar el doble procesamiento.

### 55-67 min: proyecto Branch Queue

**Qué decir (literal)**

> Aquí no hay una prioridad global: hay tres agentes independientes y cada uno atiende su servicio. La estructura correcta es una cola por servicio. Así `call_next("deposito")` no recorre tickets de retiros ni de gestión de cuenta.

El ticket contiene `number`, `client_name`, `service_type` e `issued_at`. Los servicios válidos son `deposito`, `retiro` y `gestion_cuenta`; el contador de tickets es global y empieza en 1. Implementar `issue_ticket`, `call_next`, `peek_next`, `list_waiting` y `stats`, además del menú CLI.

Mini plan:

```text
crear Ticket con número global y servicio
crear tres colas FIFO internas por servicio
issue_ticket: validar servicio, incrementar contador y encolar
call_next: retirar solo de la cola solicitada
peek_next: consultar sin retirar
list_waiting: agrupar por servicio
stats: contar cada servicio y total
gestionar cola vacía y servicio inválido
documentar por qué separar colas es más eficiente
```

Prueba oral: emitir tickets alternando servicios. Los números deben ser 1, 2, 3 globalmente, pero cada agente solo debe llamar a su propia cola. Preguntar qué debe mutar primero si dos agentes llaman simultáneamente: la extracción de la cola debe ser la operación que reserve el ticket antes de devolverlo, para que no sea llamado dos veces.

## Cierre y evaluación

Preguntar:

1. ¿Qué significa FIFO y qué hacen `enqueue` y `dequeue`?
2. ¿Qué tres condiciones forman la prueba de candidato asíncrono?
3. ¿Cuándo conviene una cola de prioridad?
4. ¿Qué diferencia hay entre CPU-bound e I/O-bound?
5. ¿Qué protege el patrón estado-antes-del-trabajo?
6. ¿Por qué el jitter evita tormentas de reintentos?
7. ¿Por qué `branch-queue` usa una cola por servicio?

Respuestas esperadas: primero en entrar/primero en salir; duración, independencia de fallos e independencia del resultado; urgencias antes que tareas normales; cálculo frente a espera externa; evita procesamiento duplicado; desincroniza reintentos; permite que cada agente opere directamente sobre su servicio.

## Comandos y prompts

Los READMEs indican crear los repositorios `triage-queue` y `branch-queue`, abrirlos en local o Codespace y crear `triage_queue.py` y `branch_queue.py`. No incluyen comandos de shell completos ni prompts de OpenClaw. Por trazabilidad no se añaden comandos o prompts inventados; el profesor puede usar el CLI del proyecto y la biblioteca estándar indicada.

## Checklist del profesor

- [ ] Se explicó FIFO antes de prioridad.
- [ ] Se clasificaron candidatos asíncronos y CPU/I/O.
- [ ] Se dibujó productor-cola-consumidor.
- [ ] Se explicó estado-antes-del-trabajo y jitter.
- [ ] Se cubrieron las cinco operaciones de ambos proyectos.
- [ ] Se comprobaron cola vacía, servicio inválido, prioridad y FIFO.
- [ ] El alumnado dejó una nota de diseño sobre concurrencia.
