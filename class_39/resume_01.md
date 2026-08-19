# Guia Docente Completa: Class 39
## ORM + Evolucion de Esquema con FastAPI (SQLModel y Alembic)

Duracion objetivo: 60-75 minutos.

Fuentes usadas para esta guia:
- class_39/object_relational_mapping_the_universal_translat.json
- class_39/managing_database_evolution_with_fastapi.json
- class_39/ai-eng-milestone-backend-development_project_README.es.md
- class_39/ai-eng-inventory-management-backoffice_project_README.es.md

---

## 1) Objetivos de aprendizaje

Al cerrar la clase, el estudiante deberia poder:
- Explicar que problema resuelve un ORM y como conecta clases Python con tablas SQL.
- Definir modelos con SQLModel, incluyendo claves primarias y relaciones 1:1, 1:n y n:m.
- Ejecutar operaciones de sesion (add, commit, rollback, select con filtros).
- Explicar por que aparece el problema N+1 y como evitarlo con carga ansiosa.
- Diferenciar create_all de migraciones versionadas.
- Aplicar el flujo base de Alembic: init, revision autogenerada, inspeccion, upgrade y downgrade.
- Conectar lo anterior con los dos proyectos de inventario (backend y backoffice).

---

## 2) Agenda recomendada (70 min)

- Apertura y contexto: 5 min
- Bloque A. Entendiendo el puente ORM: 12 min
- Bloque B. Modelado y relaciones en SQLModel: 18 min
- Bloque C. Sesiones, transacciones y N+1: 12 min
- Bloque D. Migraciones con Alembic en FastAPI: 15 min
- Bloque E. Puente directo a proyectos del modulo: 6 min
- Cierre y chequeo: 2 min

Recorte a 60 min:
- Reducir 5 min del Bloque B (hacer solo 1:1 y 1:n).
- Reducir 5 min del Bloque D (explicar downgrade sin demo completa).

Extension a 75 min:
- Sumar 5 min en Bloque C para comparar consulta naive vs consulta con carga ansiosa.

---

## 3) Guion docente detallado

## Apertura (5 min)

Que decir (literal):

"Hoy vamos a conectar dos piezas que en proyectos reales van juntas: primero, como modelar y consultar datos con ORM; segundo, como evolucionar ese esquema sin romper produccion usando migraciones."

"La meta no es memorizar comandos: es entender el flujo completo que luego aplicamos al milestone de inventario."

Prompt de arranque para OpenClaw:

```text
Resumen en 5 bullets de este objetivo de clase:
1) mapear clases Python a tablas SQL,
2) definir relaciones,
3) operar sesiones de forma segura,
4) versionar cambios de esquema con Alembic,
5) conectar todo con un proyecto de inventario en FastAPI.
Usa lenguaje corto y tecnico.
```

---

## Bloque A. Entendiendo el puente ORM (12 min)

Lecciones base:
- 0 Bienvenido a orm
- 1 Entendiendo el puente orm
- 1.1 Mapeando conceptos a sql

Que decir (literal):

"Un ORM traduce entre objetos Python y tablas SQL. Clase equivale a tabla, atributo a columna, instancia a fila."

"El objetivo del ORM no es esconder SQL para siempre, sino permitir que escribamos codigo mas mantenible sin perder el control del modelo relacional."

"Si no entendemos ese mapeo, luego cuesta depurar errores de consultas y relaciones."

Mini demo de mapeo (mostrar y leer):

```python
from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=80)
    email: str = Field(unique=True)
    is_active: bool = Field(default=True)
```

Pregunta de chequeo:
- "En este modelo, cual atributo corresponde a la clave primaria y cual restriccion evita correos duplicados?"

---

## Bloque B. Modelado y relaciones en SQLModel (18 min)

Lecciones base:
- 1.2 Definiendo tu primer modelo
- 2 Explorando relaciones
- 2.1 Enlaces uno a uno y uno a muchos
- 2.2 Conexiones muchos a muchos

Que decir (literal):

"Las relaciones permiten navegar objetos relacionados sin escribir JOIN explicito en cada punto de lectura."

"El lado hijo define la foreign key; Relationship habilita navegacion Pythonica; back_populates debe estar emparejado en ambos lados."

"Para 1:1, la FK debe ser unique=True; para 1:n, el lado padre suele exponer una lista."

Ejercicio guiado en vivo (tal como aparece en la leccion):
- Definir Author, Book y Biography.
- Author tiene muchos Book (1:n).
- Author tiene una Biography (1:1 con FK unique=True).
- Crear un Author con 2 Book y 1 Biography.
- Consultar e imprimir nombre, bio y lista de titulos.

Prompt para OpenClaw (codigo de apoyo):

```text
Genera un ejemplo minimo con SQLModel para Author, Book y Biography con estas reglas:
- Relacion 1:n Author->Book.
- Relacion 1:1 Author->Biography usando FK unique=True.
- back_populates correcto en ambos lados.
- Bloque with Session(engine) que agrega 1 autor, 2 libros y 1 biografia, hace commit y luego consulta Author para imprimir nombre, bio y titulos.
No agregues framework web ni rutas, solo modelos y sesion.
```

---

## Bloque C. Sesiones, transacciones y N+1 (12 min)

Lecciones base:
- 3 Sesiones y transacciones resumen
- 3.1 Operando con sesiones
- 3.2 Gestionando registros de base de datos

Que decir (literal):

"La sesion es el area de trabajo entre nuestros objetos y la base de datos: preparamos cambios, confirmamos o revertimos."

"commit persiste; rollback deshace cambios pendientes en errores."

"El problema N+1 aparece cuando hacemos una consulta inicial y luego disparamos una consulta extra por cada elemento."

Snippet minimo para demo:

```python
from sqlmodel import Session, select

with Session(engine) as session:
    user = User(username="ana", email="ana@example.com")
    session.add(user)
    session.commit()

with Session(engine) as session:
    queried_user = session.exec(select(User).where(User.username == "ana")).first()
    print(queried_user.email)
```

Pregunta de chequeo:
- "Si falla una operacion intermedia dentro de la sesion, que accion evita dejar cambios parciales?"

---

## Bloque D. Migraciones con Alembic en FastAPI (15 min)

Lecciones base:
- 0 Bienvenido a la evolucion de la base de datos
- 1 Que son las migraciones
- 1.1 Ventajas y compensaciones de las migraciones
- 2 Introduccion a alembic
- 2.1 Configurando alembic en fastapi
- 2.2 Creando y ejecutando migraciones
- 2.3 Desafio practico de migracion

Que decir (literal):

"create_all sirve para inicializacion simple, pero no versiona cambios de esquema ni deja historial confiable para equipo."

"Una migracion tiene dos direcciones: upgrade para avanzar y downgrade para revertir."

"En equipos, migraciones son el contrato de evolucion del esquema."

Comandos exactos para demo:

```bash
uv add alembic
uv run alembic init migrations
```

```bash
uv run alembic revision --autogenerate -m "agregar telefono a usuarios"
uv run alembic upgrade head
uv run alembic downgrade -1
```

Fragmento de ejemplo para inspeccion:

```python
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('users', 'phone')
```

Prompt para OpenClaw:

```text
Explica este flujo de migraciones en formato operativo para equipo:
1) cambio en modelo,
2) alembic revision --autogenerate,
3) revisar upgrade/downgrade,
4) alembic upgrade head,
5) rollback con alembic downgrade -1.
Incluye 3 riesgos si no se revisa el archivo autogenerado.
```

---

## Bloque E. Puente directo a proyectos del modulo (6 min)

Fuentes de proyecto:
- ai-eng-milestone-backend-development
- ai-eng-inventory-management-backoffice

Que decir (literal):

"En el milestone backend se exige arquitectura de doble base: TinyDB para auth y Supabase/PostgreSQL para inventario y ordenes."

"La regla critica de negocio es que stock no se modifica directamente: solo cambia por ordenes inbound y outbound."

"En el milestone de backoffice, la interfaz debe consumir /inventory, mostrar stock actual, y renderizar errores HTTP 400 de forma legible para operaciones."

Resumen de requisitos clave del proyecto backend:
- Rutas bajo prefijo /inventory.
- Modelos ORM en SQLModel y esquemas de request/response separados.
- current_stock calculado como entradas menos salidas.
- Rechazar outbound que deja stock negativo con HTTP 400 antes de persistir.
- Guardar user_uuid del usuario autenticado en cada orden.

Resumen de requisitos clave del proyecto backoffice:
- Pagina de productos con indicador visual de stock.
- Formulario inbound con confirmacion y errores legibles.
- Formulario outbound mostrando stock actual del producto seleccionado, warning cliente y manejo de 400.
- Historial de ordenes con distincion inbound/outbound y user_uuid.
- Proteccion de rutas por autenticacion.

Mini plan en pseudocodigo para explicar al grupo:

```text
Backend:
1. Conectar TinyDB (auth) + SQLModel engine (Supabase).
2. Definir modelos de entidad inventariable + inbound + outbound.
3. Implementar calculo current_stock = sum(inbound) - sum(outbound).
4. Validar en POST outbound: si qty > stock_actual -> HTTP 400.
5. Exponer endpoints bajo /inventory.

Backoffice:
1. Crear capa API centralizada para /inventory con token.
2. Construir vista productos con stock actual.
3. Construir formulario inbound.
4. Construir formulario outbound con stock reactivo del producto.
5. Construir vista historial de ordenes.
6. Redireccionar a login si no hay autenticacion.
```

---

## 4) Comandos de clase listos para copiar

Librerias necesarias segun el contenido de esta clase:
- sqlmodel: ORM para mapear clases Python a tablas relacionales y operar sesiones.
- psycopg2-binary: driver PostgreSQL para conectar FastAPI/SQLModel con Supabase.
- alembic: sistema de migraciones versionadas (upgrade/downgrade) para evolucion de esquema.

```bash
# Preparacion del entorno backend con uv (segun brief y lecciones)
uv add sqlmodel psycopg2-binary alembic

# sqlmodel: define modelos ORM, relaciones y sesiones con sintaxis tipada.
# psycopg2-binary: driver PostgreSQL para conectar con Supabase desde SQLModel/SQLAlchemy.
# alembic: versiona cambios de esquema y permite upgrade/downgrade controlado.

# Flujo base de migraciones con Alembic usando uv
uv run alembic init migrations
uv run alembic revision --autogenerate -m "add bio column to users"
uv run alembic upgrade head
uv run alembic downgrade -1
```

```bash
# Dependencias de backoffice (segun brief)
npm install
```

---

## 5) Checklist de preparacion docente

Antes de clase:
- Confirmar que existen los 2 JSON de contenidos en class_39.
- Abrir snippets de SQLModel (modelo y sesion) para demo rapida.
- Preparar terminal con comandos de Alembic.
- Tener a mano los requisitos de ambos proyectos (backend y backoffice).

Durante clase:
- Verificar que el grupo entiende mapeo clase->tabla antes de migraciones.
- Preguntar explicitamente por diferencia create_all vs migraciones.
- Forzar el razonamiento de regla de negocio: "sin mutacion directa de stock".

Contingencia (si falla demo en vivo):
- Leer y analizar solo el archivo de migracion generado (upgrade/downgrade) sin ejecutar DB.
- Convertir la practica en pseudocodigo y validacion por pares.

---

## 6) Preguntas de comprobacion final

- Que problema exacto resuelve un ORM en este modulo?
- Donde se define la foreign key y donde va Relationship en SQLModel?
- Que diferencia operativa hay entre commit y rollback?
- Por que autogenerate no se debe ejecutar "a ciegas"?
- Que regla de negocio evita inconsistencias de stock en el proyecto?
- Que debe mostrar el formulario outbound antes de enviar una salida?

---

## 7) Cierre sugerido (literal)

"Si dominas ORM pero no versionas esquema, tu app se rompe al crecer. Si versionas esquema pero no respetas reglas de negocio, tu inventario miente. Esta clase une ambas capas para que el backend sea correcto y operable en produccion."

"Tu siguiente paso es implementar el flujo completo de inventario: modelo, reglas de stock, migraciones, y luego interfaz de backoffice consumiendo esos endpoints con manejo de errores real."
