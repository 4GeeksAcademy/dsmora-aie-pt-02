# Clase 42: Caching — de fundamentos a FastAPI y Next.js

## Nota de alcance

Esta guía se redacta exclusivamente a partir de los tres JSON guardados en esta carpeta:

- `caching_faster_responses_without_extra_work.json` (11 lecciones): fundamentos generales de caching, arquitectura de capas, invalidación y las cuatro estrategias de caché, con un ejemplo Cache-Aside en Python.
- `caching_in_fastapi.json` (13 lecciones): caché en proceso con `lru_cache`, `FastAPICache` (TTL, namespaces, backends), invalidación con claves de consulta, ETags y escalado con Redis.
- `caching_in_next_js.json` (12 lecciones): la directiva `use cache` en tres niveles, construcción de claves de caché, perfiles `cacheLife` y etiquetas `cacheTag`/`revalidateTag`.

Algunas lecciones se repiten en contenido entre índices consecutivos (por ejemplo, el resumen de FastAPICache aparece en los índices 3 y 4, y varias conclusiones se repiten entre el penúltimo y el último índice de cada tutorial); para esta guía se usó la versión más completa de cada tema.

Además se incorporó el proyecto asociado `ai-eng-application-caching` (onepage no renderizable directamente, obtenido vía API de BreatheCode): `ai-eng-application-caching_project_asset.json` y `ai-eng-application-caching_project_README.es.md`.

## Objetivos de aprendizaje

Al terminar, el grupo podrá:

- Explicar el ciclo de acierto/fallo de caché y por qué el caching mejora velocidad, eficiencia y escalabilidad.
- Distinguir las tres capas de arquitectura de caché: en proceso, distribuida (Redis) y CDN/caché HTTP.
- Comparar invalidación por TTL frente a invalidación basada en eventos.
- Diferenciar las cuatro estrategias de caché (Cache-Aside, Write-Through, Write-Behind, TTL-Based) e implementar Cache-Aside con TTL en Python.
- Aplicar caching en FastAPI con `lru_cache`, `FastAPICache` (TTL, namespaces, `InMemoryBackend`/`RedisBackend`) y ETags para caché condicional HTTP.
- Aplicar la directiva `use cache` de Next.js en sus tres niveles, controlar la vida útil con `cacheLife` e invalidar bajo demanda con `cacheTag`/`revalidateTag`.

## Preparación del profesor

- Abrir los tres JSON de esta carpeta para tener los ejemplos a la vista.
- Tener un entorno Python listo para ejecutar el ejemplo Cache-Aside (no requiere dependencias externas).
- Tener a mano el comando `pip install fastapi-cache2` para mostrarlo, sin necesidad de instalarlo en vivo si no hay tiempo.
- Si se quiere mostrar Redis en vivo, verificar que haya un servidor Redis accesible en `redis://localhost:6379`; si no, quedarse en la lectura del código.
- Tener el editor abierto para mostrar snippets de FastAPI (Python) y Next.js (TypeScript/TSX).

## Agenda de 60 minutos

| Tiempo | Bloque |
|---|---|
| 0-6 min | Fundamentos: qué es caching y el ciclo acierto/fallo |
| 6-14 min | Arquitectura de capas e invalidación (TTL vs eventos) |
| 14-24 min | Las cuatro estrategias de caché + demo Cache-Aside en Python |
| 24-36 min | Caching en FastAPI: `lru_cache` y `FastAPICache` |
| 36-44 min | ETag y caché condicional en FastAPI |
| 44-56 min | Caching en Next.js: `use cache`, `cacheLife`, `cacheTag`/`revalidateTag` |
| 56-60 min | Cierre: caché en producción y próximos pasos |

Para una clase de 75 minutos, usar las extensiones indicadas en cada bloque (tabla comparativa de las cuatro estrategias, perfil personalizado de `cacheLife` y una pregunta grupal adicional de cierre).

## Desarrollo para el profesor

### 1. Fundamentos: qué es caching (6 minutos)

**Qué decir (literal)**

> Imaginen su API como una cafetería muy concurrida. Cada vez que un cliente pide el mismo café, el barista lo prepara desde cero. Eso toma tiempo y ralentiza la fila. El caching es preparar un lote con anticipación y servirlo al instante cuando se solicite: almacena los resultados de operaciones costosas —consultas a bases de datos o cálculos complejos— para no repetir el trabajo cuando se pidan los mismos datos otra vez.

Explicar el ciclo de acierto/fallo con la analogía del "caché de memoria como intermediario rápido": la app revisa el caché antes de ir a la fuente de datos; si encuentra el dato es un acierto de caché y responde al instante; si no lo encuentra es un fallo de caché, obtiene el dato de la fuente, lo guarda en el caché y lo devuelve.

Mencionar las tres razones del material para cachear: velocidad (respuesta casi instantánea), eficiencia (menos carga en la base de datos) y escalabilidad (la API soporta más solicitudes).

**Pregunta para el grupo**

> Si nuestra API consulta la misma fila de la base de datos cientos de veces por minuto, ¿qué le pasa a la base de datos si no cacheamos nada?

**Respuesta esperada**

Se sobrecarga con trabajo repetido e innecesario, lo que aumenta la latencia y el riesgo de saturación.

### 2. Arquitectura de capas e invalidación (8 minutos)

**Qué decir (literal)**

> El caching no es una solución única para todos: existe en varias capas, cada una con compromisos distintos de velocidad, alcance y persistencia.

Presentar las tres capas del material:

- **Caché en memoria dentro del proceso** (por ejemplo, un diccionario de Python): la más rápida, pero solo disponible para una instancia y se pierde al reiniciar.
- **Caché distribuida** (por ejemplo, Redis): algo más lenta por la latencia de red, mas se comparte entre instancias y sobrevive a reinicios.
- **CDN / caché HTTP**: capa global fuera de la aplicación, ideal para escalar respuestas públicas, con control limitado sobre la invalidación.

**Qué decir (literal)**

> Si su API corre en varios servidores detrás de un balanceador de carga y cada uno tiene su propio caché en memoria, no comparten datos entre sí: eso puede producir respuestas inconsistentes. Ahí es donde entra Redis como caché compartida.

Explicar los dos métodos de invalidación:

- **TTL (Tiempo de Vida)**: cada entrada expira tras un tiempo fijo; simple, pero puede servir datos obsoletos hasta la expiración.
- **Basada en eventos**: se elimina o actualiza la entrada de caché explícitamente cuando los datos originales cambian; garantiza consistencia, pero es más compleja de coordinar.

```python
# Invalidación basada en eventos en un endpoint FastAPI
@app.patch('/products/{product_id}')
def update_product(product_id: int, data: dict):
    db.update_product(product_id, data)
    cache_key = f'product:{product_id}'
    if cache_key in cache:
        del cache[cache_key]
    return {'status': 'updated'}
```

**Qué preguntar después**

> ¿Por qué muchos sistemas combinan TTL con invalidación basada en eventos en lugar de usar solo uno de los dos?

**Respuesta esperada**

La invalidación basada en eventos maneja con precisión la mayoría de las actualizaciones, y el TTL actúa como red de seguridad para entradas que no se invalidaron por un evento perdido.

### 3. Las cuatro estrategias de caché + demo Cache-Aside (10 minutos)

**Qué decir (literal)**

> Las estrategias de caché son las reglas que gobiernan cómo y cuándo se almacenan y actualizan los datos. Elegir la estrategia correcta depende de la carga de lectura/escritura de la aplicación y de cuánta consistencia se necesita.

Presentar las cuatro estrategias del material:

1. **Cache-Aside (carga perezosa)**: al leer, se verifica el caché; si falta, se carga desde la base de datos y se guarda. Al escribir, se actualiza la base de datos y se invalida o deja expirar el caché. Ideal para cargas con muchas lecturas.
2. **Write-Through**: cada escritura actualiza simultáneamente caché y base de datos; las lecturas siempre van al caché. Da fuerte consistencia, pero escrituras más lentas.
3. **Write-Behind**: las escrituras van primero al caché y un proceso en segundo plano sincroniza la base de datos de forma asíncrona. Escrituras muy rápidas, pero riesgo de pérdida de datos si el caché falla antes de sincronizar.
4. **Caché basada en TTL**: las entradas expiran automáticamente tras un tiempo fijo, sin invalidación explícita.

**Comandos exactos para la demo**

```bash
python3 - <<'EOF'
import time

cache = {}

def query_database(user_id: int) -> dict:
    return {"id": user_id, "name": f"Usuario {user_id}"}

def get_user(user_id: int) -> dict:
    now = time.time()
    if user_id in cache:
        value, expires_at = cache[user_id]
        if now < expires_at:
            print("ACIERTO DE CACHÉ")
            return value
        else:
            del cache[user_id]
    print("FALLO DE CACHÉ")
    result = query_database(user_id)
    cache[user_id] = (result, now + 5)
    return result

print(get_user(1))  # FALLO DE CACHÉ
print(get_user(1))  # ACIERTO DE CACHÉ
time.sleep(6)
print(get_user(1))  # FALLO DE CACHÉ (expiró)
print(get_user(2))  # FALLO DE CACHÉ (nuevo usuario)
EOF
```

**Qué decir (literal)**

> La primera llamada falla en caché porque está vacío; guardamos el resultado con expiración a 5 segundos. La segunda llamada dentro de esos 5 segundos acierta y responde al instante. Después de esperar 6 segundos, el TTL expiró y volvemos a fallar en caché.

**Prompt exacto para la demo con agente de IA**

```text
Implementa una función get_product(product_id) en Python que use la estrategia Cache-Aside con un TTL de 10 segundos, siguiendo el mismo patrón que get_user: un diccionario cache con (valor, timestamp de expiración), impresión de ACIERTO/FALLO DE CACHÉ, y una función simulada query_database. Incluye llamadas de prueba que demuestren un fallo, un acierto y una expiración.
```

**Extensión a 75 minutos: tabla comparativa**

| Estrategia | Lectura | Escritura | Consistencia | Ejemplo de uso |
|---|---|---|---|---|
| Cache-Aside | Verifica caché, carga en fallo | Escribe en BD, invalida caché | Eventual | Catálogo de productos |
| Write-Through | Siempre lee caché | Escribe en caché y BD sincronizadas | Fuerte | Perfiles de usuario |
| Write-Behind | Lee caché | Escribe en caché, sincroniza BD asíncronamente | Eventual, riesgo de pérdida | Registro de alta velocidad |
| TTL-Based | Lee caché, expira por TTL | Solo escribe en BD | Eventual | Instantáneas de noticias |

### 4. Caching en FastAPI: `lru_cache` y `FastAPICache` (12 minutos)

**Qué decir (literal)**

> El caché en proceso vive dentro de la memoria del proceso Python: sin llamadas de red, sin lecturas de disco, solo memoria rápida. Es ideal cuando los datos cambian poco y la aplicación corre como un solo proceso. Su limitación principal es el alcance: si corren varios workers (por ejemplo, Gunicorn con 4 workers), cada uno tiene su propio caché aislado.

```python
from functools import lru_cache

@lru_cache(maxsize=128)  # Caché hasta 128 llamadas únicas
def get_exchange_rates():
    import time
    time.sleep(2)  # Simula una llamada lenta a la API
    return {"USD": 1.0, "EUR": 0.92, "GBP": 0.79}
```

**Qué decir (literal)**

> `lru_cache` es excelente para memorizar funciones simples, pero no tiene TTL, no conoce el contexto HTTP y no soporta caché distribuido. Ahí es donde entra FastAPICache.

**Comandos exactos**

```bash
pip install fastapi-cache2
```

```python
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend())
    yield

app = FastAPI(lifespan=lifespan)

BOOKS = [
    {"id": 1, "title": "Código Limpio"},
    {"id": 2, "title": "El Programador Pragmático"}
]

@app.get("/books")
@cache(expire=60)  # Cachea la respuesta por 60 segundos
async def get_books():
    return BOOKS
```

Explicar que FastAPICache agrega encabezados `X-FastAPI-Cache: HIT` o `MISS` para observar el comportamiento, y que el parámetro `namespace` en `@cache(expire=120, namespace="products")` permite invalidar en bloque con `FastAPICache.clear(namespace="products")`.

**Prompt exacto para la demo con agente de IA**

```text
Configura FastAPICache con InMemoryBackend dentro del ciclo de vida de una app FastAPI. Decora el endpoint /books con @cache para almacenar en caché su respuesta durante 30 segundos bajo el espacio de nombres "books". Crea un endpoint POST /books/refresh que limpie el espacio de nombres "books", forzando datos frescos en la siguiente solicitud.
```

**Mención de escalado con Redis**

> Para producción con múltiples instancias, se reemplaza `InMemoryBackend` por `RedisBackend` desde `fastapi_cache.backends.redis`, usando un cliente `aioredis.from_url("redis://localhost:6379")` dentro del `lifespan`.

**Qué preguntar después**

> ¿Por qué `lru_cache` no es suficiente para una API con varios workers detrás de un balanceador de carga?

### 5. ETag y caché condicional (8 minutos)

**Qué decir (literal)**

> Un ETag es un identificador único —normalmente un hash MD5— del estado actual de una respuesta. El cliente lo envía de vuelta en el encabezado `If-None-Match`; si coincide con el ETag actual, el servidor responde 304 sin cuerpo, ahorrando ancho de banda.

```python
import hashlib
import json
from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/products")
async def get_products(request: Request, response: Response):
    products = [
        {"id": 1, "name": "Guitarra", "price": 799},
        {"id": 2, "name": "Piano", "price": 2999},
        {"id": 3, "name": "Batería", "price": 699}
    ]
    body = json.dumps(products, sort_keys=True)
    etag = f'"{hashlib.md5(body.encode()).hexdigest()}"'

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304, headers={"ETag": etag})

    response.headers["ETag"] = etag
    return products
```

**Qué decir (literal)**

> Noten dos detalles del material: usamos `sort_keys=True` para que el hash sea consistente, y el ETag va entre comillas dobles según RFC 7232. FastAPICache reduce el cálculo del servidor; los ETags reducen el ancho de banda de red. Se usan juntos, no en lugar del otro.

**Qué preguntar después**

> Si un cliente envía `If-None-Match` con un ETag que ya no coincide, ¿qué debe hacer el servidor?

**Respuesta esperada**

Enviar el recurso actualizado completo junto con su nuevo ETag (respuesta 200, no 304).

### 6. Caching en Next.js: `use cache`, `cacheLife` y `cacheTag` (12 minutos)

**Qué decir (literal)**

> En Next.js el caché ya no es magia oculta: es una característica explícita controlada con la directiva `use cache`. Antes de usarla hay que habilitarla en la configuración.

```ts
// next.config.ts
const nextConfig = {
  cacheComponents: true,
}

export default nextConfig
```

Mostrar los tres niveles del material:

```ts
// Nivel de archivo: todas las funciones async exportadas comparten caché
'use cache'

export async function getData() {
  // En caché
}
```

```tsx
// Nivel de componente: cachea la salida renderizada según las props
export async function ProductCard({ id }: { id: string }) {
  'use cache'
  const product = await fetchProduct(id)
  return <div>{product.name}</div>
}
```

```ts
// Nivel de función: cachea el valor de retorno según los argumentos
export async function getExpensiveReport(month: string) {
  'use cache'
  return computeReport(month)
}
```

**Qué decir (literal)**

> La clave de caché se construye automáticamente con cuatro elementos: el ID de construcción del despliegue, el ID de la función, los argumentos serializables y, en desarrollo, un hash de recarga en caliente. Solo primitivos, objetos simples, arrays, Date, Map y Set son serializables como parte de la clave.

Explicar los perfiles `cacheLife` (ejes stale, revalidate, expire) con los perfiles integrados (`seconds`, `minutes`, `hours`, `days`, `weeks`, `max`):

```ts
import { cacheLife } from 'next/cache'

export async function getArticles() {
  'use cache'
  cacheLife('hours')  // el contenido cambia varias veces al día
  const res = await fetch('/api/articles')
  return res.json()
}
```

Y las etiquetas de invalidación bajo demanda con esquema de dos niveles (gruesa/detallada):

```tsx
'use cache'
import { cacheTag } from 'next/cache'

async function getProduct(productId: string) {
  cacheTag('products', `product-${productId}`)
  const res = await fetch(`/api/products/${productId}`)
  return res.json()
}
```

> Llamar a `revalidateTag('products', 'max')` invalida todos los productos; llamar a `revalidateTag('product-42', 'max')` invalida solo ese producto.

**Prompt exacto para la demo con agente de IA**

```text
Aplica la directiva 'use cache' a una función getProducts en lib/data.ts para cachear la lista de productos, y a un componente ProductCard que reciba userId como prop (no leas cookies ni encabezados dentro del componente cacheado). Luego agrega cacheTag('products') a getProducts y una Server Action publishPost que llame a revalidateTag('posts', 'max') tras guardar una nueva publicación.
```

**Extensión a 75 minutos: perfil personalizado**

```ts
// next.config.ts
const nextConfig: NextConfig = {
  cacheComponents: true,
  cacheLife: {
    realtime: {
      stale: 30,
      revalidate: 60,
      expire: 300,
    },
  },
}
```

**Qué preguntar después**

> ¿Qué diferencia hay entre invalidar la etiqueta `products` y invalidar la etiqueta `product-42`?

### 7. Cierre: caché en producción (4 minutos)

**Qué decir (literal)**

> Ya vimos tres capas que se combinan en producción: caché en proceso con `lru_cache` para ganancias rápidas sin dependencias, `FastAPICache` con TTL y backends enchufables (memoria o Redis) para flexibilidad a nivel de respuesta HTTP, y ETags para reducir el ancho de banda a nivel de protocolo. En Next.js, el mismo principio aplica: `use cache` para marcar qué cachear, `cacheLife` para decidir por cuánto tiempo, y `cacheTag`/`revalidateTag` para invalidar exactamente lo que cambió.

Mencionar la recomendación del material: empezar simple con Cache-Aside y TTL razonables, medir las mejoras, y añadir complejidad (Redis, invalidación por eventos, etiquetas finas) solo cuando sea necesario.

**Preguntas de chequeo final**

> Con sus propias palabras, ¿cuál es la idea más importante que se llevan sobre caching y cómo la aplicarían en un proyecto propio?

**Cierre sugerido**

- Recordar que la invalidación de caché es, según el propio material, "uno de los problemas más difíciles en la informática", y que combinar TTL con invalidación basada en eventos suele ser la solución práctica.
- Señalar los próximos pasos mencionados por el material: profundizar en Redis, prevención de cache stampede y encabezados HTTP de caching (`Cache-Control`, ETag).

## Plan de contingencia

- Si no hay tiempo para correr el script Python en vivo, mostrar el código y narrar la salida esperada línea por línea.
- Si no hay acceso a Redis, omitir la demo en vivo y quedarse en la explicación del snippet de `RedisBackend`.
- Si el grupo tiene poca experiencia previa con Next.js, priorizar los bloques 1-5 (fundamentos y FastAPI) y dejar el bloque de Next.js como lectura dirigida de código sin ejecución.

## 8) Proyecto: Optimización de rendimiento: Caching

Fuente: `ai-eng-application-caching_project_README.es.md` (asset `ai-eng-application-caching`, obtenido vía API de BreatheCode ante fallo de render del onepage).

### Resumen de requisitos del proyecto

El proyecto se construye sobre el monorepo del proyecto transversal del estudiante (no un repositorio nuevo).

- **Frontend (Next.js)**: identificar al menos dos componentes o rutas candidatos a Lazy Loading (justificando por qué conviene diferir su carga) e implementarlo con `next/dynamic` o `React.lazy`; identificar al menos una oportunidad de `useMemo` sobre un cálculo no trivial con un array de dependencias bien definido, e implementarla.
- **Backend (FastAPI)**: listar los endpoints y evaluar por cada uno coste de la operación, frecuencia de llamadas y frecuencia de cambio de los datos subyacentes; elegir al menos dos endpoints que cumplan los tres criterios (coste + frecuencia + estabilidad) e implementar su caching (diccionario en memoria con TTL, `functools.lru_cache` o Redis); implementar invalidación de caché cuando los datos subyacentes cambien (por ejemplo, en una escritura).
- **Restricción de seguridad explícita del README**: no cachear endpoints con datos personalizados, de sesión o sensibles sin acotar la clave de caché al usuario autenticado, porque una clave compartida para datos privados es una fuga de datos.
- **Informe `CACHING_REPORT.md`** con cuatro secciones obligatorias: decisiones en el frontend, decisiones en el backend (coste, frecuencia, TTL elegido y estrategia de invalidación por endpoint), al menos un intercambio explícito frescura vs. rendimiento, y qué no se cacheó y por qué.
- **Entrega**: rama nueva (`feature/caching-optimisation`) y Pull Request hacia `main` del repositorio del proyecto transversal.

### Cómo hilarlo con las lecciones previas

- El eje "costo de cálculo vs. costo de almacenamiento" y "frescura vs. rendimiento" del README es el mismo criterio de decisión presentado en el bloque 3 (las cuatro estrategias de caché) y en el bloque 2 (TTL vs invalidación basada en eventos): el proyecto pide aplicar ese criterio a endpoints reales en vez de a un ejemplo aislado.
- El caching de backend permitido en el README (diccionario en memoria con TTL, `lru_cache` o Redis) corresponde directamente a lo practicado en el bloque 4 (`lru_cache`, `FastAPICache`) y a la demo Cache-Aside del bloque 3; la invalidación exigida cuando cambian los datos subyacentes es la misma invalidación basada en eventos del bloque 2.
- El Lazy Loading y `useMemo` del frontend son técnicas de optimización distintas a la directiva `use cache` de Next.js vista en el bloque 6: conviene aclarar explícitamente en clase que el proyecto no pide `use cache`/`cacheLife`/`cacheTag`, sino Lazy Loading (`next/dynamic`/`React.lazy`) y memoización de cálculos (`useMemo`).
- El middleware de timing propuesto en el README (medir antes de cachear) conecta con la pregunta recurrente de toda la clase: "¿vale la pena cachear esto?", antes de elegir cualquier estrategia.

### Ejemplos en lenguaje natural

- Un endpoint como `GET /products?category=electronics` que aparece lento en los logs de timing y se repite en ráfagas con los mismos parámetros es, según el propio README, un candidato fuerte de caching.
- Un `POST` que escribe datos, o un `GET` cuya respuesta cambia por usuario, no es un buen candidato de caché compartido — o solo lo es con una clave de caché acotada a ese usuario.
- Un catálogo de productos puede tolerar un TTL de 60 segundos; un saldo bancario no: cada elección de TTL debe documentarse como un intercambio explícito entre velocidad y consistencia.

### Mini plan en pseudocodigo

```text
INICIO
	Paso 1 (Medir): Agregar middleware de timing en FastAPI y registrar método, ruta, status y duración de cada petición.
	Paso 2 (Generar carga realista): Sembrar (seed) datos suficientes en las tablas de lectura pesada para que los tiempos reflejen un escenario real.
	Paso 3 (Identificar candidatos backend): Cruzar coste (ms), frecuencia (repeticiones de la misma ruta) y estabilidad (¿cambian poco los datos?) para elegir al menos 2 endpoints.
	Paso 4 (Implementar caching backend): Para cada endpoint elegido, aplicar caché en memoria con TTL, lru_cache o Redis, y agregar invalidación cuando los datos subyacentes cambien.
	Paso 5 (Verificar seguridad): Confirmar que ningún endpoint con datos personales o de sesión use una clave de caché compartida.
	Paso 6 (Identificar candidatos frontend): Usar React DevTools Profiler y la pestaña Network para encontrar componentes que se re-renderizan sin cambio real de props y bundles grandes cargados de más.
	Paso 7 (Implementar optimización frontend): Aplicar Lazy Loading (next/dynamic o React.lazy) a al menos 2 componentes/rutas y useMemo a al menos 1 cálculo no trivial.
	Paso 8 (Documentar): Redactar CACHING_REPORT.md con decisiones de frontend, decisiones de backend, al menos un intercambio frescura/rendimiento y qué no se cacheó y por qué.
	Paso 9 (Entregar): Crear la rama feature/caching-optimisation y abrir el Pull Request hacia main.
FIN
```
