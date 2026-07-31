# Resumen de la clase 32

Este resumen está basado en el contenido de los JSON del scraper para la clase 32 y está pensado para poder usarlo como guía de clase.

## Objetivo de la clase

Explicar por qué una API necesita persistencia real y cómo introducir un sistema simple de almacenamiento con TinyDB, validación con Pydantic y datos iniciales con seeders.

## Cómo desarrollar la clase

1. Abrir con el problema de los datos en memoria: mostrar que si el proceso se reinicia, la información desaparece.
2. Introducir TinyDB como solución básica de persistencia en archivo JSON.
3. Explicar el flujo CRUD: insertar, leer, buscar, actualizar y eliminar registros.
4. Añadir Pydantic para validar la estructura de los datos antes de guardarlos.
5. Mostrar cómo integrar esto en un endpoint FastAPI.
6. Cerrar con el concepto de seeder y su utilidad para cargar datos iniciales de forma reproducible.

## Ejemplo práctico para explicar

Un ejemplo claro es una pequeña API de contactos: primero se guarda la información en memoria, luego se pasa a TinyDB y se valida con un esquema antes de almacenarla.

## Puntos clave para enfatizar

- La persistencia permite que los datos sobrevivan a reinicios.
- TinyDB ofrece una forma sencilla de guardar información sin montar una base de datos completa.
- La validación con Pydantic evita datos inconsistentes.
- Los seeders ayudan a preparar un entorno de desarrollo con datos iniciales.

## Ejemplo de código

El material del JSON muestra este ejemplo inicial de persistencia con TinyDB:

```python
from tinydb import TinyDB

db = TinyDB("db.json")
```

## Qué decir en clase

Explicar que el objetivo no es solo “guardar algo”, sino hacer que los datos sobrevivan a reinicios y puedan recuperarse después.

## Qué preguntar después

¿Qué diferencia hay entre un dato que vive en memoria y un dato que se guarda de forma persistente?

## Cierre sugerido

Preguntar si los estudiantes entienden la diferencia entre tener datos en memoria y tener datos reales guardados para una aplicación que va a usarse de forma continua.
