# Resumen de la clase 32

Este resumen está basado en el contenido de los JSON del scraper para la clase 32.

## Qué se enseña en esta clase

La clase introduce la idea de pasar de datos temporales en memoria a un modelo de persistencia más realista. El punto central es entender que una API necesita guardar información de forma durable para que los datos sobrevivan a reinicios y puedan consultarse, actualizarse o eliminarse más adelante.

## Conceptos clave

- Por qué almacenar datos es necesario en una aplicación real.
- Cómo usar TinyDB como almacenamiento local en formato JSON.
- Operaciones básicas de CRUD: insertar, leer, buscar, actualizar y eliminar registros.
- La importancia de validar datos antes de guardarlos, con Pydantic como capa de esquema.
- Los errores comunes al guardar información sin control, como datos inconsistentes o estructuras poco claras.
- La integración de TinyDB con un endpoint FastAPI.
- Qué es un seeder y cómo se usa para cargar datos iniciales de manera reproducible.

## Enfoque del resumen

La clase combina persistencia, validación y preparación de datos iniciales. En otras palabras, muestra cómo construir una base mínima de almacenamiento que sea útil para una API simple, sin perder control sobre la forma de los datos.
