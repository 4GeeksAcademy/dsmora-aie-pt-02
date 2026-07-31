# Guía Docente Completa: Class 32 - Almacenamiento de Información con TinyDB, Pydantic y Seeders

Clase online para 60-75 minutos.
Documento para profesor: incluye guion literal, comandos exactos y prompts completos. El profesor puede saltarse bloques sin perder continuidad.

## 1) Objetivo de la clase

Al finalizar, el estudiante podrá:

- Explicar por qué guardar datos solo en memoria rompe la confiabilidad de una API.
- Implementar persistencia básica con TinyDB y operaciones CRUD esenciales.
- Aplicar validación con Pydantic antes de insertar o actualizar datos.
- Ejecutar un seeder para poblar datos iniciales consistentes en desarrollo.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y contexto: 5 min
- Bloque A: de memoria volátil a persistencia: 12 min
- Bloque B: CRUD con TinyDB (insertar, buscar, actualizar, eliminar): 16 min
- Bloque C: capa de esquema con Pydantic y antipatrones: 15 min
- Bloque D: integración en endpoint FastAPI + seeders: 12 min
- Cierre + checklist + Q&A: 5 min

Si tienes 75 min:

- Añade 10 min de práctica guiada para que cada estudiante agregue un endpoint de búsqueda por email y corra su seeder.

Si tienes 60 min:

- Recorta parte de Bloque D (deja solo demo del profesor) y mueve preguntas de seeders a tarea.

## 3) Preparación docente (antes de clase)

Checklist técnico:

- Python 3.10+ disponible.
- pipenv disponible (o virtualenv como alternativa).
- Terminal abierta en la carpeta del proyecto.

Comandos de verificación previa:

```bash
python3 --version
pipenv --version
mkdir -p class_32/demo_persistence && cd class_32/demo_persistence
```

Instalación para demo:

```bash
pipenv --python 3.12
pipenv install tinydb fastapi "uvicorn[standard]" pydantic email-validator
```

## 4) Guion docente detallado (con texto literal)

## Apertura (5 min)

Qué decir (literal):

"Hoy vamos a resolver un problema real de backend: aplicaciones que olvidan todo al reiniciar el servidor."

"La meta es pasar de datos en memoria a persistencia confiable usando TinyDB, y mantener calidad con Pydantic y seeders."

## Bloque A - De memoria volátil a persistencia (12 min)

### A1. Concepto rápido (4 min)

Qué decir (literal):

"Una lista en Python es rápida, pero vive dentro del proceso. Si el proceso muere, los datos mueren."

"Persistencia significa que los datos sobreviven reinicios. Esa es la diferencia entre un ejercicio y una aplicación útil para usuarios."

### A2. Demo guiada (4 min)

Ejecuta:

```bash
cd class_32/demo_persistence
pipenv run python - <<'PY'
contacts = []
contacts.append({'name': 'Ana', 'email': 'ana@mail.com'})
print('Antes de reiniciar proceso:', contacts)
PY

pipenv run python - <<'PY'
contacts = []
print('Nuevo proceso, lista en memoria:', contacts)
PY
```

Qué decir (literal):

"Acabamos de mostrar por qué no basta memoria RAM: cada ejecución comienza de cero."

### A3. Mini práctica (4 min)

Prompt exacto sugerido:

```text
Actúa como instructor backend. Explícame en lenguaje simple la diferencia entre datos en memoria y datos persistentes, con un ejemplo de API de contactos.
```

## Bloque B - CRUD con TinyDB (16 min)

### B1. Insertar y guardar registros (5 min)

Ejecuta:

```bash
cd class_32/demo_persistence
cat > tinydb_crud.py <<'PY'
from tinydb import TinyDB, Query

# TinyDB crea/abre un archivo JSON local
DB_FILE = 'contacts.json'
db = TinyDB(DB_FILE)

# Limpiamos para demo reproducible
db.truncate()

# Create
id_ana = db.insert({'name': 'Ana', 'email': 'ana@mail.com', 'age': 21, 'city': 'Madrid'})
id_luis = db.insert({'name': 'Luis', 'email': 'luis@mail.com', 'age': 17, 'city': 'Lima'})
print('IDs insertados:', id_ana, id_luis)

# Read
Contact = Query()
adults = db.search(Contact.age >= 18)
print('Mayores de edad:', adults)

# Update
db.update({'city': 'Barcelona'}, Contact.name == 'Ana')
print('Ana actualizada:', db.search(Contact.name == 'Ana'))

# Delete
db.remove(Contact.name == 'Luis')
print('Datos finales:', db.all())
PY

pipenv run python tinydb_crud.py
```

Qué decir (literal):

"TinyDB nos da persistencia en archivo JSON sin montar un servidor de base de datos."

"El flujo mínimo de una API real es CRUD: crear, leer, actualizar y eliminar."

### B2. Búsqueda y filtrado con Query (6 min)

Qué decir (literal):

"El objeto Query permite filtrar con operadores comparables a SQL mentalmente, pero en sintaxis Python."

"Si el esquema está desordenado, estas búsquedas se vuelven frágiles. Por eso después agregamos validación."

Prompt exacto sugerido:

```text
Genera 4 ejemplos de filtros TinyDB con Query para una colección de contactos: igualdad por email, mayores de 18, ciudad distinta de Madrid y combinación AND por edad y ciudad.
```

### B3. Validación rápida del bloque (5 min)

Checklist:

- Existe el archivo contacts.json después de ejecutar el script.
- Se ven resultados de búsqueda y actualización en consola.
- El registro eliminado ya no aparece en db.all().

## Bloque C - Pydantic como capa de esquema + antipatrones (15 min)

### C1. Antipatrón: insertar sin validar (5 min)

Qué decir (literal):

"TinyDB es flexible y acepta casi cualquier diccionario. Esa flexibilidad sin control causa caos de campos inconsistentes."

"Si hoy guardas email y mañana guardas correo, luego tus queries fallan silenciosamente."

### C2. Demo con modelo Pydantic (6 min)

Ejecuta:

```bash
cd class_32/demo_persistence
cat > validate_and_store.py <<'PY'
from pydantic import BaseModel, EmailStr, ValidationError
from tinydb import TinyDB

class Contact(BaseModel):
    name: str
    email: EmailStr
    age: int
    city: str


db = TinyDB('contacts_validated.json')
db.truncate()

raw_ok = {'name': 'Ana', 'email': 'ana@mail.com', 'age': 21, 'city': 'Madrid'}
raw_bad = {'name': 'Luis', 'correo': 'luis@mail.com', 'age': 'diecisiete', 'city': 'Lima'}

for item in [raw_ok, raw_bad]:
    try:
        contact = Contact(**item)
        db.insert(contact.model_dump())
        print('Insertado:', contact.model_dump())
    except ValidationError as e:
        print('Error de validación:')
        print(e)

print('Persistidos válidos:', db.all())
PY

pipenv run python validate_and_store.py
```

Qué decir (literal):

"Pydantic convierte una base flexible en un flujo confiable: si el dato es inválido, no entra."

"Validar antes de persistir reduce errores acumulados y mantiene tus endpoints predecibles."

### C3. Prompt de refuerzo (4 min)

Prompt exacto sugerido:

```text
Actúa como mentor Python. Reescribe este flujo para que toda inserción en TinyDB pase por un modelo Pydantic Contact con validación de email y edad entera.
```

## Bloque D - FastAPI con TinyDB + Seeder (12 min)

### D1. Endpoint mínimo persistente (7 min)

Ejecuta:

```bash
cd class_32/demo_persistence
cat > main.py <<'PY'
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from tinydb import TinyDB, Query

app = FastAPI(title='Contacts API with TinyDB')
db = TinyDB('contacts_api.json')

class ContactIn(BaseModel):
    name: str
    email: EmailStr
    age: int
    city: str

@app.post('/contacts')
def create_contact(payload: ContactIn):
    doc_id = db.insert(payload.model_dump())
    return {'id': doc_id, **payload.model_dump()}

@app.get('/contacts')
def list_contacts(min_age: int | None = None):
    if min_age is None:
        return db.all()
    Contact = Query()
    return db.search(Contact.age >= min_age)
PY

pipenv run uvicorn main:app --reload --port 8010
```

En otra terminal, prueba:

```bash
curl -X POST http://127.0.0.1:8010/contacts \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana","email":"ana@mail.com","age":21,"city":"Madrid"}'

curl "http://127.0.0.1:8010/contacts?min_age=18"
```

Qué decir (literal):

"Aquí vemos el flujo completo: request JSON, validación automática con Pydantic, persistencia en TinyDB y respuesta con ID."

### D2. Seeder con pipenv (5 min)

Ejecuta:

```bash
cd class_32/demo_persistence
cat > seed.py <<'PY'
from tinydb import TinyDB
from pydantic import BaseModel, EmailStr

class Contact(BaseModel):
    name: str
    email: EmailStr
    age: int
    city: str

seed_data = [
    {'name': 'Alice', 'email': 'alice@example.com', 'age': 25, 'city': 'Bogota'},
    {'name': 'Bob', 'email': 'bob@example.com', 'age': 31, 'city': 'Quito'},
    {'name': 'Carla', 'email': 'carla@example.com', 'age': 19, 'city': 'CDMX'},
]

db = TinyDB('contacts_api.json')
db.truncate()

for row in seed_data:
    contact = Contact(**row)
    db.insert(contact.model_dump())

print(f'Seed completado: {len(seed_data)} contactos')
PY

pipenv run python seed.py
curl "http://127.0.0.1:8010/contacts"
```

Qué decir (literal):

"Seeder significa iniciar la base con datos consistentes para desarrollo, testing y demos repetibles."

## 5) Cierre (5 min)

Qué decir (literal):

"Hoy construimos un patrón universal de backend: validar, persistir, consultar y preparar datos iniciales."

"No importa la base de datos futura: este flujo mental se mantiene y escala."

Checklist final en vivo:

```bash
cd class_32/demo_persistence
ls -1 *.json
curl "http://127.0.0.1:8010/contacts"
```

## 6) Preguntas de chequeo rápidas

- ¿Qué problema concreto resuelve la persistencia frente al almacenamiento en memoria?
- ¿Por qué TinyDB puede volverse riesgoso si no agregas una capa de validación?
- ¿En qué punto del flujo FastAPI ocurre la validación de Pydantic?
- ¿Cuál es la diferencia entre un seeder y una migración?

## 7) Plan de contingencia

Si falla la demo principal:

```bash
cd class_32/demo_persistence
pipenv run python tinydb_crud.py
cat contacts.json
```

Si falla FastAPI o puerto ocupado:

```bash
pipenv run uvicorn main:app --reload --port 8011
curl "http://127.0.0.1:8011/contacts"
```

Si falla instalación de dependencias:

- Ejecutar primero la demo local de TinyDB sin API.
- Mostrar validación Pydantic con el script validate_and_store.py.
- Dejar FastAPI como bloque opcional de cierre y compartir comandos para práctica posterior.
