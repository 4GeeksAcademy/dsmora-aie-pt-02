# Guía Docente Completa: Clase 32 - Almacenamiento de Información

Clase online para 60-75 minutos.
Documento para profesor: incluye objetivo, agenda sugerida, guion literal, ejemplos de código y una mini demo para conectar persistencia, TinyDB, Pydantic y seeders dentro de una API sencilla.

## 1) Objetivo de la clase

Al finalizar, el estudiante podrá:

- Explicar por qué guardar datos solo en memoria no sirve para una aplicación real.
- Entender qué aporta una base de datos, aunque sea una opción simple como TinyDB.
- Crear operaciones básicas de persistencia: insertar, buscar, actualizar y eliminar registros.
- Usar Pydantic como capa de validación antes de guardar datos.
- Integrar TinyDB en un endpoint de FastAPI.
- Entender qué es un seeder y cuándo conviene usarlo.

## 2) Agenda sugerida (60-75 min)

Ruta base de 65 minutos:

- Apertura y problema real: 8 min
- Bloque A: por qué almacenar datos y qué resuelve una base de datos: 10 min
- Bloque B: TinyDB y operaciones CRUD básicas: 15 min
- Bloque C: validación con Pydantic y anti-patrones: 12 min
- Bloque D: integración con FastAPI: 12 min
- Bloque E: seeders, recap y preguntas: 8 min

Si tienes 75 min:

- Añade una práctica guiada para extender el modelo Contact con nuevos campos y adaptar las búsquedas.

Si tienes 60 min:

- Reduce la demo de FastAPI a un solo endpoint POST y deja update/delete como explicación conceptual.

## 3) Preparación docente

Checklist técnico:

- Python 3.10+ disponible.
- Entorno virtual o pipenv funcionando.
- FastAPI, TinyDB y Pydantic instalables.
- Terminal abierta en la carpeta del proyecto.

Comandos de preparación sugeridos:

```bash
python3 --version
mkdir -p class_32/demo_storage
cd class_32/demo_storage
python3 -m venv .venv
source .venv/bin/activate
pip install tinydb fastapi uvicorn pydantic
```

## 4) Guion docente detallado

## Apertura (8 min)

Qué decir (literal):

"Hasta ahora muchas de nuestras APIs funcionan, pero tienen un problema serio: recuerdan datos solo mientras el servidor sigue vivo. Si el proceso se reinicia, todo desaparece."

"Hoy vamos a dar un paso importante: pasar de datos volátiles a datos persistentes. No es solo una mejora técnica; es una condición mínima para que una aplicación sea útil de verdad."

Pregunta para abrir conversación:

- ¿Qué pasaría en una app de contactos o tareas si cada reinicio borrara toda la información?

## Bloque A - Por qué almacenar datos (10 min)

### A1. Problema del almacenamiento en memoria (4 min)

Qué decir (literal):

"Guardar datos en una lista de Python es cómodo para empezar, pero no es persistencia. Es memoria temporal. Si el servidor cae o se reinicia, esa información deja de existir."

Ejemplo rápido:

```python
contacts = []

contacts.append({"name": "Ana", "email": "ana@mail.com"})
print(contacts)
```

Explicación:

- Funciona mientras el proceso sigue ejecutándose.
- No sobrevive a reinicios.
- No escala bien si varios usuarios usan la app.

### A2. Por qué no basta con guardar archivos manualmente (3 min)

Qué decir (literal):

"Un archivo JSON simple ya da persistencia, pero gestionar búsquedas, actualizaciones y consistencia a mano se vuelve incómodo muy rápido. Una base de datos te da una estructura operativa para resolver eso mejor."

Puntos a enfatizar:

- Buscar dentro de un archivo grande es costoso.
- Actualizar requiere leer y reescribir contenido.
- Si varias operaciones escriben al mismo tiempo, aparecen problemas de consistencia.

### A3. Qué aporta una base de datos (3 min)

Qué decir (literal):

"Una base de datos no es solo un lugar donde guardo cosas. Es una herramienta para organizar, consultar y modificar información de forma más confiable."

## Bloque B - TinyDB y CRUD básico (15 min)

### B1. Introducción a TinyDB (4 min)

Qué decir (literal):

"TinyDB es útil para enseñar persistencia porque no necesita servidor aparte. Guarda documentos en un archivo JSON y nos deja enfocarnos en el flujo mental de persistir datos."

Código base:

```python
from tinydb import TinyDB

db = TinyDB("contacts.json")
```

Explica:

- Si el archivo no existe, TinyDB lo crea.
- Si ya existe, lo abre y reutiliza los datos.

### B2. Insertar registros (4 min)

Código para demo:

```python
from tinydb import TinyDB

db = TinyDB("contacts.json")

contact_id = db.insert({"name": "Ana", "email": "ana@mail.com"})
print(contact_id)

db.insert_multiple([
	{"name": "Juan", "email": "juan@mail.com"},
	{"name": "Maria", "email": "maria@mail.com"}
])
```

Qué decir (literal):

"Aquí ya no estamos agregando datos a una lista efímera. Estamos escribiendo registros en un archivo persistente gestionado por TinyDB."

### B3. Buscar y filtrar datos (4 min)

Código para demo:

```python
from tinydb import TinyDB, Query

db = TinyDB("contacts.json")
Contact = Query()

ana = db.search(Contact.name == "Ana")
gmail_users = db.search(Contact.email.test(lambda value: value.endswith("mail.com")))

print(ana)
print(gmail_users)
```

Qué decir (literal):

"Persistir datos no sirve de mucho si luego no puedes encontrarlos fácilmente. Por eso las búsquedas son parte central del flujo CRUD."

### B4. Actualizar y eliminar (3 min)

Código para demo:

```python
from tinydb import TinyDB, Query

db = TinyDB("contacts.json")
Contact = Query()

db.update({"email": "ana.nueva@mail.com"}, Contact.name == "Ana")
db.remove(Contact.name == "Juan")
```

Punto docente:

- CRUD significa crear, leer, actualizar y eliminar.
- Aunque TinyDB sea simple, el patrón mental es el mismo que usarán después con otras bases de datos.

## Bloque C - Pydantic como capa de validación (12 min)

### C1. El problema de guardar datos sin esquema (5 min)

Qué decir (literal):

"TinyDB es flexible, pero esa flexibilidad tiene un costo: acepta casi cualquier diccionario. Si no validamos antes, terminamos con datos inconsistentes."

Anti-patrón:

```python
db.insert({"name": "Ana", "correo": "ana@mail.com"})
db.insert({"full_name": "Luis", "email": "luis@mail.com"})
```

Explica:

- Los nombres de campos quedan desalineados.
- Luego las búsquedas fallan o devuelven resultados incompletos.

### C2. Validar con Pydantic (7 min)

Código recomendado:

```python
from pydantic import BaseModel, EmailStr, ValidationError


class Contact(BaseModel):
	name: str
	email: EmailStr


raw_data = {"name": "Ana", "email": "ana@mail.com"}

try:
	contact = Contact(**raw_data)
	db.insert(contact.model_dump())
except ValidationError as error:
	print(error)
```

Qué decir (literal):

"Pydantic funciona como una aduana. Antes de que un dato entre a la base, comprobamos que tiene la forma correcta."

"Esto hace que la base de datos sea más limpia y que el resto de la aplicación sea más confiable."

## Bloque D - TinyDB dentro de FastAPI (12 min)

### D1. Mostrar el flujo completo (6 min)

Qué decir (literal):

"En una API real, el flujo correcto es: llega un JSON al endpoint, FastAPI lo valida con Pydantic, lo convertimos a diccionario y recién entonces lo insertamos en TinyDB."

Demo sugerida:

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from tinydb import TinyDB

app = FastAPI()
db = TinyDB("contacts.json")


class Contact(BaseModel):
	name: str
	email: EmailStr


@app.post("/contacts")
def create_contact(contact: Contact):
	contact_id = db.insert(contact.model_dump())
	return {"id": contact_id, **contact.model_dump()}
```

### D2. Ejecución del ejemplo (3 min)

Comando sugerido:

```bash
uvicorn app:app --reload
```

Qué decir (literal):

"La diferencia importante es que aquí ya no dependemos de una lista global en memoria. Cada contacto queda persistido en el archivo de TinyDB."

### D3. Pregunta de comprensión (3 min)

- ¿En qué momento del flujo se valida el dato?
- ¿En qué momento pasa a quedar persistido?

## Bloque E - Seeders y cierre conceptual (8 min)

### E1. Qué es un seeder (4 min)

Qué decir (literal):

"Un seeder es un script que llena la base de datos con datos iniciales consistentes. Sirve para desarrollar, probar y hacer demos sin tener que escribir todo a mano cada vez."

Ejemplo:

```python
from tinydb import TinyDB
from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
	name: str
	email: EmailStr


db = TinyDB("contacts.json")
db.truncate()

seed_data = [
	{"name": "Alice", "email": "alice@example.com"},
	{"name": "Bob", "email": "bob@example.com"},
	{"name": "Charlie", "email": "charlie@example.com"}
]

for item in seed_data:
	contact = Contact(**item)
	db.insert(contact.model_dump())

print("Base de datos inicializada")
```

Comando sugerido:

```bash
python seed.py
```

### E2. Recapitulación final (4 min)

Qué decir (literal):

"Hoy no solo aprendimos una librería. Aprendimos un patrón completo: validar, almacenar, consultar y preparar datos iniciales. Ese patrón se repite en casi cualquier backend real."

## 5) Mini demo integral sugerida

Si quieres hacer una sola demo compacta, crea este archivo:

```python
from tinydb import TinyDB, Query
from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
	name: str
	email: EmailStr
	age: int


db = TinyDB("contacts.json")
ContactQuery = Query()

contact = Contact(name="Ana", email="ana@mail.com", age=25)
doc_id = db.insert(contact.model_dump())
print("Insertado:", doc_id)

results = db.search(ContactQuery.age >= 18)
print("Mayores de edad:", results)

db.update({"age": 26}, ContactQuery.name == "Ana")
print("Actualizado:", db.search(ContactQuery.name == "Ana"))
```

Comandos:

```bash
python app.py
cat contacts.json
```

## 6) Preguntas de chequeo

- ¿Cuál es la diferencia entre memoria volátil y persistencia?
- ¿Por qué TinyDB puede ser una buena herramienta para aprender persistencia?
- ¿Qué problema resuelve Pydantic antes de insertar datos?
- ¿Qué ventaja tiene un seeder frente a cargar datos manualmente?
- ¿Por qué CRUD sigue siendo importante aunque cambie la tecnología de base de datos?

## 7) Errores comunes para enfatizar

- Guardar datos sin validación previa.
- Pensar que un archivo JSON manual equivale a una estrategia completa de persistencia.
- Mezclar nombres de campos distintos para el mismo dato.
- Olvidar limpiar o reinicializar datos cuando se ejecuta un seeder varias veces.

## 8) Variantes de recorte o extensión

### Versión 60 min

- Mantener solo insert, search y validación.
- Mostrar FastAPI con un único endpoint POST.
- Dejar update/delete como lectura guiada.

### Versión 75 min

- Añadir un endpoint GET por email o nombre.
- Pedir a los estudiantes que agreguen el campo city al modelo y ajusten el seeder.
- Comparar rápidamente TinyDB con una base de datos relacional que verán más adelante.

## 9) Cierre sugerido

Qué decir (literal):

"Si una aplicación no recuerda información, no importa mucho cuán bonita sea su API: sigue siendo frágil. La persistencia convierte una demo temporal en una base real para construir software útil."

"Lo que hoy hicimos con TinyDB y Pydantic es una versión pequeña de un patrón profesional que volverá a aparecer con otras bases de datos y otros frameworks."
