# Guia Docente Completa: Class 16 - APIs Externas y Comunicacion Stateless

Clase online para 60 a 75 minutos.
Version extendida con ejemplos concretos y ejecutables para cada tema explicado.

## 1) Objetivos de aprendizaje

Al finalizar, el estudiante podra:

- Explicar que es una API y como conecta frontend y backend.
- Elegir correctamente metodo HTTP segun intencion.
- Construir solicitudes completas: URL + headers + body.
- Interpretar codigos de estado y decidir que hacer en UI.
- Evitar anti patrones de autenticacion y headers faltantes.
- Pensar en modo stateless: cada request lleva todo.
- Implementar polling basico con limpieza de intervalo.

## 2) Mapa y tiempo sugerido (72 min)

- Apertura: 3 min
- Bloque A - API y ciclo request/response: 12 min
- Bloque B - Metodos HTTP y CRUD real: 12 min
- Bloque C - Headers y body con casos correctos/incorrectos: 12 min
- Bloque D - Codigos de estado y manejo de errores: 10 min
- Bloque E - Stateless y mochila completa: 10 min
- Bloque F - Ejercicio interactivo guiado: 7 min
- Bloque G - Ejercicio real aplicado con polling: 6 min

## 3) Guion docente detallado

## Apertura (3 min)

Mensaje sugerido:

"Hoy vamos a dejar de hacer fetch por intuicion y empezar a hacerlo con criterio profesional."

Preparacion:

- Consola y Network tab abiertas.
- Confirmar que todos pueden ejecutar snippets.

## Bloque A - Que es una API (12 min)

Conceptos clave:

- Frontend consume contratos.
- Backend expone recursos.
- API define como pedir y como responder.

### Ejemplo practico A1 - Leer recurso

```js
fetch("https://jsonplaceholder.typicode.com/posts/1")
  .then((res) => res.json())
  .then((post) => console.log("[POST]", post.title));
```

Que explicar:

- URL apunta al recurso.
- respuesta trae representacion del recurso.

### Ejemplo practico A2 - Parametros de consulta

```js
fetch("https://jsonplaceholder.typicode.com/comments?postId=1")
  .then((res) => res.json())
  .then((comments) => console.log("[COMMENTS_COUNT]", comments.length));
```

Que explicar:

- query params filtran resultado sin cambiar endpoint base.

## Bloque B - Metodos HTTP y CRUD (12 min)

Conceptos clave:

- GET = leer
- POST = crear
- PUT = reemplazo completo
- PATCH = update parcial
- DELETE = eliminar

### Ejemplo practico B1 - POST crear recurso

```js
fetch("https://jsonplaceholder.typicode.com/posts", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title: "Mi post", body: "Contenido", userId: 1 })
})
  .then((res) => res.json())
  .then((created) => console.log("[CREATED_ID]", created.id));
```

### Ejemplo practico B2 - PATCH parcial vs PUT completo

PATCH:

```js
fetch("https://jsonplaceholder.typicode.com/posts/1", {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title: "Titulo actualizado" })
});
```

PUT:

```js
fetch("https://jsonplaceholder.typicode.com/posts/1", {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ id: 1, title: "Nuevo", body: "Reemplazo", userId: 1 })
});
```

Que explicar:

- PATCH minimiza riesgo de sobreescritura accidental.

## Bloque C - Headers y body (12 min)

Conceptos clave:

- Content-Type comunica formato.
- Authorization comunica identidad.
- FormData no requiere setear Content-Type manual.

### Ejemplo practico C1 - Correcto con JSON y token

```js
fetch("https://api.example.com/tasks", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer abc123"
  },
  body: JSON.stringify({ title: "Practicar APIs" })
});
```

### Ejemplo practico C2 - Incorrecto (sin Content-Type)

```js
fetch("https://api.example.com/tasks", {
  method: "POST",
  body: JSON.stringify({ title: "Sin content-type" })
});
```

Resultado esperado al explicar:

- Backend puede responder 400 por no parsear el body como JSON.

### Ejemplo practico C3 - FormData correcto

```js
const fd = new FormData();
fd.append("avatar", new Blob(["demo"], { type: "text/plain" }), "avatar.txt");

fetch("https://api.example.com/upload", {
  method: "POST",
  headers: {
    "Authorization": "Bearer abc123"
  },
  body: fd
});
```

## Bloque D - Codigos de estado y errores (10 min)

Conceptos clave:

- 2xx exito.
- 4xx error del cliente.
- 5xx error del servidor.
- fetch rechaza por red, no por HTTP.

### Ejemplo practico D1 - Manejo robusto

```js
fetch("https://jsonplaceholder.typicode.com/users/999")
  .then((res) => {
    console.log("[STATUS]", res.status);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then((data) => console.log("[DATA]", data))
  .catch((err) => console.error("[ERROR]", err.message));
```

Que remarcar:

- 404 entra al then primero; el throw lo redirige a catch.

### Ejemplo practico D2 - Error de red simulado

```js
fetch("https://dominio-inexistente.ejemplo/api")
  .then((res) => res.json())
  .catch((err) => console.error("[NETWORK_ERROR]", err.message));
```

## Bloque E - Stateless y mochila completa (10 min)

Conceptos clave:

- El servidor no recuerda request anterior.
- Cada request debe incluir token + recurso + contexto.

### Ejemplo practico E1 - Error tipico 401

Incorrecto:

```js
fetch("https://api.example.com/profile");
```

Correcto:

```js
fetch("https://api.example.com/profile", {
  headers: { "Authorization": "Bearer abc123" }
});
```

### Ejemplo practico E2 - Helper buildRequest

```js
function buildRequest({ method, endpoint, token, resourceId, body }) {
  const url = resourceId ? `${endpoint}/${resourceId}` : endpoint;
  const headers = {};

  if (token) headers.Authorization = `Bearer ${token}`;
  if (body) headers["Content-Type"] = "application/json";

  return {
    method,
    url,
    headers,
    body: body ? JSON.stringify(body) : undefined
  };
}

console.log(buildRequest({
  method: "PATCH",
  endpoint: "/api/users",
  token: "abc123",
  resourceId: 42,
  body: { email: "nuevo@mail.com" }
}));
```

## Bloque F - Ejercicio interactivo guiado (7 min)

Consigna:

- Crear funcion fetchUserData(id) con these reglas:
  - log de status
  - parsear solo status 200
  - "User not found" para resto

Solucion guia:

```js
function fetchUserData(id) {
  return fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
    .then((res) => {
      console.log("[STATUS]", res.status);
      if (res.status !== 200) {
        console.log("[INFO] User not found");
        return null;
      }
      return res.json();
    })
    .then((data) => {
      if (data) console.log("[USER]", data.name);
    })
    .catch((err) => console.error("[NETWORK_ERROR]", err.message));
}
```

## Bloque G - Ejercicio real aplicado con polling (6 min)

Consigna:

- Poll cada 3 segundos.
- Authorization en cada request.
- since=lastId.
- stop para limpiar.

Solucion base:

```js
function startPolling(token, onData) {
  let lastId = 0;

  const poll = async () => {
    try {
      const res = await fetch(`/api/notifications?since=${lastId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) return;

      const data = await res.json();
      if (data.items?.length) {
        lastId = data.items[data.items.length - 1].id;
        onData(data.items);
      }
    } catch (err) {
      console.error("[POLLING_ERROR]", err.message);
    }
  };

  poll();
  const intervalId = setInterval(poll, 3000);
  return () => clearInterval(intervalId);
}
```

## 4) Banco de preguntas para clase

- Cual metodo usarias para cambiar solo el email de un usuario y por que?
- Que diferencia ves entre error HTTP y error de red en estos logs?
- Por que este request dio 401 si "ya habia login"?
- Que riesgo hay si no limpiamos el polling al salir del componente?

## 5) Errores frecuentes y correcciones

Error: usar POST para actualizar parcialmente.
Correccion:

```js
method: "PATCH"
```

Error: asumir que 404 entra automaticamente a catch.
Correccion:

```js
if (!res.ok) throw new Error(`HTTP ${res.status}`);
```

Error: olvidar Authorization despues de login.
Correccion:

```js
headers: { Authorization: `Bearer ${token}` }
```

Error: no limpiar polling.
Correccion:

```js
return () => clearInterval(intervalId);
```

## 6) Cierre (2 min)

Mensaje final sugerido:

"Cuando cada request esta bien armada, depurar deja de ser adivinanza.
Y cuando depurar es claro, escalar es mucho mas simple."

Mini tarea:

- Crear un archivo apiClient.js con:
  - helper buildRequest,
  - parseo de respuesta con control HTTP,
  - funcion de polling con stop.
