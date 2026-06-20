# Guia Docente Completa: Class 15 - Flujo de Datos, Sesiones y Promesas

Clase online pensada para 60 a 75 minutos.
Version extendida con ejemplos concretos en cada concepto para explicar y codificar en vivo.

## 1) Objetivos de aprendizaje

Al finalizar, el estudiante podra:

- Explicar donde vive la data en una app React y por que importa.
- Distinguir estado local, estado compartido y estado persistido.
- Aplicar Context + reducer sin mutacion directa.
- Elegir entre LocalStorage y SessionStorage segun necesidad.
- Implementar lectura defensiva de storage.
- Manejar promesas con then/catch y con async/await.
- Diferenciar error de red vs error HTTP.
- Resolver escenarios reales con Promise.all y manejo de errores.

## 2) Mapa y tiempo sugerido (70 min)

- Apertura y contexto: 3 min
- Bloque A - Flujo de datos y arquitectura: 14 min
- Bloque B - Store, acciones y anti mutacion: 12 min
- Bloque C - Persistencia en navegador: 13 min
- Bloque D - Promesas y fetch robusto: 10 min
- Bloque E - Ejercicio interactivo guiado: 8 min
- Bloque F - Ejercicio real aplicado: 8 min
- Cierre y recap: 2 min

## 3) Guion docente detallado

## Apertura (3 min)

Mensaje sugerido:

"Hoy resolvemos 3 problemas tipicos de frontend real: perdida de estado,
persistencia mal elegida y asincronia que rompe UX."

Acciones:

- Pedir consola abierta.
- Alinear objetivo: entender, luego implementar.

## Bloque A - Flujo de datos y arquitectura (14 min)

Conceptos clave:

- El flujo de datos es una decision de diseno.
- MVC como marco mental.
- Fuente unica de verdad para evitar inconsistencias.

### Ejemplo practico A1 - Prop drilling excesivo

Que mostrar:

```jsx
function App() {
  const [user, setUser] = React.useState({ name: "Ana" });
  return <Page user={user} setUser={setUser} />;
}

function Page({ user, setUser }) {
  return <Layout user={user} setUser={setUser} />;
}

function Layout({ user, setUser }) {
  return <Header user={user} setUser={setUser} />;
}

function Header({ user, setUser }) {
  return <button onClick={() => setUser({ ...user, name: "Ana Maria" })}>{user.name}</button>;
}
```

Que explicar:

- Solo Header usa la data, pero 3 componentes intermedios la transportan.
- Esto escala mal y complica refactor.

Resultado esperado:

- El grupo identifica el problema de arquitectura antes de hablar de Context.

### Ejemplo practico A2 - Modelo mental de flujo unidireccional

Que decir en pizarra:

- Vista dispara evento.
- Evento llama accion.
- Accion actualiza estado.
- React rerenderiza vista.

Mini codigo de apoyo:

```js
const [count, setCount] = React.useState(0);
const onClick = () => setCount((prev) => prev + 1);
```

## Bloque B - Store, acciones y anti mutacion (12 min)

Conceptos clave:

- Store central para estado compartido.
- Acciones con responsabilidad unica.
- Mutacion directa = bugs dificiles.

### Ejemplo practico B1 - Reducer correcto

```js
const initialStore = () => ({ todos: ["Estudiar"] });

function storeReducer(state, action) {
  switch (action.type) {
    case "ADD_TODO":
      return {
        ...state,
        todos: [...state.todos, action.payload]
      };
    default:
      return state;
  }
}
```

Resultado esperado:

- Queda claro que el reducer siempre retorna nuevo estado.

### Ejemplo practico B2 - Anti patron de mutacion

Codigo incorrecto para discutir:

```js
function badAddTodo(state, newTodo) {
  state.todos.push(newTodo);
  return state;
}
```

Como explicarlo:

- Mutar referencias rompe previsibilidad.
- Puede haber renderes inconsistentes.

## Bloque C - Persistencia en navegador (13 min)

Conceptos clave:

- LocalStorage: persiste entre reinicios del navegador.
- SessionStorage: vive mientras la pestana siga abierta.
- Nunca guardar secretos (tokens sensibles o passwords) en storage cliente.

### Ejemplo practico C1 - Hook utilitario defensivo

```js
function getSafeSession(key, fallback) {
  try {
    const raw = sessionStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function setSafeSession(key, value) {
  sessionStorage.setItem(key, JSON.stringify(value));
}
```

Que demostrar en vivo:

- Guardar objeto.
- Corromper valor manualmente desde consola.
- Leer sin romper app gracias a fallback.

### Ejemplo practico C2 - Criterio de eleccion rapido

Casos:

- Tema visual de usuario: LocalStorage.
- Paso de formulario en visita actual: SessionStorage.
- JWT de autenticacion: no en storage cliente si puedes usar cookie httpOnly.

## Bloque D - Promesas y fetch robusto (10 min)

Conceptos clave:

- Promesas: pending, fulfilled, rejected.
- fetch no rechaza por 404/500 automaticamente.
- Hay que validar response.ok.

### Ejemplo practico D1 - then/catch correcto

```js
fetch("https://jsonplaceholder.typicode.com/users/1")
  .then((response) => {
    console.log("[STATUS]", response.status);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  })
  .then((user) => console.log("[USER]", user.name))
  .catch((error) => console.error("[ERROR]", error.message));
```

### Ejemplo practico D2 - async/await equivalente

```js
async function loadUser(id) {
  try {
    const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const user = await response.json();
    console.log("[USER]", user.name);
  } catch (error) {
    console.error("[ERROR]", error.message);
  }
}

loadUser(1);
```

### Ejemplo practico D3 - Promise.all vs secuencial

Paralelo:

```js
const ids = [1, 2, 3];

Promise.all(ids.map((id) => fetch(`https://jsonplaceholder.typicode.com/users/${id}`).then((r) => r.json())))
  .then((users) => console.log("[PARALELO]", users.map((u) => u.name)))
  .catch((err) => console.error(err.message));
```

Secuencial:

```js
async function loadSequential() {
  const result = [];
  for (const id of [1, 2, 3]) {
    const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
    result.push(await res.json());
  }
  console.log("[SECUENCIAL]", result.map((u) => u.name));
}

loadSequential();
```

## Bloque E - Ejercicio interactivo guiado (8 min)

Enunciado:

- Completar fetchUserData(id) con then/catch.
- Requisitos:
  - Log de status.
  - Parsear JSON solo status 200.
  - Mensaje user not found si no existe.

Plantilla para estudiantes:

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
      if (data) console.log("[DATA]", data);
    })
    .catch((err) => console.error("[NETWORK_ERROR]", err.message));
}
```

## Bloque F - Ejercicio real aplicado (8 min)

Escenario:

- Mini onboarding de 2 pasos persistido en SessionStorage.

Solucion base:

```js
function saveOnboarding(state) {
  sessionStorage.setItem("onboarding", JSON.stringify(state));
}

function loadOnboarding() {
  const raw = sessionStorage.getItem("onboarding");
  return raw ? JSON.parse(raw) : { currentStep: 1, name: "" };
}

function resetOnboarding() {
  sessionStorage.removeItem("onboarding");
}

let state = loadOnboarding();
state = { ...state, name: "Ana", currentStep: 2 };
saveOnboarding(state);
console.log("[RESTORED]", loadOnboarding());
resetOnboarding();
```

Resultado esperado:

- Al recargar, se conserva paso y nombre.
- Con reset vuelve a estado inicial.

## 4) Banco de preguntas para dinamizar clase

- Que diferencia hay entre dato global y dato local en este componente?
- Si el usuario cierra pestana, que se mantiene y que no?
- Por que este 404 no entro al catch?
- En este caso conviene Promise.all o secuencial? Por que?

## 5) Errores frecuentes y correccion inmediata

Error: fetch con 404 sin validar response.ok.
Correccion:

```js
if (!response.ok) throw new Error(`HTTP ${response.status}`);
```

Error: catch vacio.
Correccion:

```js
.catch((err) => console.error("[ERROR]", err.message));
```

Error: mutar estado directo.
Correccion:

```js
return { ...state, items: [...state.items, newItem] };
```

## 6) Cierre (2 min)

Mensaje final sugerido:

"Si dominas flujo de datos, persistencia correcta y asincronia robusta,
tu frontend deja de ser fragil y empieza a ser mantenible."

Micro tarea:

- Tomar una app anterior y aplicar:
  - una store clara,
  - un helper defensivo de storage,
  - y un fetch con manejo HTTP + red.
