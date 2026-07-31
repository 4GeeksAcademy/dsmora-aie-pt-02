# Resumen de la clase 35

Este resumen está basado en el contenido de los JSON del scraper para la clase 35 y está pensado para usarlo como guía de clase.

## Objetivo de la clase

Enseñar a manejar errores de forma consciente para que una aplicación siga siendo usable, clara y resistente incluso cuando algo falla.

## Cómo desarrollar la clase

1. Empezar por mostrar los puntos comunes donde fallan las aplicaciones: red, datos incompletos y entradas inesperadas.
2. Explicar la anatomía de un fallo y cómo un error puede propagarse si no se maneja.
3. Introducir try/catch/finally como herramienta para controlar errores de forma explícita.
4. Mostrar cómo tratar errores en operaciones asíncronas y en llamadas a APIs.
5. Explicar el uso de valores por defecto, encadenamiento opcional y renderizado seguro para evitar que la interfaz se rompa.
6. Cerrar con la importancia de traducir errores técnicos a mensajes claros para el usuario y de preparar componentes de error.

## Ejemplo práctico para explicar

Un caso claro es una pantalla que intenta cargar datos desde una API y debe mostrar un estado de carga, luego un mensaje de error si la petición falla, sin dejar la interfaz en blanco.

## Puntos clave para enfatizar

- Los errores no solo deben capturarse, también deben manejarse con una respuesta clara.
- Un sistema resiliente no evita todos los fallos, pero sí los gestiona bien.
- El renderizado defensivo evita que la UI se rompa con datos incompletos.
- El usuario necesita feedback claro cuando algo sale mal.

## Ejemplo de código

El archivo JSON de la clase incluye este ejemplo de manejo de errores con try/catch:

```javascript
function parseUserData(json) {
  return JSON.parse(json);
}

try {
  const user = parseUserData('invalid json');
  console.log(user.name);
} catch (error) {
  console.log('Error:', error.message);
}
```

## Cierre sugerido

Pedir a los estudiantes que identifiquen un punto de fallo en una aplicación real y propongan una forma de manejarlo de forma más robusta.
