# Clase 47: De Datos Brutos a Informes — Transformación, Agregación y Reporte Técnico

## Hilo con las clases anteriores

Esta clase cierra el ciclo de telemetría que empezó en la clase 43, continuó con la captura en frontend (clase 45) y el almacenamiento (clase 46). Ahora pasamos de guardar datos a transformarlos en información útil.

### Lo que viene de la clase 43

En la clase 43 se establecieron los fundamentos de telemetría: qué observar, cómo definir eventos con el patrón de event envelope, y cómo decidir entre procesamiento por flujo o por lotes.

### Lo que viene de la clase 45

En la clase 45 se implementó la captura desde el frontend con un `TelemetryService` que envía lotes de eventos al backend con batching, debounce y reintentos.

### Lo que viene de la clase 46

En la clase 46 se creó la tabla `telemetry_events` en Supabase y el endpoint real que valida eventos con Pydantic y los persiste con bulk insert. Los datos ya están fluyendo y almacenándose.

### Qué añade esta clase

```text
class_43: decidir qué observar y cómo transportar los eventos (diseño)
    ↓
class_45: capturar, proteger y enviar eventos desde el frontend (captura)
    ↓
class_46: validar y guardar eventos en telemetry_events (almacenamiento)
    ↓
class_47: transformar datos almacenados en reportes técnicos (análisis)
    ↓
proyecto: pipeline de análisis + endpoint GET /telemetry/report (entrega)
```

**Frase de enlace para decir en clase**

> En la clase 43 definimos qué observar, en la 45 capturamos esos eventos desde el frontend, en la 46 los almacenamos en Supabase. Ahora los datos ya están ahí. El problema ha cambiado: ya no es "cómo guardo esto", sino "cómo convierto estas filas en información que le sirva al equipo de ingeniería". Eso es exactamente lo que vamos a hacer hoy.

---

## Nota de alcance

Esta guía se basa exclusivamente en los dos tutoriales de LearnPack enlazados desde esta carpeta y en el README del proyecto:

- `transforming_data.json` (11 lecciones): el pipeline de 5 pasos para transformar datos — Cargar (Load), Filtrar/Refinar (Filter/Refine), Convertir tipos (Convert Types), Agrupar y Agregar (Group & Aggregate), Servir (Output). Incluye la brecha entre datos transaccionales y analíticos, el ejemplo completo del informe semanal de completados, el desafío de codificación y la evaluación basada en escenarios.
- `metrics_aggregation_grouping.json` (8 lecciones): la fórmula universal `MÉTRICA = AGREGACIÓN(columna) GROUP BY DIMENSIÓN`. Desglosa `.count()`, `.sum()`, `.mean()`, agrupación temporal (día, hora, weekday), agrupación por categorías (event_type, level, tags), filtrado (dónde va cada filtro), métricas compuestas (tasa de error, ratio, percentiles) y el endpoint FastAPI con cache.
- `ai-eng-telemetry-report_project_README.es.md` — README del proyecto final del módulo.

**Limitación de las fuentes:** Ambos tutoriales son autocontenidos y no tienen problemas de duplicación severa como los vistos en clases anteriores. Las 11 lecciones de transforming_data y las 8 de metrics_aggregation_grouping cubren contenido distinto y complementario. No se requiere scraper adicional.

---

## Por qué y para qué de esta lección

### Idea principal para el profesor

Esta lección enseña a pasar de datos almacenados en una tabla a informes procesables mediante un pipeline de transformación. El núcleo es un modelo mental de 5 pasos que se repite en cualquier contexto: cargar, refinar, convertir tipos, agrupar+agregar, y servir.

La secuencia tiene este sentido:

1. Primero se entiende la **brecha** entre datos transaccionales (CRUD) y analíticos.
2. Después se recorre el **pipeline de 5 pasos** con un ejemplo concreto (tabla `todo_completions`).
3. Luego se profundiza en la **fórmula universal** métrica = agregación(columna) group by dimensión.
4. Se exploran **agregaciones**, **agrupaciones temporales** y **métricas compuestas**.
5. Finalmente se aplica todo al **proyecto**: construir un endpoint `GET /telemetry/report` con cache.

### Por qué importa

Los datos en `telemetry_events` responden "¿qué pasó?". Las preguntas operacionales son distintas: "¿cuántos eventos de error hubo por día esta semana?" o "¿qué tipo de evento es más frecuente?". Responderlas requiere transformación — siempre en el mismo orden.

Si no se domina este pipeline, cada reporte se construye desde cero, sin estructura reproducible, y los errores (especialmente el de agrupar timestamps sin convertirlos a datetime) pasan desapercibidos porque no lanzan ninguna excepción.

### Para qué se puede utilizar

- Pipeline de 5 pasos: cargar (SQL), refinar (Pandas), convertir tipos, agrupar y agregar, servir (JSON).
- Fórmula `MÉTRICA = AGREGACIÓN(columna) GROUP BY DIMENSIÓN`: aplicable a Pandas, SQL, Excel, Tableau.
- `.count()`, `.sum()`, `.mean()`: las tres agregaciones fundamentales que cubren la mayoría de los casos.
- Agrupación temporal: día, hora, weekday, semana, mes.
- Extracción de tags (JSONB) y agrupación por dimensiones dentro de ellos.
- Métricas compuestas: tasa de error, ratio, percentiles.
- Cache en memoria con TTL: evitar recalcular en cada request.
- El proyecto: construir `analysis.py` con 3 funciones de métrica + endpoint `GET /teclemetry/report`.

### Ejemplos de vida real que puedes usar al explicarla

| Concepto | Ejemplo de vida real | Pregunta para conectar con la clase |
|---|---|---|
| Brecha transaccional vs analítica | Tabla todo_completions: los datos están pero no en el formato que responde "completions por día" | ¿Cómo transformar filas individuales en un conteo por fecha? |
| Cargar (SQL) con filtros | Traer solo eventos de la última semana en lugar de toda la tabla | ¿Qué pasa si cargamos 10 millones de filas en memoria? |
| Convertir timestamp | Timestamp como string vs como datetime | ¿Qué pasa si agrupas por fecha sin convertir antes? |
| groupby + agg | ¿Cuántos eventos de cada tipo por día? | ¿Qué combinación de agrupación y agregación responde la pregunta? |
| Extraer tags | Obtener 'endpoint' de un JSONB | ¿Cómo accedes a un campo dentro de un dict en Pandas? |
| Métrica compuesta | Tasa de error = errores / total | ¿Cómo combinas dos agregaciones en una sola métrica? |
| Cache | Reporte semanal que no cambia cada segundo | ¿Debe cada request recalcular el reporte? |

Una forma sencilla de presentar la utilidad general es:

> Los datos almacenados no son la respuesta — son la materia prima. Aprender este pipeline es lo que te permite convertir cualquier tabla en un informe que alguien pueda leer y usar para tomar decisiones.

---

## Objetivos de aprendizaje

Al terminar, el grupo podrá:

- Explicar la diferencia entre datos transaccionales (CRUD) y analíticos, y por qué una tabla optimizada para escritura no responde preguntas analíticas directamente.
- Aplicar el pipeline de 5 pasos: cargar con filtros en SQL, refinar en Pandas, convertir timestamps a datetime, agrupar con `groupby` + `agg`, y servir con `to_dict(orient='records')`.
- Escribir la fórmula universal `MÉTRICA = AGREGACIÓN(columna) GROUP BY DIMENSIÓN` y aplicarla a preguntas concretas (eventos por día, valor promedio por tipo, tasa de error diaria).
- Usar `.count()`, `.sum()`, `.mean()` correctamente, entendiendo cuándo cada una es apropiada.
- Extraer campos de `tags` (JSONB) con `.apply(lambda t: t.get('campo'))` y agrupar por ellos.
- Construir métricas compuestas (tasa de error, ratio) combinando agregaciones básicas.
- Implementar cache simple en memoria con TTL para evitar recalcular el reporte en cada request.
- Aplicar todo lo anterior al proyecto `ai-eng-telemetry-report`: crear `analysis.py` con 3 funciones de métrica + endpoint `GET /teclemetry/report`.

---

## Preparación del profesor

### Recursos en esta carpeta

- `transforming_data.json` — Contenido extraído del tutorial de transformación (11 lecciones).
- `metrics_aggregation_grouping.json` — Contenido extraído del tutorial de métricas (8 lecciones).
- `ai-eng-telemetry-report_project_README.es.md` — README del proyecto en español.
- `ai-eng-telemetry-report_project_README.md` — README del proyecto en inglés.
- `ai-eng-telemetry-report_project_asset.json` — Asset del proyecto desde BreatheCode API.

### Lo que necesitas tener abierto

- Este resumen como material principal de la clase.
- El README del proyecto (`ai-eng-telemetry-report_project_README.es.md`) para el bloque final.
- Un editor para mostrar los snippets de Pandas (todos incluidos aquí).
- Opcional: `transforming_data.json` y `metrics_aggregation_grouping.json` para consultar lecciones específicas.

### No se requiere

- Ningún servidor corriendo durante la explicación.
- Conexión a Supabase durante la teoría (pero sí para el proyecto).
- Los HTML de los tutoriales (su contenido está íntegramente en los JSON y en este resumen).

---

## Agenda de 75 minutos

| Tiempo | Bloque | Contenido |
|--------|--------|-----------|
| 0-5 min | **Apertura** | Contexto: cerramos el ciclo de telemetría. Ya tenemos datos almacenados. Hoy aprendemos a transformarlos en reportes. |
| 5-12 min | **La brecha transaccional vs analítica** | Por qué los datos en CRUD no responden preguntas analíticas. Ejemplo de tabla todo_completions. |
| 12-25 min | **Pipeline de 5 pasos** | Cargar (SQL) → Refinar (Pandas) → Convertir tipos → Agrupar + Agregar → Servir. Código paso a paso. |
| 25-30 min | **La fórmula universal** | MÉTRICA = AGREGACIÓN(columna) GROUP BY DIMENSIÓN. Tabla de ejemplos. |
| 30-40 min | **Agregaciones y agrupaciones** | .count(), .sum(), .mean(). Agrupación temporal (día, hora, weekday). Agrupación por categorías y extracción de tags. |
| 40-48 min | **Métricas compuestas y filtrado** | Tasa de error, ratio. Dónde va cada filtro (SQL vs Pandas). |
| 48-55 min | **Cache y estructura de respuesta** | Cache simple en memoria (TTL 60s). Estructura JSON con metadatos. Endpoint FastAPI completo. |
| 55-65 min | **Bloque de proyecto** | Presentar el proyecto `ai-eng-telemetry-report`. Repasar el README y las fases. |
| 65-75 min | **Práctica y cierre** | Desafío de codificación (pipeline con dataset simulado), resumen del ciclo completo, preparación para el hito de Data Pipelines. |

---

## Desarrollo para el profesor

### 1. La brecha entre datos transaccionales y analíticos (7 minutos)

**Qué decir (literal)**

> Una base de datos optimizada para CRUD no está optimizada para responder preguntas analíticas. Para obtener respuestas necesitas transformar los datos: cargar, filtrar, agrupar, agregar y producir una salida.

Mostrar la tabla `todo_completions` como ejemplo:

| id | task_id | completed_at | user_id |
|----|---------|-------------|---------|
| 1 | 101 | 2024-01-01 10:00 | 5 |
| 2 | 102 | 2024-01-01 14:00 | 5 |
| 3 | 103 | 2024-01-02 09:00 | 5 |

**Pregunta:** "¿Cuántas tareas completó el usuario 5 por día?"

- Los datos están ahí, pero no en el formato que responde la pregunta
- Necesitas filtrar por `user_id`, agrupar por fecha y contar

**Explicar estos conceptos:**

| Tipo | Características | Ejemplos |
|------|----------------|----------|
| Transaccional (CRUD) | Optimizado para escrituras rápidas, normalizado, inserts/updates/deletes | tabla `users`, `orders`, `inventory` |
| Analítico | Optimizado para lecturas y agregaciones, desnormalizado | informes semanales, dashboards, métricas |

**Pregunta de transición**

> Si los datos no están en el formato que necesito, ¿qué tengo que hacer con ellos?

**Respuesta esperada**: Tengo que transformarlos: seleccionar las filas que me interesan, organizarlas por la dimensión que importa, y calcular el resumen.

### 2. Pipeline de 5 pasos (13 minutos)

**Qué decir (literal)**

> El pipeline sigue siempre el mismo orden. No importa si usas Pandas, SQL o Excel — el orden es cargar, refinar, convertir tipos, agrupar+agregar, y servir.

#### Paso 1: Cargar (Load)

El primer paso es obtener los datos desde donde están almacenados. En nuestro caso, desde Supabase/PostgreSQL usando SQL.

**Regla de oro:** Solo carga las filas que la métrica necesita. Nunca cargues toda la tabla en memoria.

**Lo que NO hacer:**
```python
# MAL: cargar todo y filtrar en Python
df = pd.read_sql("SELECT * FROM telemetry_events", conn)
df = df[df['event_type'] == 'page_view']
```

**Lo que SÍ hacer:**
```python
# BIEN: filtrar en SQL
df = pd.read_sql("""
    SELECT * FROM telemetry_events 
    WHERE event_type = 'page_view'
    AND timestamp >= :start
    AND timestamp < :end
""", conn, params={"start": start_date, "end": end_date})
```

**Explicar:** Cuando filtras en SQL, la base de datos solo transfiere las filas necesarias. Si tienes 10 millones de filas y solo necesitas las de la última semana, cargar todo en Python significa 10 millones de filas en memoria — la mayoría innecesarias. Filtrar en SQL las descarta antes de que lleguen a Pandas.

**Buenas prácticas:**
- Usa parámetros `:start` y `:end` para rangos de fechas
- Filtra por `event_type` en SQL cuando sea posible
- No hagas `SELECT *` si solo necesitas 3 columnas

#### Paso 2: Refinar (Filter/Refine)

Una vez cargados los datos, es momento de refinarlos en Pandas:

- Extraemos campos del JSON de `tags`
- Descartamos filas con dimensiones nulas
- Aplicamos filtros adicionales que no se pudieron hacer en SQL

**Dónde va cada filtro:**

| Criterio | Capa | Cómo |
|----------|------|------|
| Rango de timestamp | SQL | `WHERE timestamp >= :start AND timestamp < :end` |
| event_type | SQL | `WHERE event_type = '...'` |
| Dimensiones dentro de tags | Pandas | Extraer de tags, descartar nulos, groupby |
| Flags derivados | Pandas | Construir columnas como `is_error` |
| Predicados opcionales sobre tags | Pandas | Filtrar DataFrame después de extraer |

**Ejemplo en Pandas:**
```python
# Extraer campo 'endpoint' de tags
df['endpoint'] = df['tags'].apply(lambda t: t.get('endpoint'))

# Descartar filas sin endpoint
df = df.dropna(subset=['endpoint'])

# Crear flag de error
df['is_error'] = df['level'] == 'error'
```

#### Paso 3: Convertir tipos (Convert Types) — EL MÁS CRÍTICO

**Qué decir (literal, con énfasis)**

> Este es el paso que más se olvida y el que más bugs silenciosos produce. Los timestamps llegan como strings desde la base de datos. Si haces `groupby()` sobre strings que parecen fechas, obtienes grupos incorrectos sin ningún error visible. No hay excepción. No hay warning. Solo datos mal agrupados.

**La conversión obligatoria:**
```python
df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
df['date'] = df['timestamp'].dt.date
```

**Mostrar el error clásico:**
- `'2024-01-01'` como string se agrupa correctamente (todos los eventos del mismo día tienen el mismo string)
- `'2024-01-01T10:00:00'` como string NO se agrupa por día porque cada timestamp es único
- La conversión a datetime permite usar `.dt.date`, `.dt.hour`, `.dt.weekday()`

**Otros tipos a considerar:**
```python
df['value'] = pd.to_numeric(df['value'], errors='coerce')
```

**Preguntar**

> ¿Qué pasa si agrupas por fecha sin convertir el timestamp a datetime antes?

**Respuesta esperada**: Cada timestamp único se trata como un grupo diferente, y obtienes cientos de grupos de 1 fila en lugar de grupos por día.

#### Paso 4 y 5: Agrupar (Group) y Agregar (Aggregate)

**La fórmula mental:**
```
MÉTRICA = AGREGACIÓN(columna) agrupada por DIMENSIÓN
```

**En Pandas:**
```python
# Agrupar por fecha y contar
df_grouped = df.groupby('date').size().reset_index(name='count')

# Múltiples agregaciones
df_grouped = df.groupby('date').agg(
    count=('id', 'count'),
    total_value=('value', 'sum'),
    avg_value=('value', 'mean')
).reset_index()
```

#### Paso 6: Servir (Output)

```python
resultado = df_grouped.reset_index().to_dict(orient='records')
# Output: [{'date': '2024-01-01', 'count': 150}, ...]
```

**Buenas prácticas:**
- Usa `orient='records'` para obtener una lista de dicts
- Convierte tipos no serializables (ej. `numpy.int64` → `int`)
- Estructura la respuesta con metadatos útiles

#### Ejemplo completo: Informe semanal de completados

```python
import pandas as pd
from sqlalchemy import create_engine

def weekly_completion_report(conn, start_date, end_date):
    # 1. Cargar (Load)
    query = """
        SELECT task_id, user_id, completed_at
        FROM todo_completions
        WHERE completed_at >= :start AND completed_at < :end
    """
    df = pd.read_sql(query, conn, params={
        "start": start_date, "end": end_date
    })
    
    # 2. Convertir tipos
    df['completed_at'] = pd.to_datetime(df['completed_at'])
    df['date'] = df['completed_at'].dt.date
    
    # 3. Agrupar y Agregar (COUNT(*) GROUP BY date)
    report = df.groupby('date').size().reset_index(name='completions')
    
    # 4. Servir
    return report.reset_index().to_dict(orient='records')
```

**Aplicación a telemetría:**
```python
def events_per_day(conn, start_date, end_date):
    df = pd.read_sql("""
        SELECT event_type, timestamp FROM telemetry_events
        WHERE timestamp >= :start AND timestamp < :end
    """, conn, params={"start": start_date, "end": end_date})
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df['date'] = df['timestamp'].dt.date
    return df.groupby('date').size().reset_index(name='count') \
        .to_dict(orient='records')
```

**Preguntar**

> ¿Qué columnas de telemetry_events necesitarías para calcular "errores por tipo de evento por día"?

**Respuesta esperada**: `timestamp` (para la fecha), `event_type` (para el tipo), `level` (para identificar errores). El filtro `level='error'` puede ir en SQL o en Pandas como flag.

### 3. La fórmula universal: MÉTRICA = AGREGACIÓN(columna) GROUP BY DIMENSIÓN (5 minutos)

**Qué decir (literal)**

> Esta fórmula es la misma detrás de cualquier reporte, dashboard o análisis de datos. Ya sea que uses Pandas, SQL, Excel o Tableau, el concepto es siempre el mismo.

**Componentes:**
- **Métrica**: El valor que quieres medir (ej. "completions por día")
- **Agregación**: La función que resume datos (count, sum, mean)
- **Columna**: Sobre qué datos aplicas la agregación
- **Dimensión**: El eje o categoría por la que agrupas (tiempo, usuario, tipo)

**Tabla de ejemplos:**
| Pregunta | Métrica = | Agregación(columna) | Dimensión |
|----------|-----------|---------------------|-----------|
| ¿Cuántos eventos por día? | event_count = | COUNT(*) | by date |
| ¿Valor total por tipo? | total_value = | SUM(value) | by event_type |
| ¿Promedio por usuario? | avg_per_user = | AVG(value) | by user_id |
| ¿Tasa de error diaria? | error_rate = | COUNT(*) WHERE level='error' / COUNT(*) | by date |

**Preguntar**

> ¿Cuál sería la fórmula para "valor promedio de eventos por tipo"?

**Respuesta esperada**: `avg_value = AVG(value) GROUP BY event_type`, que en Pandas es `df.groupby('event_type')['value'].mean()`.

### 4. Agregaciones y agrupaciones (10 minutos)

**Qué decir (literal)**

> Ahora vamos a detallar cada función de agregación y los distintos tipos de agrupación que podemos hacer.

#### Las tres funciones fundamentales

**`.count()` — Contar ocurrencias**
```python
# ¿Cuántos eventos hay en total?
total = df['id'].count()

# ¿Cuántos eventos por tipo?
counts = df.groupby('event_type').size()
```

**`.sum()` — Sumar valores**
```python
# ¿Cuál es el valor total de eventos?
total_value = df['value'].sum()

# Valor total por tipo de evento
sums = df.groupby('event_type')['value'].sum()
```

**`.mean()` — Promedio**
```python
# ¿Cuál es el valor promedio?
avg_value = df['value'].mean()

# Promedio por tipo de evento
means = df.groupby('event_type')['value'].mean()
```

**Tabla comparativa:**
| Función | Qué hace | Cuándo usarla |
|---------|----------|---------------|
| `.count()` | Cuenta filas no nulas | Frecuencia, volumen |
| `.sum()` | Suma valores numéricos | Total acumulado |
| `.mean()` | Promedio de valores | Valor típico, rendimiento promedio |

**Nota importante:** Si el grupo no tiene filas, `.count()` devuelve 0, `.sum()` devuelve 0, `.mean()` devuelve NaN. Considera usar `.fillna(0)` después de `.mean()` si necesitas enteros.

#### Agrupación temporal

El tiempo es la dimensión más común en análisis de telemetría.

```python
# Convertir timestamp primero
df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)

# Diferentes niveles de granularidad
df['date'] = df['timestamp'].dt.date         # 2024-01-01
df['hour'] = df['timestamp'].dt.hour         # 0-23
df['weekday'] = df['timestamp'].dt.dayofweek  # 0=lunes, 6=domingo
df['week'] = df['timestamp'].dt.isocalendar().week  # número de semana
df['month'] = df['timestamp'].dt.month        # 1-12
df['year'] = df['timestamp'].dt.year          # 2024
```

**Agrupación por hora:**
```python
hourly = df.groupby('hour').size().reset_index(name='count')
print(hourly)
#    hour  count
# 0     0    120
# 1     0     95
# 2     0     70
```

**Agrupación por día de semana:**
```python
df['weekday'] = df['timestamp'].dt.day_name()
weekday_counts = df.groupby('weekday').size().reset_index(name='count')
```

**Buenas prácticas:**
- Siempre convierte a datetime ANTES de agrupar
- Elige la granularidad que responda la pregunta (día vs hora vs minuto)
- Para rangos largos, considera agrupar por semana o mes
- Usa fechas en UTC para consistencia

#### Agrupación por categorías

**Por tipo de evento (event_type):**
```python
by_type = df.groupby('event_type').size().reset_index(name='count')
```

**Por nivel de severidad (level):**
```python
by_level = df.groupby('level').size().reset_index(name='count')
#   level  count
# 0  info    700
# 1  warn    200
# 2  error   100
```

**Por dimensiones dentro de tags (JSONB):**
```python
# Extraer campo 'endpoint' de tags
df['endpoint'] = df['tags'].apply(lambda t: t.get('endpoint'))

# Agrupar por endpoint
by_endpoint = df.groupby('endpoint').size().reset_index(name='count')

# Combinar dimensiones: evento + endpoint
df['event_endpoint'] = df['event_type'] + ':' + df['endpoint']
by_combined = df.groupby('event_endpoint').size().reset_index(name='count')
```

**Agrupación múltiple (multi-index):**
```python
# Dos dimensiones: event_type y level
multi = df.groupby(['event_type', 'level']).size().reset_index(name='count')
#   event_type level  count
# 0  api_call  error     30
# 1  api_call  info     300
# 2  page_view info     400
```

**Consejos:**
- Descarta filas con dimensiones nulas antes de agrupar
- Para tags, extrae el campo primero, luego groupby
- Las agrupaciones múltiples dan más contexto que las simples

### 5. Métricas compuestas y filtrado (8 minutos)

**Qué decir (literal)**

> Las métricas más valiosas suelen ser combinaciones de agregaciones básicas. No nos quedamos en count, sum y mean — las combinamos para crear tasas y ratios.

#### Tasa de error
```python
# errores / total
# Primero: calcular total y errores por día
daily = df.groupby('date').agg(
    total=('id', 'count'),
    errors=('is_error', 'sum')
).reset_index()
daily['error_rate'] = daily['errors'] / daily['total']
```

**Implementación completa:**
```python
def error_rate_by_day(conn, start, end):
    # SQL: cargar eventos del período
    df = pd.read_sql("""
        SELECT level, event_type, timestamp 
        FROM telemetry_events
        WHERE timestamp >= :start AND timestamp < :end
    """, conn, params={"start": start, "end": end})
    
    # Pandas: convertir, crear flag y agrupar
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df['date'] = df['timestamp'].dt.date
    df['is_error'] = df['level'] == 'error'
    
    daily = df.groupby('date').agg(
        total=('id', 'count'),
        errors=('is_error', 'sum')
    ).reset_index()
    daily['error_rate'] = (daily['errors'] / daily['total']).round(4)
    
    return daily.to_dict(orient='records')
```

#### Otras métricas compuestas

**Percentiles:**
```python
p50 = df['value'].median()
p95 = df['value'].quantile(0.95)
p99 = df['value'].quantile(0.99)
```

**Ratio de conversión (ejemplo conceptual):**
```python
# completions / page_views
daily['conversion_rate'] = daily['completions'] / daily['page_views']
```

#### Dónde va cada filtro — Repaso

| Criterio | Capa | Razón |
|----------|------|-------|
| Rango de timestamp | SQL | Reduce drásticamente los datos transferidos |
| event_type | SQL | Filtro de alto volumen |
| Dimensiones en tags | Pandas | El JSONB se parsea mejor en Pandas |
| Flags derivados | Pandas | Se construyen después de la carga |
| Predicados opcionales | Pandas | Por defecto en Pandas |

**Nota:** Para la tasa de error necesitas todos los eventos (info, warn, error) porque el ratio usa el total como denominador. Por eso el filtro de fechas va en SQL pero la clasificación error/no-error va en Pandas.

### 6. Cache y estructura de respuesta (7 minutos)

**Qué decir (literal)**

> Calcular el reporte dentro del endpoint en cada request es ineficiente. Si los datos no cambian cada segundo, el pipeline va en una función separada y el resultado se cachea.

#### Cache simple en memoria
```python
_cache = {"data": None, "expires_at": None}

def get_cached_or_compute(start_date, end_date):
    now = datetime.now()
    if _cache["data"] and _cache["expires_at"] > now:
        return _cache["data"]
    
    result = compute_report(start_date, end_date)
    _cache["data"] = result
    _cache["expires_at"] = now + timedelta(seconds=60)
    return result
```

#### Estructura JSON de respuesta
```python
return {
    "period": {
        "from": start_date.isoformat(),
        "to": end_date.isoformat()
    },
    "metrics": {
        "events_per_day": df_grouped.to_dict(orient='records'),
        "error_rate_by_type": ...
    },
    "generated_at": datetime.now().isoformat()
}
```

#### Endpoint FastAPI completo
```python
from fastapi import FastAPI, Query
from datetime import date, timedelta

app = FastAPI()
_cache = {"data": None, "expires_at": None}

def compute_report(start_date, end_date):
    # ... pipeline completo con 3+ funciones de métrica ...
    pass

@app.get("/telemetry/report")
async def get_report(
    start: date = Query(default=None),
    end: date = Query(default=None)
):
    if start is None:
        end = date.today()
        start = end - timedelta(days=7)
    if end is None:
        end = date.today()
    
    now = datetime.now()
    if _cache["data"] and _cache["expires_at"] > now:
        return _cache["data"]
    
    result = compute_report(start, end)
    _cache["data"] = result
    _cache["expires_at"] = now + timedelta(seconds=60)
    return result
```

**Consideraciones:**
- Siempre valida que los tipos sean serializables (int, float, str, None)
- `numpy.int64` → `int`, `numpy.float64` → `float`
- Los datetime se convierten con `.isoformat()`

**Preguntar**

> Si el reporte semanal se consulta cada minuto pero los datos cambian cada hora, ¿debe cada request recalcular el pipeline?

**Respuesta esperada**: No. Con cache de 60 segundos, solo el primer request de cada minuto recalcula. Los siguientes usan el resultado cacheado.

### 7. Bloque de proyecto (10 minutos)

**Resumen del brief**

El proyecto `ai-eng-telemetry-report` es el último del módulo de Application Telemetry. Los datos ya están en `telemetry_events`. El objetivo es:

1. Crear `services/telemetry/analysis.py` con **3 funciones de métrica** independientes, cada una encapsulando una dimensión operacional distinta.
2. Crear el endpoint `GET /teclemetry/report` que sirva el resultado con cache.

**Reglas no negociables:**
- No calcular nada dentro del endpoint en cada request — el pipeline va aparte
- Convertir timestamps a `datetime` antes de cualquier agrupación
- Filtrar en SQL lo que se pueda filtrar en SQL
- El reporte es **técnico**, no de negocio — nada de tasas de conversión ni ingresos

**Métricas válidas (el README da estos ejemplos):**
1. Volumen de eventos por tipo y por día
2. Tasa de error por día o por tipo de evento
3. Latencia o tiempo de respuesta (si se capturó una métrica de rendimiento)

**Mini plan en pseudocódigo:**
```text
analysis.py:
    function events_per_day(conn, start, end):
        SQL: SELECT event_type, timestamp FROM telemetry_events
             WHERE timestamp >= :start AND timestamp < :end
        Pandas: convertir timestamp, extraer date
        groupby(['date', 'event_type']).size()
        return to_dict(orient='records')
    
    function error_rate(conn, start, end):
        SQL: SELECT level, timestamp FROM telemetry_events
             WHERE timestamp >= :start AND timestamp < :end
        Pandas: convertir timestamp, crear flag is_error
        groupby('date').agg(total=count, errors=sum(is_error))
        calcular error_rate = errors / total
        return to_dict(orient='records')

endpoint:
    GET /telemetry/report?start=...&end=...
        si no hay start/end → últimos 7 días
        check cache (TTL 60s)
        llamar a cada función de métrica
        devolver { period: {...}, metrics: {...} }
```

**Criterios de evaluación (del README):**
- [ ] `analysis.py` existe con al menos 3 funciones de métrica independientes
- [ ] Cada función sigue: cargar (SQL) → refinar (Pandas) → convertir tipos → agrupar → agregar
- [ ] Timestamps convertidos con `utc=True` antes de groupby temporal
- [ ] No se usan loops — solo operaciones de Pandas
- [ ] Cada función devuelve lista de dicts serializable a JSON
- [ ] Endpoint acepta `start_date`/`end_date` opcionales, default 7 días
- [ ] Endpoint devuelve `{ "period": {...}, "metrics": {...} }`
- [ ] Cache en memoria con TTL de 60 segundos
- [ ] Cada métrica responde una pregunta **técnica/operacional**

### 8. Práctica y cierre (10 minutos)

**Desafío de codificación**

Si queda tiempo, proponer este ejercicio con dataset simulado:

```python
import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000
data = {
    'timestamp': pd.date_range('2024-01-01', periods=n, freq='H'),
    'event_type': np.random.choice(
        ['page_view', 'button_click', 'api_call', 'error'], n
    ),
    'user_id': np.random.randint(1, 51, n),
    'value': np.random.uniform(0, 100, n).round(2),
    'level': np.random.choice(['info', 'warn', 'error'], n, p=[0.7, 0.2, 0.1])
}
df = pd.DataFrame(data)
df.to_csv('telemetry_sample.csv', index=False)
```

**Requisitos:**
1. Carga el CSV
2. Filtra solo eventos con `level='error'`
3. Convierte timestamp a datetime y extrae la fecha
4. Agrupa por fecha y cuenta errores por día
5. Devuelve el resultado como lista de dicts

**Solución:**
```python
def error_rate_per_day(csv_path):
    df = pd.read_csv(csv_path)
    df = df[df['level'] == 'error']
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    report = df.groupby('date').size().reset_index(name='error_count')
    return report.to_dict(orient='records')

print(error_rate_per_day('telemetry_sample.csv'))
```

**Preguntas de cierre del proyecto:**
- ¿Cuál es el paso más crítico del pipeline y por qué?
- ¿Dónde debe ir el filtro de `event_type`?
- ¿Por qué el reporte debe ser técnico y no de negocio?
- ¿Qué pasa si no usamos cache?
- ¿Cuál es la diferencia entre un reporte bajo demanda y uno precomputado?

**Cierre del ciclo completo:**
```text
Clase 43:  Diseño de telemetría        → ¿Qué observar? ¿Cómo describirlo?
Clase 45:  Captura frontend            → TelemetryService, batch, sendBeacon
Clase 46:  Almacenamiento              → Supabase, validación Pydantic, bulk insert
Clase 47:  Análisis y reporte técnico  → Pandas, pipeline 5 pasos, endpoint GET /telemetry/report
```

> El proyecto de esta clase es el último del módulo de Application Telemetry. Después de esto, el siguiente hito será Data Pipelines, donde las métricas técnicas se convierten en métricas de negocio con herramientas más especializadas.

---

## Recorte y extensión

### Versión de 60 minutos

- Brecha transaccional vs analítica: 5 minutos (solo la tabla ejemplo y la pregunta)
- Pipeline de 5 pasos: 10 minutos (mostrar solo los snippets clave, sin el ejemplo completo)
- Fórmula universal + agregaciones: 10 minutos (tabla de ejemplos + count/sum/mean, sin agrupación temporal detallada)
- Métricas compuestas: 5 minutos (solo tasa de error, sin percentiles)
- Cache y endpoint: 5 minutos (mostrar el código completo pero sin explicar cada línea)
- Proyecto: 15 minutos (presentar README y fases, omitir el desafío de codificación)
- Cierre: 10 minutos

### Versión de 90 minutos

- Incluir el desafío de codificación completo con dataset simulado
- Agregar un ejercicio de agrupación temporal con datos reales
- Mostrar ambos tutoriales JSON en detalle (lección por lección)
- Dedicar 20 minutos al proyecto: revisar cada criterio de evaluación y empezar a esbozar `analysis.py`

---

## Checklist de cierre

- [ ] Se explicó la brecha entre datos transaccionales y analíticos
- [ ] Se recorrió el pipeline de 5 pasos con código
- [ ] Se mostró la conversión obligatoria de timestamp y el error clásico
- [ ] Se practicó `groupby` + `agg` con count, sum, mean
- [ ] Se hizo agrupación temporal (día, hora) y por categorías (event_type, tags)
- [ ] Se construyó una métrica compuesta (tasa de error)
- [ ] Se explicó la decisión de dónde va cada filtro (SQL vs Pandas)
- [ ] Se implementó cache en memoria con TTL
- [ ] Se presentó el proyecto con sus fases y criterios de evaluación
- [ ] Se resolvió el desafío de codificación (o se dejó como tarea)