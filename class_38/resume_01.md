# Guía Docente Constructiva: Class 38
## Gestionando Tablas Relacionales con SQL

Sesión recomendada: 60-75 minutos.
Propósito: Enseñar a diseñar, crear y consultar bases de datos relacionales con múltiples tablas conectadas mediante claves primarias y foráneas.

## 1) Enfoque pedagógico de esta versión

Esta guía reorganiza el contenido en decisiones docentes:

- Qué concepto desbloquea comprensión real de bases de datos relacionales.
- Qué error frecuente aparece al trabajar con múltiples tablas.
- Qué ejemplo guiado permite corregir ese error.
- Cómo conectar la teoría con la práctica en proyectos reales.

## 2) Objetivos de aprendizaje

Al final de la sesión, el estudiante debería poder:

- Diseñar esquemas de bases de datos con múltiples tablas relacionadas.
- Definir claves primarias y foráneas correctamente.
- Crear relaciones uno a uno, uno a muchos y muchos a muchos.
- Ejecutar consultas JOIN para combinar datos de múltiples tablas.
- Mantener la integridad referencial con restricciones ON DELETE/UPDATE.
- Realizar operaciones CRUD en tablas relacionadas.

## 3) Estructura de clase (60-75 min)

- Apertura: 5 min
- Bloque 1. Fundamentos de tablas relacionales: 12 min
- Bloque 2. Claves primarias y foráneas: 15 min
- Bloque 3. Consultas JOIN: 18 min
- Bloque 4. Integridad referencial y cascada: 10 min
- Bloque 5. Ejercicio práctico integrador: 15 min
- Cierre y chequeo: 5-10 min

## 4) Análisis constructivo por bloque

### Bloque 1. Fundamentos de tablas relacionales

Fuente integrada: Introducción a tablas relacionales.

Análisis constructivo:

- Fortalece la comprensión de por qué necesitamos múltiples tablas.
- Riesgo en clase: confundir normalización con complejidad innecesaria.
- Intervención docente: usar ejemplos cotidianos (tienda en línea, sistema de usuarios).

Conceptos clave para proyectar:

- Redundancia: datos duplicados que pueden causar inconsistencias.
- Integridad: garantizar que los datos sean correctos y consistentes.
- Atomicidad: cada columna debe contener un solo valor.

### Bloque 2. Claves primarias y foráneas

Fuente integrada: Claves primarias y foráneas.

Análisis constructivo:

- La clave primaria es el identificador único de cada registro.
- La clave foránea crea la conexión entre tablas.
- Error común: olvidar establecer la relación con REFERENCES.

Ejemplo guiado:

```sql
-- Crear tabla de usuarios
CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Crear tabla de pedidos con referencia
CREATE TABLE pedidos (
    pedido_id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(usuario_id)
);
```

### Bloque 3. Consultas JOIN

Fuente integrada: Consultas con JOIN.

Análisis constructivo:

- JOIN es la herramienta fundamental para trabajar con datos relacionados.
- INNER JOIN solo muestra registros con coincidencia en ambas tablas.
- LEFT JOIN muestra todos los registros de la tabla izquierda.

Ejemplo práctico:

```sql
-- Listar usuarios y sus pedidos
SELECT u.nombre, p.fecha_pedido
FROM usuarios u
LEFT JOIN pedidos p ON u.usuario_id = p.usuario_id;
```

### Bloque 4. Integridad referencial y cascada

Fuente integrada: Integridad referencial y cascada.

Análisis constructivo:

- ON DELETE CASCADE elimina registros hijos cuando se elimina el padre.
- ON DELETE SET NULL establece NULL en la clave foránea.
- IMPORTANTE: usar con precaución para no perder datos accidentalmente.

### Bloque 5. Ejercicio práctico integrador

Actividad:

1. Diseñar esquema para sistema de cursos (instructores, cursos, estudiantes, inscripciones).
2. Crear las tablas con relaciones correctas.
3. Resolver consultas de conteo, listado y agregación.

## 5) Errores comunes y cómo evitarlos

| Error | Solución |
|-------|----------|
| Olvidar la clave primaria | Siempre definir PRIMARY KEY en cada tabla |
| No usar NOT NULL | Establecer restricciones cuando el dato es obligatorio |
| Confundir tipos de JOIN | Explicar la diferencia con diagramas |
| No usar transacciones | Agrupar operaciones relacionadas en BEGIN/COMMIT |

## 6) Material de apoyo

- Documentación oficial de PostgreSQL sobre JOINs
- Diagramas de relación entre entidades (ERD)
- Ejemplos prácticos de esquemas de bases de datos

## 7) Conexión con el proyecto

Esta clase sienta las bases para:

- Diseñar el esquema de bases de datos del proyecto EduTrack
- Crear relaciones entre entidades (estudiantes, cursos, calificaciones)
- Implementar consultas complejas para reportes y estadísticas