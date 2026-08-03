# Guía Docente Completa: Clase 34 - Gestión de Sesiones en Frontend

Clase online para 60-75 minutos.
Documento para profesor: incluye objetivo, agenda, guion literal y ejemplos para explicar cómo una app frontend mantiene, restaura y destruye la sesión de un usuario de forma segura.

## 1) Objetivo de la clase

Al finalizar, el estudiante podrá:

- Explicar qué es una sesión en una aplicación web.
- Diferenciar mecanismos de autenticación de estrategias de almacenamiento.
- Entender el ciclo de vida de la sesión: inicio, continuidad y destrucción.
- Implementar el concepto de hidratación de sesión al arrancar una app.
- Entender por qué las rutas protegidas requieren verificación real y no solo ocultar UI.
- Diseñar manejo básico de expiración de token y cierre de sesión automático.

## 2) Agenda sugerida (60-75 min)

Ruta base de 70 minutos:

- Apertura y problema del estado en web: 8 min
- Bloque A: qué es una sesión y por qué importa: 10 min
- Bloque B: ciclo de vida de la sesión y memoria de sesión: 12 min
- Bloque C: mecanismos de autenticación vs almacenamiento: 12 min
- Bloque D: tokens, route guards e hidratación: 18 min
- Cierre y preguntas: 10 min

Si tienes 75 min:

- Añade una práctica guiada con un componente PrivateRoute y un caso de token expirado.

Si tienes 60 min:

- Reduce la comparación de mecanismos de autenticación y enfócate en hidratación y guards.

## 3) Preparación docente

Checklist:

- Tener claro que HTTP es sin estado.
- Poder mostrar ejemplos de localStorage, sessionStorage y header Bearer.
- Tener un flujo mental de login, recarga de página, validación del token y logout.

## 4) Guion docente detallado

## Apertura (8 min)

Qué decir (literal):

"La web funciona sobre HTTP, y HTTP no recuerda nada por sí mismo. Cada request llega como si fuera nueva. Entonces, si una app parece recordarte, es porque alguien gestionó sesión por encima de ese protocolo."

"Hoy no vamos a tratar autenticación como una pantalla de login, sino como un sistema de estado que la app mantiene y sincroniza."

## Bloque A - Qué es una sesión y por qué importa (10 min)

### A1. Definición de sesión (4 min)

Qué decir (literal):

"Una sesión es la forma en que la aplicación mantiene continuidad entre interacciones separadas. Sin eso, cada recarga sería como empezar desde cero."

Ejemplos del material:

- Carrito de compras.
- Preferencias de usuario.
- Estado autenticado.

### A2. Sesión no es lo mismo que autenticación (3 min)

Qué decir (literal):

"Autenticación verifica identidad. La sesión mantiene el estado relacionado con esa identidad entre solicitudes."

### A3. Impacto en experiencia y seguridad (3 min)

Puntos a enfatizar:

- Evita logins repetidos.
- Permite continuidad entre páginas.
- Exige validar y limpiar bien el estado.

## Bloque B - Ciclo de vida de la sesión y memoria de sesión (12 min)

### B1. Inicio, continuidad y destrucción (6 min)

Qué decir (literal):

"Toda sesión tiene un ciclo de vida. Empieza, se mantiene por un tiempo y finalmente termina, ya sea por logout o por expiración."

Ejemplo inicial:

```javascript
function initializeSession() {
  if (!localStorage.getItem('session_initialized')) {
    localStorage.setItem('session_initialized', Date.now());

    fetch('/api/session/start', { method: 'POST' })
      .then(response => response.json())
      .then(data => localStorage.setItem('session_token', data.token));
  }
}
```

### B2. Memoria de sesión (6 min)

Explica:

- Almacenamiento temporal durante una pestaña.
- Almacenamiento que sobrevive recargas.
- Relación entre estado UI y persistencia mínima.

Qué decir (literal):

"No todo dato de sesión merece persistencia larga. Parte del trabajo es decidir qué vive solo en memoria, qué vive en storage y qué debe quedar solo en el backend."

## Bloque C - Mecanismos de autenticación vs almacenamiento (12 min)

### C1. Mecanismo no es almacenamiento (4 min)

Qué decir (literal):

"JWT, Basic Auth u OAuth describen cómo te autenticas. localStorage, sessionStorage y cookies describen dónde guardas el estado o el token. Son decisiones distintas."

### C2. Ejemplo de Basic Auth (3 min)

```javascript
const username = 'user123';
const password = 'passw0rd';
const basicAuthToken = btoa(`${username}:${password}`);

fetch('https://api.example.com/data', {
  headers: {
    Authorization: `Basic ${basicAuthToken}`
  }
});
```

### C3. Estrategias de almacenamiento (5 min)

Comparativa docente:

- localStorage: persiste entre recargas.
- sessionStorage: vive por pestaña/sesión de navegador.
- cookies httpOnly: reducen exposición al JavaScript del cliente.

Ejemplo de hidratación desde localStorage:

```javascript
useEffect(() => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    fetch('/api/validate-token', {
      headers: { Authorization: `Bearer ${token}` }
    }).then(res => {
      if (!res.ok) {
        localStorage.removeItem('auth_token');
      }
    });
  }
}, []);
```

## Bloque D - Tokens, route guards e hidratación (18 min)

### D1. Bearer token y validación (4 min)

Qué decir (literal):

"El token no debe asumirse válido solo porque existe en el navegador. Debe verificarse con el backend."

Formato clave:

```http
Authorization: Bearer <token>
```

### D2. PrivateRoute y protección real (5 min)

Ejemplo:

```jsx
import { Navigate } from 'react-router-dom';

function PrivateRoute({ children, token }) {
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}
```

Qué decir (literal):

"Un guard de ruta es mejor que esconder enlaces, pero sigue necesitando verificación del backend. Si solo confías en la UI, la seguridad es débil."

### D3. Hidratación de sesión al iniciar la app (5 min)

Qué decir (literal):

"Cuando la app arranca, no basta con leer un token. Hay que restaurar el estado de forma segura: leerlo, validarlo, cargar al usuario si sigue siendo válido y limpiar si ya expiró."

### D4. Expiración y cierre automático (4 min)

Ejemplo de manejo de 401:

```javascript
fetch('/api/protected', {
  headers: { Authorization: `Bearer ${token}` }
}).then(res => {
  if (res.status === 401) {
    localStorage.removeItem('auth_token');
    window.location.href = '/login?sessionExpired=true';
  }
  return res.json();
});
```

Punto docente:

- Limpiar token.
- Limpiar estado del usuario.
- Redirigir con mensaje claro.

## 5) Flujo de demo sugerido

1. Login guarda token.
2. Recarga de página.
3. useEffect intenta restaurar sesión.
4. Backend valida token.
5. Si falla, se limpia y se manda al login.

## 6) Preguntas de chequeo

- ¿Por qué HTTP necesita un mecanismo adicional para recordar al usuario?
- ¿Qué diferencia hay entre JWT y localStorage?
- ¿Qué debería pasar al arrancar una app si encuentra un token guardado?
- ¿Por qué ocultar botones no protege realmente una ruta?
- ¿Qué pasos mínimos debe hacer la app ante un 401?

## 7) Cierre sugerido

Qué decir (literal):

"Una sesión frontend bien gestionada no es solo comodidad. Es una combinación de continuidad, validación y limpieza correcta del estado."

"La aplicación madura no solo inicia sesión; sabe restaurarla, verificarla y destruirla cuando corresponde."
