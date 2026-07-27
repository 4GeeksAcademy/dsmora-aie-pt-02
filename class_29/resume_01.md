# Guia Docente Completa: Class 29 - API en Python, Pydantic y Documentacion

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos. El profesor puede saltarse bloques sin perder continuidad.

## 1) Objetivo de la clase

Al finalizar, el estudiante podra:

- Construir una API CRUD basica con FastAPI para servir a un frontend.
- Validar entradas y serializar salidas con modelos Pydantic de forma segura.
- Diferenciar modelos de entrada y salida para evitar fuga de datos sensibles.
- Publicar y mejorar documentacion de endpoints para humanos y agentes AI/LLM.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y contexto: 5 min
- Bloque A (CRUD FastAPI): 14 min
- Bloque B (Pydantic validacion/serializacion): 16 min
- Bloque C (endpoint completo y pruebas): 14 min
- Bloque D (documentacion API para humanos + AI): 11 min
- Cierre + checklist + Q&A: 5 min

Si tienes 75 min:

- Anade 10 min de practica guiada con una segunda entidad (por ejemplo, `tasks`).

Si tienes 60 min:

- Recorta 5 min del Bloque D y 5 min del Bloque C (haz la prueba de errores solo para un caso 422).

## 3) Preparacion docente (antes de clase)

Checklist tecnico:

- Python 3.10+ disponible.
- Entorno virtual y dependencias instaladas (fastapi, uvicorn).
- `curl` disponible para pruebas rapidas HTTP.

Comandos de verificacion previa:

```bash
python3 --version
python3 -m pip --version
curl --version
```

Inicializacion recomendada del proyecto demo:

```bash
mkdir -p class_29/live_api_demo
cd class_29/live_api_demo
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi "uvicorn[standard]"
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Que decir (literal):

"Hoy vamos a conectar tres piezas que en produccion no se separan: endpoints CRUD, validacion de datos y documentacion util. Si una falla, toda la integracion backend-frontend se rompe."

"La meta no es memorizar decoradores. La meta es disenar contratos API que sean correctos, seguros y entendibles por personas y por agentes AI."

## Bloque A - CRUD FastAPI para servir al frontend (14 min)

### A1. Concepto rapido (4 min)

Que decir (literal):

"Un endpoint es un contrato: ruta + metodo HTTP + forma de entrada + forma de salida. CRUD se traduce a GET, POST, PUT, PATCH, DELETE."

"El frontend no adivina. El frontend depende de respuestas predecibles y codigos HTTP correctos como 200, 201, 404 y 422."

### A2. Demo guiada (6 min)

Ejecuta:

```bash
cat > main.py << 'PY'
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Class 29 Contacts API")

contacts = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]

@app.get("/contacts")
def get_contacts():
    return contacts

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):
    for c in contacts:
        if c["id"] == contact_id:
            return c
    raise HTTPException(status_code=404, detail="Contacto no encontrado")
PY

uvicorn main:app --reload --port 8000
```

En otra terminal, prueba:

```bash
curl -s http://127.0.0.1:8000/contacts
curl -s http://127.0.0.1:8000/contacts/1
curl -s http://127.0.0.1:8000/contacts/999
```

Que decir (literal):

"Fijense como 404 comunica semantica de recurso no encontrado. Es mejor que responder 200 con un texto de error ambiguo."

### A3. Mini practica (4 min)

Prompt exacto sugerido:

```text
Actua como senior backend teacher. Dame un endpoint DELETE /contacts/{contact_id} para FastAPI usando una lista en memoria. Requisitos: devolver {"detail":"Contacto eliminado"} si existe; si no existe, lanzar HTTPException 404 con detail "Contacto no encontrado". Incluye codigo completo listo para pegar en main.py.
```

## Bloque B - Pydantic para validacion y serializacion (16 min)

### B1. Concepto y riesgos (5 min)

Que decir (literal):

"Datos externos no son confiables. Pydantic convierte, valida y rechaza lo invalido antes de que ensucie la logica de negocio."

"Sin modelos de salida, puedes filtrar de mas y exponer campos privados. Con response_model definimos exactamente que sale."

### B2. Ejemplo practico (7 min)

Ejecuta:

```bash
cat > main.py << 'PY'
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Class 29 Contacts API")

contacts = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "internal_note": "VIP"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "internal_note": "Late payer"},
]

class ContactCreate(BaseModel):
    name: str
    email: str

class ContactPublic(BaseModel):
    id: int
    name: str
    email: str

class ContactPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

@app.get("/contacts", response_model=list[ContactPublic])
def get_contacts():
    return contacts

@app.post("/contacts", response_model=ContactPublic, status_code=201)
def create_contact(payload: ContactCreate):
    new_id = max(c["id"] for c in contacts) + 1 if contacts else 1
    record = {
        "id": new_id,
        "name": payload.name,
        "email": payload.email,
        "internal_note": "created from API",
    }
    contacts.append(record)
    return record

@app.patch("/contacts/{contact_id}", response_model=ContactPublic)
def patch_contact(contact_id: int, payload: ContactPatch):
    for c in contacts:
        if c["id"] == contact_id:
            updates = payload.model_dump(exclude_unset=True)
            c.update(updates)
            return c
    raise HTTPException(status_code=404, detail="Contacto no encontrado")
PY
```

Pruebas clave:

```bash
curl -s -X POST http://127.0.0.1:8000/contacts \
  -H "Content-Type: application/json" \
  -d '{"name":"Carla","email":"carla@example.com"}'

curl -s -X POST http://127.0.0.1:8000/contacts \
  -H "Content-Type: application/json" \
  -d '{"name":null,"email":12345}'
```

Que decir (literal):

"El segundo caso debe devolver 422. Eso es bueno: la API se protege sola y le da feedback preciso al cliente."

### B3. Validacion (4 min)

Checklist:

- El endpoint POST devuelve 201 cuando el payload es valido.
- El endpoint POST devuelve 422 cuando el payload rompe tipos requeridos.
- El endpoint GET no expone `internal_note` gracias a `response_model`.

## Bloque C - Endpoint completo y prueba de contrato (14 min)

Ejecuta:

```bash
cat > jobs.py << 'PY'
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Jobs API")

class JobCreate(BaseModel):
    title: str
    company: str
    salary: float
    recruiter_notes: str

class JobPublic(BaseModel):
    title: str
    company: str

@app.post("/jobs", response_model=JobPublic)
def create_job(payload: JobCreate):
    return payload
PY

uvicorn jobs:app --reload --port 8001
```

Prueba de contrato:

```bash
curl -s -X POST http://127.0.0.1:8001/jobs \
  -H "Content-Type: application/json" \
  -d '{"title":"Backend Engineer","company":"Acme Corp","salary":85000,"recruiter_notes":"FastAPI solido"}'
```

Prompt exacto sugerido:

```text
Necesito pruebas manuales con curl para validar contrato de un endpoint POST /jobs con response_model JobPublic. Dame: 1) caso valido, 2) caso invalido por tipo de salary, 3) criterios esperados de status code y campos visibles en respuesta. Responde en markdown con bloques bash.
```

## Bloque D - Documentacion API para humanos y agentes AI (11 min)

Ejecuta:

```bash
curl -s http://127.0.0.1:8000/openapi.json | head -n 40
```

Que decir (literal):

"FastAPI genera OpenAPI automaticamente, pero eso no significa documentacion perfecta. Tenemos que enriquecer descripciones, ejemplos y errores para que humanos y LLMs entiendan la intencion del endpoint."

"Una regla simple: si otro equipo no puede usar tu endpoint sin preguntarte por chat, la documentacion aun no esta lista."

Prompt exacto sugerido:

```text
Ayudame a mejorar la documentacion de este endpoint FastAPI:
- Ruta: POST /contacts
- Entrada: ContactCreate(name:str, email:str)
- Salida: ContactPublic(id:int, name:str, email:str)
Quiero: summary, description clara, ejemplo de request JSON, ejemplo de response JSON, y errores 422/404 documentados. Devuelvelo como codigo Python listo para pegar en el decorador.
```

## 5) Cierre (5 min)

Que decir (literal):

"Hoy cerramos el ciclo completo de una API usable: contrato CRUD, validacion confiable y documentacion que evita friccion."

"Si su API valida bien pero no se entiende, falla adopcion. Si se entiende pero no valida, falla confiabilidad. Necesitamos ambas."

Checklist final en vivo:

```bash
curl -s http://127.0.0.1:8000/contacts
curl -s http://127.0.0.1:8000/docs
curl -s http://127.0.0.1:8001/docs
```

## 6) Preguntas de chequeo rapidas

- Cuando usarias PATCH en lugar de PUT para una actualizacion?
- Que ventaja concreta da `response_model` respecto a devolver diccionarios sin filtrar?
- Que significa un 422 en FastAPI y por que mejora la calidad del backend?
- Que elementos minimos debe incluir la documentacion de un endpoint para que otro equipo lo use sin dudas?

## 7) Plan de contingencia

Si falla la demo principal:

- Opcion A: usar solo un archivo `main.py` minimo con GET y POST, dejando PATCH como lectura guiada.
- Opcion B: si falla uvicorn por entorno, mostrar codigo y ejecutar solo validaciones de Pydantic en REPL Python.
- Opcion C: si hay poco tiempo, omitir Bloque D practico y hacer cierre conceptual con checklist de calidad de documentacion.

Comandos de respaldo:

```bash
python3 -m pip install --upgrade pip
pip install fastapi "uvicorn[standard]"
python3 -c "from pydantic import BaseModel; print('pydantic ok')"
```

## 8) Mapa de origen (temas usados)

Esta guia se construyo a partir de:

- `building_a_python_api.json`: CRUD, codigos HTTP, flujo request/response.
- `validating_and_serializing_api_data_with_pydantic.json`: modelos de entrada/salida, 422, endpoint completo.
- `api_documentation.json`: documentacion clara, antipatrones y uso de OpenAPI/Swagger.
