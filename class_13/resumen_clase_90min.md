# Resumen Integrado de Clase (90 min)
## DOM + Ejercicios DOM + SPA + React/Next.js + Organizacion Frontend (class_13)

Este resumen integra los cinco modulos de class_13 en una sola sesion de 90 minutos.
La meta es conectar manipulacion del DOM, arquitectura frontend moderna y organizacion de codigo
para que el estudiante pase de ejercicios sueltos a construccion de aplicaciones con criterio.

## 1) Resultado general esperado de la sesion

Al cierre, el grupo deberia lograr:
- Manipular el DOM con seguridad (seleccion, creacion, eliminacion y eventos).
- Resolver ejercicios practicos de dificultad progresiva sin duplicar logica.
- Explicar diferencias entre MPA y SPA, y el rol del bundling.
- Entender base de React/Next.js (componentes, App Router, renderizado).
- Organizar estructura de carpetas y modulos para escalar proyectos.

## 2) Estructura sugerida para 90 minutos

### Bloque A - Dominio practico del DOM (20 min)

Objetivo del bloque:
- Consolidar operaciones clave del DOM para interactividad inmediata.

Lo trabajado:
- Seleccion de nodos con querySelector/querySelectorAll.
- Cambios de texto, atributos y clases.
- Creacion y eliminacion de elementos.
- Eventos click/input con validaciones minimas.

### Bloque B - Taller rapido de ejercicios DOM (20 min)

Objetivo del bloque:
- Ganar velocidad de ejecucion con ejercicios cortos y repetibles.

Lo trabajado:
- Cambio de estilos por evento.
- Render de listas dinamicas.
- Agregar y remover items en una mini Todo List.
- Limpieza de estado visual y reutilizacion de funciones.

### Bloque C - Arquitectura SPA y routing (18 min)

Objetivo del bloque:
- Entender como se comporta una SPA en build y runtime.

Lo trabajado:
- Diferencia build time vs runtime.
- Comparacion MPA vs SPA.
- Navegacion con hash routing e introduccion a History API.
- Antipatrones comunes en routing y estado.

### Bloque D - Introduccion a React y Next.js (20 min)

Objetivo del bloque:
- Enlazar fundamentos de componentes con estructura real de proyecto.

Lo trabajado:
- Modelo mental de componentes en React.
- Rol de Next.js sobre React.
- Estructura App Router (layout/page/rutas anidadas).
- Criterio inicial para elegir CSR vs SSR.

### Bloque E - Organizacion frontend y cierre (12 min)

Objetivo del bloque:
- Definir reglas de estructura para evitar caos al crecer.

Lo trabajado:
- Separacion vistas vs componentes reutilizables.
- Modularizacion por feature.
- Convenciones de naming y barrel exports.
- Checklist final de calidad tecnica y mantenibilidad.

## 3) Ejemplos para clase en vivo (guion rapido por bloque)

### Ejemplo en vivo A - DOM basico con feedback visible (Bloque A)

Objetivo docente:
- Mostrar causa/efecto inmediato entre evento y cambio en pantalla.

Snippet para proyectar:
```js
const title = document.querySelector("h1");
const btn = document.querySelector("#change-title");

btn?.addEventListener("click", () => {
  if (title) title.textContent = "Titulo actualizado desde JS";
});
```

Que observar en vivo:
- Validacion de null antes de modificar nodos.
- Diferencia entre seleccionar y realmente mutar el DOM.

### Ejemplo en vivo B - Todo List incremental (Bloque B)

Objetivo docente:
- Integrar seleccion, creacion, evento y remove en un solo flujo.

Snippet para proyectar:
```js
const input = document.querySelector("#todo-input");
const addBtn = document.querySelector("#add-todo");
const list = document.querySelector("#todo-list");

addBtn?.addEventListener("click", () => {
  const text = input?.value?.trim() || "";
  if (!text || !list) return;

  const li = document.createElement("li");
  const removeBtn = document.createElement("button");
  li.textContent = text + " ";
  removeBtn.textContent = "x";
  removeBtn.addEventListener("click", () => li.remove());
  li.appendChild(removeBtn);
  list.appendChild(li);
});
```

Que observar en vivo:
- Evitar duplicacion de listeners.
- Manejar entrada vacia antes de renderizar.

### Ejemplo en vivo C - Router cliente minimo (Bloque C)

Objetivo docente:
- Entender la ilusion de navegacion sin recarga completa.

Snippet para proyectar:
```js
function renderRoute() {
  const route = window.location.hash || "#/home";
  const app = document.querySelector("#app");
  if (!app) return;

  app.textContent = route === "#/about" ? "Vista About" : "Vista Home";
}

window.addEventListener("hashchange", renderRoute);
renderRoute();
```

Que observar en vivo:
- Cambio de URL y render sin descargar un nuevo HTML.
- Punto de entrada unico para decidir vista.

### Ejemplo en vivo D - Componente React simple (Bloque D)

Objetivo docente:
- Pasar de manipular nodos manualmente a pensar en componentes.

Snippet para proyectar:
```tsx
type BadgeProps = { label: string };

export function Badge({ label }: BadgeProps) {
  return <span>{label}</span>;
}
```

Que observar en vivo:
- Reuso del componente con diferentes props.
- Separacion entre estructura de UI y datos.

### Ejemplo en vivo E - Organizacion por feature (Bloque E)

Objetivo docente:
- Aterrizar reglas de organizacion en estructura real.

Estructura para proyectar:
```text
src/
  features/
    todos/
      components/
      services/
      index.ts
    auth/
      components/
      services/
      index.ts
```

Que observar en vivo:
- Cada feature encapsula su logica.
- Imports mas limpios usando archivos index.ts.

## 4) Actividad integradora sugerida (15 min dentro de los bloques)

Caso:
- Construir una mini app de tareas con dos vistas: "Home" y "About".

Entregable minimo por equipo:
- Vista Home con lista de tareas (agregar/eliminar).
- Navegacion por hash entre Home y About.
- Estructura de carpetas propuesta para escalar a React/Next.js.

Criterios de evaluacion:
- Correcta manipulacion de DOM y eventos.
- Routing funcional sin recarga completa.
- Claridad de modularizacion y naming.

## 5) Riesgos detectados y refuerzo recomendado

- Riesgo: codificar todo en un solo archivo largo.
  Refuerzo: separar funciones de render, eventos y utilidades.
- Riesgo: confundir SPA con "muchas paginas html".
  Refuerzo: repetir modelo de documento unico + router cliente.
- Riesgo: saltar a React sin base DOM clara.
  Refuerzo: usar React como capa de abstraccion sobre conceptos ya dominados.
- Riesgo: estructura de carpetas inconsistente.
  Refuerzo: definir convencion del equipo antes de crecer features.

## 6) Distribucion final de tiempo

- Bloque A: 20 min
- Bloque B: 20 min
- Bloque C: 18 min
- Bloque D: 20 min
- Bloque E: 12 min

Total: 90 min
