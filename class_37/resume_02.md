# Guia Docente Extendida: Class 37 (90 min)
## Panorama de BBDD + SQL Operativo + Supabase + Proyecto de Auditoria

Esta version extendida integra los tres modulos de class_37 con foco en clase sincrona de 90 minutos.
La secuencia esta construida desde los JSON de:

- `introduction_to_databases.json`
- `fundamentals_of_sql.json`
- `using_postgresql_remotely_with_supabase.json`

Y aterriza en el proyecto:

- `edutrack_data_audit_sql_project_README.es.md`

## 1) Resultado final esperado de la sesion

Al cerrar la clase, el estudiante deberia poder:

- Explicar por que una decision de base de datos afecta calidad de producto y de reportes.
- Distinguir TinyDB (documental) de una base relacional para casos de negocio concretos.
- Ejecutar y justificar consultas SQL CRUD, filtros y agregaciones con tratamiento de NULL.
- Operar una base PostgreSQL remota con Supabase desde panel SQL y desde Python.
- Traducir un brief de auditoria (EduTrack) en plan de ejecucion tecnico y reporte legible.

## 2) Agenda de 90 minutos

- Bloque A (15 min): Mapa de bases de datos y criterio de eleccion.
- Bloque B (20 min): Modelo relacional y fundamentos SQL.
- Bloque C (20 min): Filtros complejos, agregaciones y NULL.
- Bloque D (20 min): Supabase remoto + cliente Python.
- Bloque E (10 min): Proyecto EduTrack, requisitos y plan de ataque.
- Cierre (5 min): chequeo rapido y siguientes pasos.

## 3) Preparacion docente previa

Checklist:

- Tener visible la secuencia de lecciones de los 3 JSON.
- Tener cuenta Supabase y acceso al SQL Editor.
- Tener Python 3 listo con librerias para demo.

Comandos exactos:

```bash
python3 --version
python3 -m pip --version
python3 -m pip install supabase python-dotenv
```

Validacion inicial del entorno SQL (alineado al proyecto):

```sql
SELECT * FROM enrollments LIMIT 5;
```

## 4) Guion docente por bloques

## Bloque A (15 min): Elegir bien la base de datos

Base en modulo:

- `0 El paisaje de la base de datos`
- `1 El modelo relacional`
- `2 Bases de datos de documentos`
- `2.1 Almacenes clave valor`
- `2.2 Otros tipos de bases de datos`
- `3 Elegir la base de datos correcta`

Mensaje docente central:

- La eleccion depende de forma de datos, relaciones, patron de consulta y escalado.

Comparativa concreta para clase: TinyDB vs relacional

- Modelo: TinyDB guarda documentos JSON flexibles; relacional usa tablas con esquema.
- Relaciones: TinyDB no obliga modelado relacional explicito; relacional trabaja con claves y coherencia entre tablas.
- Consulta: TinyDB prioriza simplicidad local; relacional habilita SQL declarativo para filtrar/agrupar/reportar.
- Caso de uso: TinyDB es util para aprendizaje/prototipo; relacional es preferible en auditorias como EduTrack.

Que decir (literal):

"Si el problema es solo guardar datos sueltos, un documento puede bastar. Si necesito consistencia entre entidades y reportes confiables, necesito modelo relacional."

"No elegimos base por moda, la elegimos por tipo de pregunta que negocio nos va a hacer despues."

Mini actividad (3 min):

- Dar 3 escenarios y que el grupo clasifique rapido: documental, relacional o clave-valor.

## Bloque B (20 min): Modelo relacional y SQL base

Base en modulo:

- `0 Bienvenido a sql y bases de datos relacionales`
- `1 Que es sql y como funcionan las tablas relacionales`
- `1.1 Tipos de datos y claves primarias en la practica`
- `2 Entendiendo select insert update y delete`

Foco:

- Tablas, filas, columnas, clave primaria.
- SQL declarativo: decir que datos quieres.
- CRUD seguro con columnas explicitas y filtros claros.

Demostracion SQL (exacta):

```sql
-- READ
SELECT product_name, price
FROM products
WHERE is_active = true;

-- CREATE
INSERT INTO products (product_name, price, category_id, is_active, created_at)
VALUES ('Data Audit Notebook', 39.99, 1, true, CURRENT_TIMESTAMP);

-- UPDATE
UPDATE products
SET price = 44.99
WHERE product_name = 'Data Audit Notebook';

-- DELETE seguro
DELETE FROM products
WHERE product_name = 'Data Audit Notebook' AND is_active = true;
```

Que decir (literal):

"Si no puedo explicar por que mi WHERE toca solo esas filas, no ejecuto la consulta todavia."

"La clave primaria no es burocracia: es lo que evita ambiguedad cuando un dato crece."

## Bloque C (20 min): Filtrado complejo, agregacion y NULL

Base en modulo:

- `3 Clausulas where y operadores`
- `3.1 Consultas de filtrado complejas`
- `4 Group by funciones aggregate y manejo de nulos`
- `4.1 Consultas de agrupacion y manejo de nulos`

Foco:

- Operadores y parentesis para controlar logica AND/OR.
- GROUP BY para resumen por segmento.
- Diferencia operacional entre `COUNT(*)` y `COUNT(campo)` con NULL.
- Introduccion a HAVING como filtro post-agregacion.

Demostracion SQL (exacta):

```sql
-- Filtro compuesto con parentesis
SELECT product_id, product_name, category, price
FROM products
WHERE (category = 'Clothing' AND price < 50)
   OR (category = 'Accessories' AND price BETWEEN 10 AND 30);

-- Agregacion y NULL
SELECT
  category,
  COUNT(*) AS total_rows,
  COUNT(price) AS rows_with_price,
  AVG(price) AS avg_price
FROM products
GROUP BY category;

-- Ejemplo de HAVING
SELECT category, COUNT(*) AS enrollments
FROM enrollments
GROUP BY category
HAVING COUNT(*) > 3;
```

Que decir (literal):

"COUNT(*) cuenta filas; COUNT(campo) cuenta valores no nulos. Esa diferencia cambia decisiones."

"HAVING filtra grupos ya resumidos. WHERE filtra filas antes de agrupar."

## Bloque D (20 min): Supabase remoto y cliente Python

Base en modulo:

- `0 De local a remoto`
- `1 Que es supabase`
- `1.1 Configurando tu proyecto`
- `1.2 Manejando tablas`
- `2 El cliente python de supabase`
- `2.1 Sembrando tu base de datos`
- `2.2 Leyendo y filtrando datos`
- `3 Verificacion de integracion supabase`

Foco:

- Por que pasar de local a remoto (persistencia, acceso compartido, escala).
- Flujo tecnico: `.env` -> `create_client` -> consulta -> validacion.
- Verificacion cuando falla (credenciales, permisos, RLS, nombre de tabla).

Comandos y script de demo:

```bash
cat > .env << 'EOF'
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
EOF
```

```python
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

response = supabase.table("tasks").select("title, done").eq("done", False).execute()

if getattr(response, "error", None):
    print("Error al obtener tareas:", response.error)
else:
    for task in response.data:
        print(task["title"], task["done"])
```

Que decir (literal):

"Remoto no significa complejo: significa que tus datos sobreviven y se comparten."

"Cuando falla integracion, seguimos checklist tecnico: URL, KEY, tabla, permisos y politicas."

## Bloque E (10 min): Proyecto EduTrack como cierre integrador

Base en brief del proyecto:

- Auditoria sobre `enrollments`.
- 12 consultas entre lectura, correccion y agregacion.
- Entrega en `queries.sql` y `analysis_report.md`.

Resumen de requisitos operativos:

- Importar `edutrack.sql` y validar carga.
- Detectar bajo progreso y casos incompletos (`instructor IS NULL`).
- Corregir datos (INSERT faltante, UPDATE instructor, DELETE cuentas test).
- Resumir por categoria y curso usando GROUP BY/HAVING/SUM/AVG.
- Documentar resultados reales para stakeholders no tecnicos.

Como conectar proyecto con modulos:

- Modulo 1 aporta criterio de por que relacional.
- Modulo 2 aporta lenguaje SQL para ejecutar auditoria.
- Modulo 3 aporta infraestructura remota reproducible.

Mini plan en pseudocodigo:

```text
INICIO
  Importar edutrack.sql en Supabase
  Verificar tabla enrollments

  Ejecutar consultas de lectura y filtrado
  Guardar salidas en borrador de reporte

  Validar filas objetivo con SELECT previo
  Ejecutar INSERT/UPDATE/DELETE

  Ejecutar agregaciones por categoria y curso
  Completar analysis_report.md con resultados reales
  Consolidar consultas en queries.sql
FIN
```

## 5) Prompts pedagogicos para uso en vivo (sin resolver tarea final)

Nota: el proyecto indica no usar IA para escribir la entrega final SQL del alumno.

```text
Actua como tutor de SQL orientado a verificacion.
No escribas la consulta final.
Hazme preguntas para validar si mi WHERE en un UPDATE podria afectar filas no deseadas.
```

```text
Explica con un ejemplo conceptual la diferencia entre COUNT(*) y COUNT(columna)
cuando hay NULL, y propon tres preguntas para comprobar que lo entendi.
No generes consultas del proyecto EduTrack.
```

```text
Dame una lista de chequeo para depurar una conexion Python a Supabase
cuando create_client funciona pero la lectura de tabla devuelve error.
No des credenciales ni asumas valores.
```

## 6) Evaluacion rapida en clase (5 min)

Preguntas de salida:

- Que criterio te haria elegir TinyDB frente a relacional en un proyecto pequeno?
- En que punto exacto del flujo usas SELECT antes de UPDATE o DELETE y por que?
- Que diferencia funcional hay entre WHERE y HAVING?
- Que evidencia debe incluir `analysis_report.md` para que negocio confie en los resultados?

## 7) Riesgos frecuentes y mitigacion

- Riesgo: ejecutar UPDATE/DELETE sin validacion previa.
  Mitigacion: regla fija de SELECT con misma condicion WHERE antes de modificar.

- Riesgo: mezclar resumen tecnico con hallazgos sin contexto.
  Mitigacion: separar en `analysis_report.md` cada consulta y su resultado legible.

- Riesgo: error de conexion Supabase por entorno mal cargado.
  Mitigacion: validar `.env`, URL/KEY y permisos (incluyendo RLS) antes de culpar al codigo.

## 8) Extension post-clase recomendada

A partir de `5 Evaluacion de fundamentos sql` y `6 Tu viaje sql hacia adelante`, proponer siguiente clase con:

- JOINs entre tablas relacionadas.
- Subconsultas y CTE para consultas complejas legibles.
- Funciones de ventana para ranking y analisis por particiones.
- Normalizacion e indexacion como paso hacia rendimiento.
