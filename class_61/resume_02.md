# Clase 61 — Taller paso a paso: RAG desde cero con Python y Qdrant

> Guía docente complementaria a `resume_01.md`. Construida desde `simple-rag-fastapi-qdrant-example_project_README.es.md` y la metadata obtenida del asset `simple-rag-fastapi-qdrant-example_project_asset.json`. La guía acompaña al grupo por las piezas del ejercicio y su orden; no añade un setup de Qdrant, instalación o ejecución que no esté especificado en el README fuente.

## Datos del recurso

- **Título:** RAG desde cero con Python y Qdrant
- **Autor:** `marcogonzalo`
- **Asset:** `simple-rag-fastapi-qdrant-example-es` (tipo `LESSON`)
- **Objetivo descrito:** construir un pipeline RAG con Python, Qdrant y llamadas directas a APIs, sin un framework de orquestación intermedio.
- **Evidencia de fuente:** `simple-rag-fastapi-qdrant-example_project_README.es.md`.

## Lugar en la secuencia de clase

Este taller transforma los fundamentos de `resume_01.md` en una implementación inspeccionable:

`documentos → embed → colección/puntos Qdrant → recuperación top-K → contexto + pregunta → API de chat → respuesta y contexto usado`.

Proponerlo después de haber explicado qué son los chunks/embeddings, el payload, la colección y las etapas Recuperar–Aumentar–Generar. La fuente usa cuatro textos breves como documentos, no una ingesta real de PDFs ni el `chunk_document` del ejercicio previo; mantener la diferencia explícita. Se puede usar como taller de 40–50 minutos o como extensión a la sesión integrada.

## Resultados esperados

El grupo podrá:

- Explicar qué entrada recibe cada función del pipeline y qué devuelve.
- Seguir un documento desde su embedding hasta el payload recuperado.
- Explicar por qué la dimensión configurada en Qdrant debe coincidir con la longitud del vector.
- Rastrear el contexto recuperado hasta el prompt y distinguirlo de la respuesta generada.
- Describir cómo los IDs deterministas hacen idempotente la indexación del ejemplo y por qué el filtro por score puede evitar pasar contexto irrelevante.
- Identificar explícitamente las dependencias externas: proceso Qdrant accesible y API compatible configurada por variables de entorno.

## Agenda del taller: 45 minutos

| Minutos | Paso | Evidencia/resultado |
| --- | --- | --- |
| 0–5 | Presentar el caso y dibujar el pipeline | Cada etapa queda visible |
| 5–12 | Revisar configuración y `embed` | El grupo explica vector, API y credencial |
| 12–23 | Seguir `setup` | Colección y puntos de la base de conocimiento |
| 23–30 | Seguir `retrieve` | Consulta traducida a top-K textos |
| 30–38 | Seguir `query` | Prompt aumentado, llamada de chat y respuesta |
| 38–45 | Umbral y checklist | Revisar respuesta sin evidencia y alineación dimensional |

**Versión de 30 minutos:** trazar `setup → retrieve → query` sobre el script completo y trabajar el umbral como pregunta final, sin transcribir código.

## Antes de la sesión: límites y dependencias

El README presenta Python, Qdrant, `requests` y un proveedor de API configurable. Indica variables de entorno y conexión a `localhost:6333`, pero **no documenta instalación de paquetes, cómo iniciar Qdrant, creación de credenciales ni un comando completo de ejecución**. No inventar esos pasos en esta guía; preparar de antemano un entorno que satisfaga esas dependencias o impartir el flujo como lectura guiada. No pedir al grupo que pegue claves en el material compartido.

La configuración didáctica de esta guía reemplaza el proveedor OpenAI del recurso por el gateway 4Geeks y el modelo de embeddings indicado para la clase. El esquema público de `https://llm.4geeks.ai/openapi.json` expone las rutas `/embeddings` y `/chat/completions`; no se ha probado una llamada autenticada ni se ha confirmado aquí la disponibilidad de cada modelo. La dimensión del embedding se obtiene de la respuesta real, no se presupone. El README no incluye un mock para ejecutar sin una API.

## Paso 0 — Dibujar el flujo antes del código (0–5 min)

Pizarra:

```text
Pregunta ──embed──> vector de consulta ──buscar──> Qdrant
Documentos ─embed──> vectores + payload ─upsert──> colección
Qdrant devuelve textos ──> contexto + pregunta ──> API de chat ──> respuesta
```

### Qué decir (literal)

«Vamos a seguir un caso mínimo de extremo a extremo. No hay un framework que oculte las etapas: una función crea embeddings, otra indexa, otra recupera y la última prepara el contexto y llama al modelo de chat. En cada paso vamos a preguntar qué dato entra y qué sale».

Los cuatro documentos de ejemplo hablan de 4Geeks Academy, sus cursos, LearnPack y Rigobot. La pregunta de muestra es `Where are the 4Geeks Academy campuses?`.

## Paso 1 — Configuración y embeddings: `embed(text)` (5–12 min)

### Configuración adaptada para esta clase

```bash
export LLM_API_URL="https://llm.4geeks.ai"
export LLM_CHAT_MODEL="<modelo-de-chat-disponible-en-4Geeks>"
# 4GEEKS_API_KEY empieza con un número, por lo que no se puede declarar con
# `export 4GEEKS_API_KEY=...` en Bash. Inyectarla desde un gestor de secretos o,
# desde un wrapper local que la solicite sin eco y asigne os.environ["4GEEKS_API_KEY"].
```

La clave no se solicita al alumnado ni se escribe en código, diapositivas, historial de shell o archivos versionados: cada persona autorizada la inyecta desde su gestor de secretos o entorno privado. El nombre solicitado empieza por un dígito; Python puede leerlo con `os.getenv`, pero Bash no permite declararlo directamente mediante `export`. Para una ejecución local se puede usar un wrapper Python que la lea con `getpass` (entrada sin eco) y asigne `os.environ["4GEEKS_API_KEY"]`. La URL es la raíz indicada por 4Geeks; el código agrega `/embeddings` o `/chat/completions`. El usuario especificó el modelo de embeddings, pero no uno de chat; por eso `LLM_CHAT_MODEL` queda separado y debe configurarse con un modelo de chat habilitado en la cuenta. No usar el modelo de embeddings como modelo de chat.

### Función de la fuente

```python
import os
import requests

API_KEY = os.getenv("4GEEKS_API_KEY")
API_URL = os.getenv("LLM_API_URL", "https://llm.4geeks.ai").rstrip("/")
EMBEDDING_MODEL = "litellm/madrid-spain/openrouter/perplexity/pplx-embed-v1-0.6b"


def embed(text: str) -> list[float]:
    """Convierte texto en un vector usando una API de embeddings genérica."""
    if not API_KEY:
        raise ValueError("4GEEKS_API_KEY environment variable is not set")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text
    }

    response = requests.post(f"{API_URL}/embeddings", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]
```

**Explicación del profesor:** `embed` recibe una cadena; manda el texto y nombre de modelo al endpoint de embeddings mediante `requests.post`; envía autenticación Bearer; `raise_for_status()` interrumpe ante una respuesta HTTP de error; devuelve el embedding ubicado en `data[0].embedding`. La lista de números es lo que se compara en la búsqueda vectorial, no el texto original.

### Preguntar

- «¿Qué recibe `embed` y qué devuelve?» → Texto y vector de floats.
- «¿Qué protege la verificación de `API_KEY`?» → Evita enviar la solicitud si no hay clave configurada.
- «¿Dónde está configurado el modelo de embedding?» → En `EMBEDDING_MODEL`, enviado en el payload de `embed`.
- «¿Hay que compartir la clave con el profesor o subirla a Git?» → No: se configura como variable privada `4GEEKS_API_KEY`.

## Paso 2 — Indexación: `setup()` (12–23 min)

### Datos, conexión y colección

El ejemplo usa `QdrantClient(host="localhost", port=6333)` y una colección llamada `documents`. La lista fuente contiene:

```python
documents = [
    "4Geeks Academy is a coding bootcamp with campuses in Miami and Spain.",
    "4Geeks courses cover Full Stack, Data Science, and AI Engineering.",
    "LearnPack is 4Geeks' interactive exercises platform.",
    "Rigobot is 4Geeks' AI tutor that guides students.",
]
```

La función `setup()` enumera las colecciones existentes. Para una colección nueva, la versión adaptada calcula primero los embeddings y usa la longitud del vector devuelto para `VectorParams(size=...)`; así no se arrastra el valor 1536 del ejemplo original de OpenAI. Después construye puntos `PointStruct(id=i, vector=vector, payload={"text": doc})` y los escribe con `client.upsert(...)`.

Fragmento ilustrativo de la adaptación dimensional (integrarlo en la rama que crea la colección):

```python
vectors = [embed(doc) for doc in documents]
vector_size = len(vectors[0])
if any(len(vector) != vector_size for vector in vectors):
    raise ValueError("Embedding vectors have inconsistent dimensions")

client.create_collection(
    collection_name=COLLECTION,
    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
)
points = [
    PointStruct(id=i, vector=vector, payload={"text": doc})
    for i, (doc, vector) in enumerate(zip(documents, vectors))
]
client.upsert(collection_name=COLLECTION, points=points)
```

### Qué decir (literal)

«La colección no almacena embeddings de cualquier longitud: obtenemos la dimensión de la respuesta del modelo y la usamos al crearla. Cada punto lleva un ID, el vector y un payload con el texto que necesitaremos mostrar luego. Si cambia el modelo y cambia la dimensión, habrá que recrear o migrar la colección».

### Trazado de un punto

| Campo | En este ejemplo | Para qué sirve en el flujo |
| --- | --- | --- |
| `id` | `i` de `enumerate(documents)` | Identifica el punto; el mismo orden genera los mismos IDs en las ejecuciones |
| `vector` | `embed(doc)` | Permite la búsqueda por cercanía semántica |
| `payload` | `{"text": doc}` | Conserva el texto legible que recupera `retrieve` |

El README caracteriza los IDs deterministas como idempotencia: volver a insertar puntos con los mismos IDs los sobrescribe en lugar de duplicarlos. En esta implementación, si la colección ya existe, `setup()` no vuelve a indexar nada. No afirmar que el código sincroniza actualizaciones del listado después de la primera creación.

### Preguntar

- «¿Cómo evitamos asumir una dimensión fija?» → Medimos `len(vector)` al recibir el embedding y creamos la colección con ese tamaño; verificamos que todos los vectores tengan longitud consistente.
- «¿Por qué guardamos el texto en `payload` además del vector?» → La búsqueda devuelve el contenido legible para construir el contexto.
- «¿Qué evita usar el mismo ID al reinsertar?» → Duplicar puntos con IDs diferentes en el caso de re-upsert del mismo registro.

## Paso 3 — Recuperación: `retrieve(query, limit=2)` (23–30 min)

```python
def retrieve(query: str, limit: int = 2) -> list[str]:
    vector_query = embed(query)
    results = client.query_points(
        collection_name=COLLECTION,
        query=vector_query,
        limit=limit,
    )
    return [r.payload["text"] for r in results.points]
```

La función recibe pregunta y cantidad máxima de resultados; la embebe usando el mismo `embed`, consulta la colección mediante `query_points` y devuelve una lista de los textos guardados en los payloads. El uso de la misma función de embedding para documentos y consulta mantiene el proceso conforme al diseño descrito.

### Qué decir (literal)

«La consulta pasa por la misma representación vectorial que los documentos. Qdrant devuelve los puntos cercanos; nosotros extraemos sus textos, no enviamos el vector al LLM como si fuera contexto».

### Preguntar

- «¿Qué controla `limit`?» → Cuántos puntos se solicitan.
- «¿Qué devuelve `retrieve` a quien la llama?» → Lista de textos de los payloads recuperados.
- «¿En qué etapa RAG estamos?» → Recuperar.

## Paso 4 — Aumentar y generar: `query(user_query, limit=2)` (30–38 min)

La función completa concatena los textos recuperados, arma un prompt con contexto y pregunta, llama al endpoint de chat con `MODEL_NAME` y devuelve un diccionario con `answer` y `context_used`. La versión didáctica del README usa esta forma:

```python
MODEL_NAME = os.getenv("LLM_CHAT_MODEL")


def query(user_query: str, limit: int = 2) -> dict:
    context_chunks = retrieve(user_query, limit=limit)
    context = "\n".join(context_chunks)

    prompt = (
        "Use the following context to answer the question. If you do not know the answer, "
        "or if the context doesn't contain it, honestly state that you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {user_query}\n"
        "Answer:"
    )

    if not API_KEY:
        raise ValueError("4GEEKS_API_KEY environment variable is not set")

    if not MODEL_NAME:
        raise ValueError("LLM_CHAT_MODEL must name a chat model enabled for this API key")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful and honest assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0
    }

    response = requests.post(f"{API_URL}/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    answer = response.json()["choices"][0]["message"]["content"]

    return {"answer": answer, "context_used": context}
```

**Enseñar las etapas por separado:** `retrieve` es recuperar; unir `context_chunks` y colocar contexto más pregunta en `prompt` es aumentar; el `POST` a `/chat/completions` es generar. El prompt explícito ordena no completar con conocimiento general cuando el contexto no contenga la respuesta. `temperature=0.0` es el valor del ejemplo. El resultado conserva el contexto usado para poder inspeccionar qué información se pasó al modelo.

### Qué decir (literal)

«No evaluemos solo la frase final. Este pipeline también devuelve `context_used`: podemos revisar qué textos se recuperaron y si la respuesta tiene fundamento en ellos. Prompt y contexto son partes visibles de la llamada, no magia del framework».

### Actividad de lectura

Seguir la pregunta de ejemplo `Where are the 4Geeks Academy campuses?` y predecir qué tipo de evidencia debe aparecer en `context_used`. La lista de documentos incluye el texto que afirma que hay campus en Miami y España. No prometer una respuesta literal fija del modelo: el README no fija una salida exacta de la API.

## Paso 5 — Umbral de score y caso sin evidencia (38–42 min)

El README explica que top-K siempre puede devolver los vecinos más cercanos aunque una consulta no relacionada tenga puntuaciones muy bajas. Muestra `query_points` conservando resultados que cumplan `r.score >= MIN_SCORE`, con `MIN_SCORE = 0.7` como ejemplo, y deja que el pipeline responda que no conoce la respuesta si no queda contexto.

### Punto de integración que hay que señalar

El snippet de umbral del README usa `vector_query` y `limit`, nombres que deben estar disponibles en el alcance de la función donde se incorpore. Tal como está mostrado, es un fragmento para integrar en `retrieve`, no un bloque independiente ejecutable. Explicar que, para aplicar el umbral al pipeline, `retrieve` debe devolver solo los textos de los hits que pasan el score; si la lista queda vacía, el prompt recibe contexto vacío y la instrucción de fallback permite al modelo indicar que no sabe. No declarar un umbral universal: `0.7` está etiquetado como ejemplo del recurso.

### Preguntar

- «¿Por qué no basta con pedir los dos vecinos más cercanos?» → Puede que ninguno sea realmente relevante.
- «¿Qué ocurre si todos están bajo el umbral?» → No se pasa ningún fragmento relevante; el modelo debe indicar que no sabe.

## Paso 6 — Checklist y revisión crítica (42–45 min)

Leer el checklist de la fuente como verificación de diseño:

1. La longitud de `embed()` coincide exactamente con `VectorParams(size=...)`; en esta adaptación se deriva del vector real.
2. Los IDs deterministas evitan duplicados al volver a insertar los mismos puntos.
3. `query()` usa el contexto recuperado en lugar de confiar en conocimiento general.
4. Una pregunta ajena al corpus puede quedar por debajo del `MIN_SCORE`.
5. Si ningún chunk supera el umbral, el sistema responde honestamente «no lo sé» en lugar de inventar.

### Cierre (literal)

«El pipeline se puede depurar etapa por etapa: inspectamos el embedding, lo que se guardó, los resultados de recuperación, el contexto del prompt y la respuesta. La lección central no es llamar a un framework, sino comprobar qué evidencia recuperó el sistema y medir relevancia en lugar de asumirla».

## Plan del profesor / contingencia

- **Si la API o Qdrant no están disponibles:** realizar walkthrough de los datos y funciones en pantalla; los JSON y el README alcanzan para explicar el flujo, pero la salida de la llamada remota no se puede reproducir sin dependencias.
- **Si `setup()` no indexa al repetirlo:** comprobar la condición de existencia de la colección. El código de fuente indexa solo cuando la colección aún no existe; no se trata de un refresco general de datos.
- **Si dimensión o métrica no concuerdan:** señalar los dos puntos que deben verificarse: vector que retorna `embed` y `VectorParams(size=..., distance=...)`.
- **Si la búsqueda devuelve texto inesperado:** inspeccionar vector de consulta, top-K, payload y, en el tramo avanzado, score/umbral antes de modificar el prompt.
- **Si el LLM responde sin apoyo:** inspeccionar `context_used` y el prompt enviado; distinguir error de recuperación de error de fidelidad/generación.

## Trazabilidad y notas de precisión

El contenido técnico del pipeline sigue el asset Markdown archivado en `simple-rag-fastapi-qdrant-example_project_README.es.md`; la configuración de proveedor en esta guía se adapta a la solicitud de usar 4Geeks y no modifica ese original archivado. La metadata del endpoint BreatheCode se archiva en `simple-rag-fastapi-qdrant-example_project_asset.json`. Los tiempos, preguntas, configuración 4Geeks y contingencias son organización/adaptación docente, no requisitos del asset.

**Diferencias dentro de la fuente:** la sección paso a paso incluye una instrucción explícita de fallback («honestly state that you don't know») y un mensaje de sistema; el script completo posterior tiene un prompt más corto y solo un mensaje de usuario. Al impartir el objetivo de prevención de alucinaciones, usar y señalar la versión explícita del paso 4, y advertir que el script completo debe conservar esa instrucción si se quiere el mismo fallback descrito. La fuente asume una dimensión 1536 para su modelo original; esta adaptación la deriva de la respuesta del modelo configurado. Confirmar que el modelo de embeddings, el modelo de chat, SDK/API y versión del cliente Qdrant sean compatibles en el entorno real; aunque las rutas aparecen en el esquema público del gateway, no se ha ejecutado una llamada autenticada y el asset no documenta versiones ni setup de infraestructura.
