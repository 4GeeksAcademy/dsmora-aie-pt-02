# Resumen Ejecutivo: Class 38
## Gestionando Tablas Relacionales con SQL

**Duración:** 60-75 minutos
**Enlace LearnPack:** https://managing-related-tables-with-sql.learn-pack.com
**Proyecto:** https://learn.4geeks.com/es/main-cohort/spain-aie-pt-2/syllabus/managing-relational-databases-with-fastapi/project/edutrack-data-audit-sql-related-tables?moduleId=2

---

## Objetivos de la Sesión

1. Comprender el diseño de bases de datos relacionales
2. Crear tablas con claves primarias y foráneas
3. Ejecutar consultas JOIN para combinar datos
4. Mantener integridad referencial con restricciones

---

## Contenido Clave

### 1. Tipos de Relaciones

| Relación | Ejemplo | Descripción |
|----------|---------|-------------|
| 1:1 | Usuario ↔ Perfil | Un registro se relaciona con uno solo |
| 1:N | Usuario → Pedidos | Un registro se relaciona con muchos |
| M:N | Pedidos ↔ Productos | Muchos registros se relacionan con muchos |

### 2. Sintaxis de Claves

```sql
-- Clave primaria
CREATE TABLE usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Clave foránea
CREATE TABLE pedidos (
    pedido_id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(usuario_id)
);
```

### 3. Tipos de JOIN

```sql
-- INNER JOIN: Solo coincidencias
SELECT u.nombre, p.pedido_id
FROM usuarios u
INNER JOIN pedidos p ON u.usuario_id = p.usuario_id;

-- LEFT JOIN: Todos los de la izquierda
SELECT u.nombre, COUNT(p.pedido_id) as total
FROM usuarios u
LEFT JOIN pedidos p ON u.usuario_id = p.usuario_id
GROUP BY u.nombre;
```

### 4. Integridad Referencial

```sql
-- ON DELETE CASCADE
CREATE TABLE detalle_pedido (
    detalle_id SERIAL PRIMARY KEY,
    pedido_id INTEGER REFERENCES pedidos(pedido_id) ON DELETE CASCADE
);

-- ON DELETE SET NULL
CREATE TABLE productos (
    producto_id SERIAL PRIMARY KEY,
    categoria_id INTEGER REFERENCES categorias(categoria_id) ON DELETE SET NULL
);
```

---

## Ejercicios Prácticos

### Ejercicio 1: Esquema de Tienda
Crear tablas para: categorías, productos, pedidos, detalle_pedido

### Ejercicio 2: Consultas con JOIN
- Listar usuarios y sus pedidos
- Encontrar productos nunca vendidos
- Calcular total gastado por usuario

### Ejercicio 3: Integridad
- Probar ON DELETE CASCADE
- Probar ON DELETE SET NULL

---

## Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "foreign key constraint fails" | Referencia a registro inexistente | Verificar que el registro padre exista |
| "duplicate key value" | Intentar insertar valor duplicado en PRIMARY KEY | Usar SERIAL o generar ID único |
| "null value not allowed" | Olvidar NOT NULL en columna obligatoria | Definir restricciones correctamente |

---

## Conexión con el Proyecto EduTrack

En el proyecto de auditoría de datos, aplicarás:

1. **Diseño de esquema:** Crear tablas para usuarios, cursos, calificaciones
2. **Relaciones:** Establecer conexiones entre entidades
3. **Consultas:** Obtener reportes combinando múltiples tablas
4. **Integridad:** Asegurar consistencia de datos

---

## Recursos Adicionales

- [Documentación PostgreSQL JOINs](https://www.postgresql.org/docs/current/tutorial-join.html)
- [Diagramas ER online](https://draw.io/)
- [Práctica SQL interactiva](https://www.sqlfiddle.com/)

---

**Siguiente clase:** Subconsultas y CTEs para consultas más complejas