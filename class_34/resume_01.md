# Resumen de la clase 34

Este resumen está basado en el contenido de los JSON del scraper para la clase 34 y está pensado para usarlo como guía de clase.

## Objetivo de la clase

Explicar cómo las aplicaciones frontend gestionan la sesión del usuario, cómo se mantiene el estado de autenticación y cómo se protegen las rutas o pantallas sensibles.

## Cómo desarrollar la clase

1. Empezar por definir qué es una sesión y por qué es importante en una app web.
2. Explicar el ciclo de vida de la sesión: inicio, mantenimiento, expiración y cierre.
3. Diferenciar entre mecanismos de autenticación y estrategias de almacenamiento.
4. Introducir el concepto de token de sesión y su relación con el estado del frontend.
5. Mostrar cómo localStorage o otras estrategias de almacenamiento influyen en la experiencia del usuario.
6. Cerrar con el tema de rutas protegidas, hidratación de sesión al arrancar la app y limpieza al cerrar sesión.

## Ejemplo práctico para explicar

Un ejemplo claro es una app que permite entrar con usuario y contraseña, conserva la sesión al recargar la página y muestra una ruta protegida solo si el usuario sigue autenticado.

## Puntos clave para enfatizar

- La sesión permite que la app recuerde que un usuario está autenticado.
- El estado de sesión debe gestionarse con cuidado para que no haya incoherencias.
- Los tokens y su almacenamiento son clave para la experiencia y la seguridad.
- Las rutas protegidas ayudan a controlar el acceso a secciones sensibles.

## Ejemplo de código

El JSON de la clase muestra un ejemplo de manejo de sesión y token en frontend:

```javascript
fetch('/api/protected', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(res => {
  if (res.status === 401) {
    localStorage.removeItem('auth_token');
    window.location.href = '/login?sessionExpired=true';
  }
  return res.json();
});
```

## Qué decir en clase

Explicar que la sesión no es solo “estar logueado”, sino un estado que debe mantenerse y limpiarse correctamente.

## Qué preguntar después

¿Qué debería pasar si la app detecta que el token ya no es válido al arrancar?

## Cierre sugerido

Pedir a los alumnos que expliquen qué pasaría si la sesión no se hidrata correctamente al iniciar la aplicación.
