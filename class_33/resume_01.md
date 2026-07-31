# Resumen de la clase 33

Este resumen está basado en el contenido de los JSON del scraper para la clase 33 y está pensado para usarlo como guía de clase.

## Objetivo de la clase

Explicar los fundamentos de la autenticación, la seguridad de las contraseñas y el uso de JWT como base para proteger rutas y recursos en una API.

## Cómo desarrollar la clase

1. Empezar por la diferencia entre autenticación y autorización, con un ejemplo simple de acceso a un recurso.
2. Explicar por qué las contraseñas deben manejarse de forma segura y por qué no deben guardarse en texto plano.
3. Introducir los métodos de autenticación y el concepto de autenticación basada en token.
4. Explicar la estructura de un JWT y cómo se usa para identificar a un usuario.
5. Mostrar cómo se relaciona esto con OAuth, el login social y la autenticación multifactor.
6. Cerrar con el concepto de rutas protegidas y los errores que conviene evitar.

## Ejemplo práctico para explicar

Un ejemplo útil es un flujo de login en el que el usuario entrega credenciales, el sistema valida la identidad y luego entrega un token que permite acceder a recursos protegidos.

## Puntos clave para enfatizar

- La autenticación responde a “quién eres”, mientras que la autorización responde a “qué puedes hacer”.
- Las contraseñas seguras y la encriptación son la base de la seguridad.
- Un JWT permite llevar identidad y permisos de forma portable.
- La seguridad real requiere más que un token: también hay que proteger rutas y manejar expiración y almacenamiento adecuado.

## Cierre sugerido

Pedir a los alumnos que expliquen con sus palabras por qué un sistema puede autenticarse pero no estar autorizado a acceder a todo.
