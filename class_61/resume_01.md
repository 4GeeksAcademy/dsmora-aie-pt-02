# Clase 61: Construir los fundamentos de un sistema RAG

> Guía docente elaborada a partir de los cuatro JSON scrapeados desde LearnPack: `tutorial.json` (RAG, 7 lecciones), `tutorial_2.json` (bases de datos vectoriales, 7), `tutorial_3.json` (Qdrant, 8) y `tutorial_4.json` (fragmentación y embedding, 8). La agenda, las frases docentes, las actividades y la secuencia didáctica son organización pedagógica; las definiciones, los ejemplos y el código técnico se mantienen dentro de lo que aparece en esas fuentes.

> **Material de proyecto añadido:** el asset `simple-rag-fastapi-qdrant-example-es` y su guía de taller paso a paso están en `simple-rag-fastapi-qdrant-example_project_asset.json`, `simple-rag-fastapi-qdrant-example_project_README.es.md` y `resume_02.md`. Usar `resume_02.md` como continuación práctica de esta guía.

## Hilo de continuidad

La clase 60 trató el monitoreo de flujos de ML desplegados: observar estados, duración, frescura y volumen. Esta sesión cambia del seguimiento operativo al diseño del conocimiento que consumirá una aplicación de IA: cómo hacer que un LLM recupere información externa antes de responder y qué componentes forman esa capa de recuperación. La secuencia de los cuatro cursos arma una progresión: problema y cadena RAG → significado y búsqueda vectorial → fragmentación y embeddings → almacenamiento, búsqueda y filtros en Qdrant → diagnóstico de calidad.

**Frase de transición:** «En la clase anterior hicimos visibles los flujos en producción. Hoy vamos a mirar otra parte de un sistema de IA: cómo conectar un modelo de lenguaje con conocimiento actualizado y propio, y cómo organizarlo para que pueda recuperarlo de manera útil».

## Objetivos

Al final, el estudiante podrá:

- Explicar la brecha de conocimiento y el riesgo de alucinación que motivan RAG, y ordenar las etapas **Recuperar → Aumentar → Generar**.
- Diferenciar búsqueda por coincidencia exacta de búsqueda por similitud semántica, y explicar el papel de vectores, métricas de distancia y ANN.
- Describir chunks autónomos, estrategias de fragmentación, solapamiento y embeddings, y relacionar el tamaño de vector con la configuración de una colección.
- Nombrar colección, punto, vector y payload en Qdrant, e interpretar una secuencia básica de crear, insertar, buscar y filtrar.
- Identificar antipatrones comunes y explicar qué revelan Recall@k y fidelidad sobre un pipeline RAG.

## Agenda sugerida: 75 minutos

| Minutos | Bloque | Resultado esperado |
| --- | --- | --- |
| 0–8 | Problema: conocimiento y límites de un LLM | Justificar RAG |
| 8–18 | Cadena RAG y respuesta confiable | Seguir Recuperar, Aumentar, Generar |
| 18–30 | Búsqueda semántica y bases vectoriales | Contrastar búsqueda exacta, semántica y ANN |
| 30–43 | Fragmentación y embeddings | Relacionar chunking, contexto y dimensión |
| 43–58 | Qdrant como capa vectorial | Leer colección, punto, upsert, búsqueda y filtros |
| 58–68 | Fallos y evaluación | Diagnosticar con Recall@k y fidelidad |
| 68–75 | Síntesis y chequeo | Reconstruir de documento a respuesta fundamentada |

**Recorte a 60 minutos:** hacer la sección de métricas como una tabla oral, recorrer Qdrant sin escribir el código y limitar la comparación de estrategias de chunking. Mantener la cadena, la distinción vector/payload y la explicación de cómo evaluar.

**Extensión a 75 minutos:** usar los tiempos completos y hacer la lectura guiada de los ejemplos de fragmentación y Qdrant. La guía no presupone que se instale ni ejecute el código en clase: los cursos scrapeados no proporcionan un procedimiento único de instalación o entorno común.

**Extensión con taller de proyecto:** si se dispone de otra sesión o bloque práctico, continuar con `resume_02.md` para recorrer `embed`, `setup`, `retrieve` y `query` de un pipeline completo en Python/Qdrant. Ese recurso incluye llamadas API y dependencias externas, y por ello requiere preparar el entorno por separado.

## Preparación docente

- Tener disponibles los cuatro JSON de `class_61/` como trazabilidad del curso.
- Recordar el hilo de continuidad con monitoreo visto en clase 60.
- Preparar la pizarra con esta cadena: `documento → chunks → embeddings → Qdrant → consulta → contexto recuperado → prompt → respuesta`.
- Si se proyecta código, presentar el snippet de fragmentación como ejercicio conceptual del curso. Su función `embed` se declara simulada y determinista; no representa la calidad semántica de un modelo real.
- El ejemplo práctico de Qdrant usa un cliente en memoria, vectores de 4 dimensiones de demostración y resultados concretos indicados por el curso. No presentarlo como colección con embeddings generados desde documentos reales.
- No asumir un comando de instalación, claves de API, servidor, modelo externo, ni una implementación completa de LLM: no hay un único setup que los cuatro JSON definan.

## 0–8 min | El problema que resuelve RAG

### Qué decir (literal)

«Un modelo de lenguaje aprendió con datos que tienen una fecha de corte y puede no conocer documentos privados o actualizaciones posteriores. Cuando le falta evidencia también puede producir una respuesta que suena plausible, pero es incorrecta. RAG introduce recuperación de información relevante para que la respuesta se apoye en conocimiento disponible para la aplicación».

El primer curso presenta, entre otros, ejemplos de guías médicas desactualizadas y un chatbot de soporte que desconoce una función nueva. También explica que actualizar el modelo mediante ajuste fino puede ser costoso y lento y que actualizar hechos no es lo mismo que cambiar comportamiento. Mantener el foco de hoy en recuperación; no abrir una discusión de fine-tuning más allá de esa distinción.

### Preguntar

- «¿Qué dos límites del LLM aparecen como motivación para RAG?» → Fecha de corte/conocimiento estático y alucinación cuando falta información relevante.
- «¿Qué tipo de información propia puede aportar una capa externa?» → Documentación interna o propietaria que no estaba en el entrenamiento.

## 8–18 min | Cadena RAG: recuperar, aumentar, generar

### Explicación docente

1. **Recuperar:** convertir la consulta del usuario en un embedding; usarlo para buscar en una base vectorial los fragmentos top-K semánticamente similares. El JSON da el ejemplo `text-embedding-ada-002` para la consulta y Qdrant como base.
2. **Aumentar:** incorporar los fragmentos recuperados junto con la consulta en el prompt. Las instrucciones del sistema deben decir que se responda a partir del contexto, se cite qué fragmento respalda la respuesta y se indique que no se sabe si el contexto no alcanza.
3. **Generar:** el LLM produce una respuesta usando la consulta y el contexto aumentado.

El curso recomienda sintetizar varios fragmentos pertinentes en lugar de seleccionar manualmente uno, limitar la cantidad a fragmentos enfocados y definir una respuesta de fallback. Como ejemplo fuente, muestra un sistema que solicita responder solo con el contexto y decir «No pude encontrar información sobre eso en nuestra documentación» cuando no hay base.

### Qué decir (literal)

«La recuperación no es la respuesta final: trae evidencia candidata. Después la añadimos al prompt y pedimos al modelo que la use. Si el contexto no responde, una aplicación confiable no le pide que complete el vacío con una conjetura; le define un fallback».

### Chequeo

Pedir al grupo ordenar las tarjetas: **Generar**, **Recuperar**, **Aumentar**. Orden correcto: Recuperar → Aumentar → Generar.

## 18–30 min | De búsqueda por palabras a búsqueda vectorial

### Contraste

- SQL/NoSQL son útiles para consultas estructuradas, valores exactos, rangos, claves y coincidencias; por sí solos no miden con eficacia la cercanía semántica de dos textos distintos.
- Una **base vectorial** almacena una representación numérica de longitud fija (embedding) y datos asociados como payload. Permite recuperar registros cuyo significado esté cerca de la consulta, aunque no comparta las mismas palabras.
- **Métrica de distancia:** define cómo se compara la cercanía. El curso describe coseno como ángulo/dirección (común en embeddings de texto), producto punto como ángulo y magnitud, y euclidiana como distancia en línea recta.
- **Búsqueda exacta del vecino más cercano:** compara la consulta con cada vector almacenado; puede ser impráctica a gran escala. **ANN** (vecinos más cercanos aproximados) sacrifica algo de precisión para ganar velocidad. El curso presenta HNSW como índice basado en un grafo jerárquico de vecinos para acelerar la búsqueda aproximada; no convertir esta clase en una explicación algorítmica profunda.

### Qué decir (literal)

«La base vectorial no adivina el texto: compara representaciones numéricas. Si dos textos expresan ideas parecidas, sus embeddings pueden quedar próximos aunque las palabras cambien. A escala, ANN acepta una aproximación controlada para no comparar exhaustivamente cada registro».

### Preguntar

- «¿Qué diferencia una búsqueda semántica de buscar la frase exacta?» → Puede recuperar significado relacionado sin igualdad de palabras.
- «¿Qué intercambia ANN frente a la búsqueda exacta?» → Algo de precisión por una mejora importante de velocidad.
- «¿Qué métrica del curso se suele usar con texto?» → Similitud coseno.

## 30–43 min | Fragmentos y embeddings

### Conceptos a enseñar

Un **chunk** es una pieza significativa de un documento y debe entenderse por sí sola. La fragmentación es importante porque cada pieza será indexada y recuperada por separado:

- Un chunk demasiado grande promedia demasiadas ideas en el embedding y puede ser vago o irrelevante.
- Uno demasiado pequeño puede perder contexto (por ejemplo, «como se mencionó antes»).
- Estrategias listadas por la fuente: tamaño fijo (simple, pero ignora estructura), por oración (respeta oraciones, que varían de longitud), por párrafo y semántica (usa embeddings para detectar cambios de tema; mayor calidad y complejidad).
- Respetar límites naturales, conservar contexto con solapamiento y limpiar encabezados/menús/artefactos HTML contribuye a mejores fragmentos. El curso también recomienda contexto de sección en el fragmento cuando se necesita procedencia.

Un **embedding** transforma texto en un vector numérico de longitud fija que representa su significado semántico. Significados cercanos tienden a producir vectores cercanos. La dimensión del vector es una propiedad que debe corresponder a la configuración de la colección Qdrant. Los modelos tienen un límite de tokens; la fuente advierte que superar ese límite puede provocar truncamiento silencioso de la entrada. Ejemplo que aparece en el curso: `all-MiniLM-L6-v2` genera 384 dimensiones y se menciona un límite común de 512 tokens, sin tratarlos como valores universales para todos los modelos.

### Código fuente del ejercicio

El curso define `chunk_document` para dividir texto por ventanas de caracteres con solapamiento, `embed` como función simulada de cuatro dimensiones e `ingest` para devolver cada fragmento junto con el vector producido. La implementación que se muestra es:

```python
def chunk_document(text, chunk_size, overlap):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def embed(text):
    # Retorna un vector determinista de 4 dimensiones para cualquier cadena de entrada
    h = hash(text) % 1000
    return [h / 1000, (h * 3 % 1000) / 1000, (h * 7 % 1000) / 1000, (h * 11 % 1000) / 1000]


def ingest(text, chunk_size, overlap):
    chunks = chunk_document(text, chunk_size, overlap)
    embedded_chunks = [{"chunk": chunk, "vector": embed(chunk)} for chunk in chunks]
    return embedded_chunks


sample_text = "Hola mundo. Este es un documento de prueba para demostrar la división y embedding."
result = ingest(sample_text, chunk_size=20, overlap=5)
```

La función avanza `chunk_size - overlap` caracteres cada vez. Con los valores del ejemplo, cada ventana tiene hasta 20 caracteres y se repiten 5 caracteres entre ventanas adyacentes. `embed` es únicamente un helper simulado de demostración: el uso de `hash` genera un vector fijo de cuatro coordenadas para esta ejecución, pero no calcula semántica como un modelo real. `ingest` devuelve una lista de diccionarios `{ "chunk": ..., "vector": ... }`.

### Qué decir (literal)

«El tamaño no es un detalle aislado: define qué idea representa cada vector. Buscamos fragmentos comprensibles por sí solos, suficientemente enfocados y sin perder el contexto de los límites. Después cada fragmento se convierte en un vector compatible con la dimensión de la colección».

### Actividad corta

Proponer oralmente un chunk que termine con «como se mencionó antes» y preguntar qué contexto falta. Luego comparar un párrafo completo con una ventana demasiado amplia: ¿cuál daría una búsqueda más enfocada y por qué? No fijar un tamaño óptimo universal; el curso indica que depende del documento y del caso de uso.

## 43–58 min | Qdrant, la capa de almacenamiento y búsqueda

### Vocabulario central

- **Colección:** contenedor de puntos que comparten dimensión vectorial y métrica de distancia.
- **Punto:** registro que reúne ID único, vector y payload.
- **Vector:** embedding usado para búsqueda por similitud.
- **Payload:** metadatos JSON (por ejemplo, título, fuente, idioma, versión) que hacen interpretable y filtrable el resultado.

Qdrant se presenta como base vectorial abierta, con persistencia y filtrado nativo. El material la ubica en el paso de recuperación de RAG. La configuración de colección debe concordar con el tamaño de los embeddings. Para pruebas, el curso usa un cliente en memoria; para una instancia en ejecución también muestra conexión local en `localhost:6333`.

### Ejemplo guiado del JSON de Qdrant

El siguiente fragmento reúne el ejemplo fuente de un cliente en memoria, colección de tamaño 4, inserción de puntos y búsqueda top-K. Los vectores son los valores didácticos del curso:

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(":memory:")
client.create_collection(
    collection_name="knowledge_base",
    vectors_config=VectorParams(size=4, distance=Distance.COSINE),
)

DOCUMENTS = [
    {"id": 1, "vector": [0.1, 0.8, 0.3, 0.5], "payload": {"title": "Intro to RAG"}},
    {"id": 2, "vector": [0.9, 0.1, 0.7, 0.2], "payload": {"title": "SQL Basics"}},
    {"id": 3, "vector": [0.2, 0.7, 0.4, 0.6], "payload": {"title": "Vector Search"}},
    {"id": 4, "vector": [0.8, 0.2, 0.6, 0.3], "payload": {"title": "Neural Networks"}},
]

points = [
    PointStruct(id=doc["id"], vector=doc["vector"], payload=doc["payload"])
    for doc in DOCUMENTS
]
client.upsert(collection_name="knowledge_base", points=points)


def search(client, query_vector, top_k):
    results = client.search(
        collection_name="knowledge_base",
        query_vector=query_vector,
        limit=top_k,
    )
    return [hit.payload for hit in results]

print(search(client, [0.1, 0.9, 0.2, 0.4], top_k=2))
# Salida esperada por la lección:
# [{'title': 'Intro to RAG'}, {'title': 'Vector Search'}]
```

**Explicar el flujo:** `QdrantClient(":memory:")` crea un cliente temporal de pruebas; `create_collection` declara cuatro dimensiones y coseno; `PointStruct` empaqueta ID, vector y payload; `upsert` inserta o actualiza los puntos; `search` recibe el vector de consulta y `limit=top_k`, y se extraen los payloads de los hits. La salida indicada corresponde a los vectores de ejemplo y no a contenido semántico generado.

### Filtrado por payload

Qdrant permite combinar similitud con metadatos. El curso muestra construir `Filter` + `FieldCondition` + `MatchValue` para recuperar solo registros cuyo campo `language` sea `en`, y pasar el filtro como `query_filter` en `client.search`. De este modo, el payload no es solo descripción: restringe el espacio de resultados, por ejemplo cuando existen contenidos parecidos en diferentes lenguajes.

También se muestran `set_payload` para actualizar metadatos sin cambiar el vector y `delete` para eliminar un punto. No hace falta ejecutar estas operaciones en la sesión; usar la distinción para explicar gestión de registros.

### Qué decir (literal)

«Una colección impone un espacio vectorial común; cada punto guarda vector y contexto. En una búsqueda, el vector encuentra cercanía semántica y el payload permite devolver un título legible o restringir resultados. Así Qdrant conecta embeddings con documentos que el resto de la aplicación puede usar».

### Preguntas

- «¿Qué tres componentes reúne un punto?» → ID, vector y payload.
- «¿Por qué el tamaño 4 de esta colección?» → Porque los vectores de demostración tienen cuatro coordenadas.
- «¿Qué hace `upsert`?» → Inserta o actualiza puntos.
- «¿Qué aporta `query_filter`?» → Restringe por valores de metadatos además de la búsqueda vectorial.

## 58–68 min | Fallos y evaluación del pipeline

### Antipatrones señalados en los cursos

**Preparación/recuperación:** chunks demasiado grandes o pequeños; partir a mitad de oración o ignorar límites naturales; contenido sucio como menús/HTML; omitir contexto de fuente; confiar en top-1; no filtrar por metadatos o no usar umbral de similitud; incluir FAQs con pregunta y respuesta juntas en el embedding; envenenamiento de datos. La guía no agrega una política de mitigación específica para cada riesgo: pedir que los estudiantes lo localicen en la etapa que puede afectar.

**Generación:** enviar demasiados fragmentos puede enterrar el contexto útil; no indicar que el modelo use solo el contexto o qué hacer cuando la respuesta no está presente puede favorecer alucinaciones. Pedir síntesis de múltiples fragmentos pertinentes, no una cantidad indiscriminada.

### Métricas que propone la fuente

- **Recall@k:** indica si el fragmento correcto aparece dentro de los primeros `k` recuperados. El curso define el resultado como 1 si aparece y 0 si no; un valor bajo apunta a problemas de recuperación. Recuperar `k=3–5` puede dar mejor cobertura que mirar solo el primer resultado, y se recomienda usar un umbral mínimo de similitud para descartar resultados de baja confianza.
- **Fidelidad:** mide si la respuesta generada refleja con precisión el contexto recuperado. Baja fidelidad puede indicar que el modelo alucina o ignora el contexto.

Usar la matriz cualitativa para diagnóstico: Recall@k bajo y fidelidad baja sugiere problemas en recuperación y generación; Recall@k alto y fidelidad baja indica que llega contexto relevante, pero la respuesta no lo está usando adecuadamente. Si la recuperación falla, revisar fragmentación/embedding/filtrado; si la respuesta no refleja el contexto, revisar instrucciones del prompt.

### Qué decir (literal)

«Necesitamos separar dos preguntas: ¿encontramos el fragmento correcto? y ¿la respuesta respeta lo recuperado? Recall@k observa la primera y fidelidad la segunda. Un sistema puede recuperar bien y, aun así, responder mal».

### Chequeo de escenarios

1. No aparece el chunk correcto entre los primeros resultados → Recall@k bajo; revisar recuperación.
2. Aparece evidencia correcta, pero la respuesta la contradice → fidelidad baja; revisar cómo se condiciona la generación.
3. Una consulta sobre Python recupera contenido parecido de JavaScript → examinar metadatos y filtros.
4. La respuesta cita una frase genérica de navegación → revisar limpieza del texto antes de fragmentar e indexar.

## 68–75 min | Cierre: reconstruir el camino

Pedir que el grupo reconstruya en voz alta:

`Documento limpio → fragmentos autosuficientes → embeddings de dimensión conocida → puntos (ID, vector, payload) en una colección → embedding de consulta → búsqueda top-K y filtros → contexto en el prompt → respuesta fundamentada o fallback`.

### Cierre sugerido (literal)

«RAG no es solo conectar un LLM a una base. La calidad empieza antes de la pregunta: cómo limpiamos y fragmentamos los documentos, qué embedding los representa y cómo quedan almacenados. Después medimos por separado si recuperamos la evidencia y si la respuesta se mantiene fiel a ella».

### Preguntas finales

- «¿Cuáles son las tres etapas de RAG?» → Recuperar, aumentar y generar.
- «¿Qué mantiene juntos el vector y el contexto legible?» → El punto con ID, vector y payload.
- «¿Qué revisarías primero con Recall@k bajo y fidelidad alta?» → Recuperación: fragmentos, embedding o filtros.
- «¿Qué necesita decir el prompt si no hay evidencia?» → Que lo indique/no invente, usando el fallback definido.

## Nota de trazabilidad y límites

El contenido técnico se ha tomado de los cuatro JSON de `class_61/`. El ejemplo de `embed` de cuatro dimensiones es simulado, no un embedding semántico real. Los ejemplos de Qdrant usan vectores de demostración y una base en memoria. Los nombres de estrategias, métricas, componentes, riesgos y la salida esperada se encuentran en las lecciones scrapeadas. La agenda, la frase de continuidad, el guion literal, las preguntas y la pizarra son estructura docente añadida; no se presentan como teoría del curso. No se agregan instalación, comandos, credenciales ni una implementación externa del LLM porque las fuentes no definen un setup común.
