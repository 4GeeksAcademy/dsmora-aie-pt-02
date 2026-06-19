# Resumen Integrado de Clase (60 min)
## DOM + SPA + React/Next.js + Organizacion Frontend (class_13)

Este resumen condensa class_13 en una sesion unica de 60 minutos.
La meta es conectar fundamentos del DOM con arquitectura SPA y una base clara
de React/Next.js, cerrando con organizacion de proyecto para alumnos en aprendizaje.

## 1) Resultado general esperado de la sesion

Al cierre, el grupo deberia lograr:
- Manipular el DOM con seguridad (seleccionar, crear, eliminar y escuchar eventos).
- Entender en palabras simples la diferencia entre MPA y SPA.
- Explicar de forma inicial que hacen React y Next.js en una app moderna.
- Organizar codigo por modulos para evitar caos al crecer.
- Resolver un mini ejercicio final en maximo 20 minutos.

## 2) Agenda sugerida para 60 minutos

- 00:00-15:00 Bloque A. DOM practico para interactividad.
- 15:00-27:00 Bloque B. De MPA a SPA (routing y bundling en lenguaje simple).
- 27:00-40:00 Bloque C. Introduccion a React y Next.js.
- 40:00-60:00 Bloque D. Mini ejercicio final integrador (20 min max).

---

## 3) Bloque A (00:00-15:00)
## DOM practico para interactividad

Conceptos importantes explicados en palabras:
- El DOM es una representacion en arbol de la pagina que JavaScript puede modificar.
- Un evento (click, input) conecta accion del usuario con cambio visual.
- Si no validas nodos o entradas, aparecen errores comunes de principiantes.

Ejemplo rapido para mostrar en vivo:

```js
const title = document.querySelector("h1");
const button = document.querySelector("#change-title");

button?.addEventListener("click", () => {
  if (!title) return;
  title.textContent = "Titulo actualizado desde JavaScript";
});
```

Check rapido antes de avanzar:
- El estudiante identifica que se selecciona y que se modifica.
- Entiende por que se valida null antes de cambiar texto.

---

## 4) Bloque B (15:00-27:00)
## De MPA a SPA sin tecnicismos innecesarios

Conceptos importantes explicados en palabras:
- MPA: cada cambio de pagina recarga todo el documento.
- SPA: la app cambia vista sin recargar el documento completo.
- Bundling: juntar y preparar archivos para que el navegador cargue mas facil.

Ejemplo minimo de routing con hash:

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

Check rapido antes de avanzar:
- El estudiante puede explicar por que cambia la vista sin recargar toda la pagina.

---

## 5) Bloque C (27:00-40:00)
## Introduccion a React y Next.js

Conceptos importantes explicados en palabras:
- React: libreria para construir UI en componentes reutilizables.
- Next.js: framework que organiza rutas, renderizado y estructura del proyecto.
- Organizacion frontend: separar vistas, componentes y utilidades para escalar.

Ejemplo basico de componente reutilizable:

```tsx
type CardProps = { title: string; description: string };

export function Card({ title, description }: CardProps) {
  return (
    <article>
      <h3>{title}</h3>
      <p>{description}</p>
    </article>
  );
}
```

Estructura simple para explicar en 1 minuto:

```text
app/
  page.tsx
  about/
    page.tsx
components/
  Card.tsx
```

---

## 6) Bloque D (40:00-60:00)
## Mini ejercicio final integrador (20 min max)

Objetivo:
- Construir una mini app de tareas con dos vistas: Home y About.

Requisitos minimos:
- Home: lista de tareas con agregar y eliminar.
- About: vista simple informativa.
- Navegacion por hash sin recarga total.
- Estructura propuesta de carpetas para evolucionar a React/Next.js.

Pauta de ejecucion sugerida:
- Min 1-5: base HTML + contenedor principal.
- Min 6-12: logica DOM (agregar/eliminar tareas).
- Min 13-17: routing hash Home/About.
- Min 18-20: limpieza rapida y explicacion de estructura.

Criterios de exito:
- Interaccion funcional en Home.
- Navegacion funcional entre 2 vistas.
- Explicacion clara (30-60s) de por que su estructura es modular.

---

## 7) Errores frecuentes y correccion

- Error: todo en un solo archivo largo.
  Correccion: separar render, eventos y utilidades.
- Error: editar sin validar entrada de usuario.
  Correccion: usar trim y cortar flujo si esta vacio.
- Error: confundir SPA con "muchas paginas HTML".
  Correccion: reforzar documento unico + cambio de vista por router.
- Error: pasar a React sin entender bien DOM/eventos.
  Correccion: practicar primero flujo DOM basico y luego abstraer con componentes.

## 8) Cierre de sesion

Mensaje clave:
- Primero dominar fundamentos (DOM + arquitectura), luego escalar con React/Next.js.

Resultado esperado:
- Estudiante capaz de construir una mini app interactiva y explicar sus decisiones tecnicas basicas en lenguaje simple.
