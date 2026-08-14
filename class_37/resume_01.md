# Guia Docente Constructiva: Class 37
## Bases de datos, SQL y Supabase aplicados a auditoria de datos

Sesion recomendada: 60-75 minutos.
Proposito: transformar tres modulos en una clase accionable, con razonamiento y practica guiada.

## 1) Enfoque pedagogico de esta version

Esta guia no resume leccion por leccion. Reorganiza el contenido en decisiones docentes:

- Que idea desbloquea aprendizaje real.
- Que error frecuente aparece en clase.
- Que ejemplo guiado permite corregir ese error.
- Como conectar tecnica con el proyecto EduTrack.

## 2) Objetivos de aprendizaje

Al final de la sesion, el estudiante deberia poder:

- Elegir entre enfoque documental y relacional con un criterio explicable.
- Ejecutar consultas SQL de lectura y modificacion con seguridad.
- Interpretar agregaciones cuando existen valores NULL.
- Operar una base remota con Supabase desde SQL Editor y Python.
- Descomponer el proyecto EduTrack en pasos verificables.

## 3) Estructura de clase (60-75 min)

- Apertura: 5 min
- Bloque 1. Decision de modelo de datos: 12 min
- Bloque 2. SQL seguro para operar datos: 18 min
- Bloque 3. Supabase remoto y validacion tecnica: 12 min
- Bloque 4. Taller guiado de auditoria EduTrack: 15 min
- Cierre y chequeo: 5-10 min

## 4) Analisis constructivo por bloque

## Bloque 1. Decision de modelo (TinyDB vs relacional)

Fuente integrada: modulo de panorama de bases de datos.

Analisis constructivo:

- Fortalece pensamiento de arquitectura temprana (no solo sintaxis).
- Riesgo en clase: elegir tecnologia por familiaridad y no por tipo de pregunta.
- Intervencion docente: usar escenario y justificar eleccion en voz alta.

Comparacion guiada para proyectar:

- TinyDB/documental:
  - Flexible para documentos tipo JSON.
  - Menor friccion para prototipos y aprendizaje.
  - Menos natural cuando necesito consistencia entre entidades relacionadas.
- Relacional:
  - Estructura por tablas con esquema y claves.
  - SQL potente para filtrar, agrupar y reportar.
  - Adecuada para auditorias con reglas de negocio y trazabilidad.

Guion literal breve:

"TinyDB sirve para arrancar rapido con documentos. En cuanto negocio pide trazabilidad entre estudiantes, cursos e inscripciones, relacional gana por claridad y control."

Ejemplo guiado 1 (lenguaje natural):

- Caso A: "guardar borradores sueltos de notas" -> documental.
- Caso B: "auditar pagos e inscripciones por categoria" -> relacional.
- Pregunta al grupo: "que consulta de negocio seria dificil en el caso A?"

## Bloque 2. SQL seguro para operar datos

Fuente integrada: modulo de fundamentos SQL (CRUD, WHERE, filtros, GROUP BY, NULL).

Analisis constructivo:

- Fortalece disciplina operativa: leer antes de modificar.
- Riesgo en clase: escribir UPDATE/DELETE sin delimitar impacto.
- Intervencion docente: regla fija "SELECT espejo" antes de cambios.

Regla de oro para clase:

- Toda consulta de cambio (UPDATE/DELETE) debe tener una version SELECT con la misma condicion WHERE.

Ejemplo guiado 2 (paso a paso SQL):

```sql
-- Paso 1: inspecciono filas objetivo
SELECT *
FROM enrollments
WHERE instructor IS NULL;

-- Paso 2: aplico cambio solo si el paso 1 es correcto
UPDATE enrollments
SET instructor = 'Pending assignment'
WHERE instructor IS NULL;
```

Ejemplo guiado 3 (NULL y agregacion):

```sql
SELECT
  category,
  COUNT(*) AS total_inscripciones,
  COUNT(monthly_fee_paid) AS con_pago_registrado,
  AVG(completion_percentage) AS promedio_completado
FROM enrollments
GROUP BY category;
```

Punto de analisis para discutir:

- `COUNT(*)` cuenta filas.
- `COUNT(columna)` ignora NULL.
- Conclusiones de negocio cambian si se interpreta mal esa diferencia.

## Bloque 3. Supabase remoto y validacion tecnica

Fuente integrada: modulo de PostgreSQL remoto con Supabase.

Analisis constructivo:

- Fortalece paso de teoria a entorno real de trabajo remoto.
- Riesgo en clase: culpar a Python cuando el problema es configuracion.
- Intervencion docente: checklist de depuracion por capas.

Checklist guiado de depuracion:

1. Variables de entorno cargadas (`SUPABASE_URL`, `SUPABASE_KEY`).
2. Conexion creada con `create_client`.
3. Tabla y columnas existen.
4. Permisos/politicas (incluyendo RLS) no bloquean la operacion.

Ejemplo guiado 4 (Python minimo):

```python
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

result = supabase.table("tasks").select("title, done").eq("done", False).execute()
print(result.data)
```

Guion literal breve:

"En remoto, la calidad no esta solo en la query: tambien esta en como verificamos entorno, permisos y datos de entrada."

## Bloque 4. Taller guiado de auditoria EduTrack

Fuente integrada: brief del proyecto `edutrack-data-audit-sql`.

Analisis constructivo:

- Fortalece pensamiento de entrega profesional, no solo ejecucion tecnica.
- Riesgo en clase: alumno hace queries aisladas sin narrativa de hallazgos.
- Intervencion docente: separar trabajo en 4 tandas y documentar evidencia.

Ruta guiada para taller corto:

1. Setup y validacion:
  - Importar `edutrack.sql`.
  - Verificar `SELECT * FROM enrollments LIMIT 5;`.
2. Lectura y filtrado:
  - bajo progreso,
  - instructor NULL,
  - top no aprobados,
  - rango temporal.
3. Correccion de datos:
  - INSERT faltante,
  - UPDATE instructor,
  - DELETE `@test.com` con SELECT espejo previo.
4. Agregacion e informe:
  - GROUP BY,
  - HAVING,
  - SUM y AVG,
  - reporte en `analysis_report.md`.

Ejemplo guiado 5 (control antes de borrar):

```sql
-- Verificacion previa
SELECT *
FROM enrollments
WHERE email LIKE '%@test.com';

-- Eliminacion despues de validar
DELETE FROM enrollments
WHERE email LIKE '%@test.com';
```

## 5) Preparacion minima docente

Comandos:

```bash
python3 --version
python3 -m pip --version
python3 -m pip install supabase python-dotenv
```

## 6) Preguntas de chequeo (salida)

- Cuando TinyDB seria suficiente y cuando ya no?
- Por que un SELECT espejo reduce riesgo en UPDATE/DELETE?
- Que diferencia practica hay entre WHERE y HAVING?
- Como explicarias a negocio una tabla de resultados con NULL?
- Que debe contener `analysis_report.md` para que sea util al equipo no tecnico?

## 7) Plan de contingencia

Si falla Supabase:

- Continuar con SQL en pizarra/editor local conservando el flujo de validacion.
- Mantener foco en criterio de decision y seguridad de cambios.

Si falla el script Python:

- Mostrar solo SQL Editor y checklist de diagnostico.
- Cerrar con mini retro: "que capa fallo y como lo sabemos?"

## 8) Cierre sugerido (literal)

"Hoy no practicamos solo comandos: practicamos criterio. Ese criterio es lo que evita errores de datos cuando el proyecto crece."

"Tu consulta no termina al ejecutarse. Termina cuando puedes explicar su impacto y dejar evidencia clara en el informe."
