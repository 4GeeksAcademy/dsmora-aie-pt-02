# Guia Docente: The DOM Exercises

Este documento adapta el modulo practico a una guia para clase online.
El foco es consolidar dominio operativo del DOM mediante ejercicios cortos,
de dificultad progresiva y retroalimentacion inmediata.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Resolver tareas concretas de manipulacion del DOM con rapidez.
  Como explicarlo: trabajar ejercicios atomicos de una sola habilidad por paso.
- Cambiar estilos y posicion de elementos dinamicamente.
  Como explicarlo: partir de un bloque base y aplicar cambios por evento.
- Crear elementos y listas a partir de datos de entrada.
  Como explicarlo: transformar texto del usuario en nodos nuevos dentro del documento.
- Eliminar elementos existentes sin romper la estructura.
  Como explicarlo: practicar remove en escenarios simples y repetibles.
- Construir una mini Todo List conectando varias tecnicas.
  Como explicarlo: integrar selectores, eventos, creacion de nodos y render.

## 2. Mapa del modulo (15 lecciones)

1. 0 Welcome
2. 1 Hello world
3. 2 Select DOM Element
4. 3 Change Div Background
5. 4 Move DOM Element
6. 5 Create DOM Element First
7. 6 Create DOM Element Second
8. 7 Create DOM list of li
9. 8.1 Remove DOM Element
10. 8.2 Remove DOM Element
11. 9 Render on Click
12. 10 Add li on Click
13. 11 Dynamic HTML String
14. 12 Add Options to the Select
15. 13 Todo List

## 3. Guion sugerido para taller online (45 minutos)

### Bloque A (10 min): Calentamiento de selectores y estilo

- Localizar nodos y validar seleccion.
  Como explicarlo: resolver Select DOM Element y mostrar errores comunes de selector.
- Cambiar estilos en caliente.
  Como explicarlo: modificar fondo y posicion para visualizar impacto inmediato.

### Bloque B (12 min): Creacion y destruccion de nodos

- Crear elementos con createElement y append.
  Como explicarlo: construir un bloque nuevo y anexarlo en contenedor principal.
- Remover elementos con control.
  Como explicarlo: aplicar remove en casos 8.1 y 8.2 para comparar estrategias.

### Bloque C (13 min): Render por evento

- Renderizar contenido en click.
  Como explicarlo: conectar boton con funcion que pinta HTML dinamico.
- Agregar items a listas en cada accion.
  Como explicarlo: usar Add li on Click con contador o texto ingresado.

### Bloque D (10 min): Integracion en Todo List

- Montar una solucion de punta a punta.
  Como explicarlo: resolver Todo List separando input, render y eventos.
- Checklist de calidad.
  Como explicarlo: revisar legibilidad, reuso de funciones y manejo de casos vacios.

## 4. Ejemplos para mostrar en vivo

### Ejemplo 1: Cambiar estilo por selector

```js
const box = document.querySelector(".box");
if (box) {
  box.style.backgroundColor = "#2563eb";
  box.style.color = "white";
}
```

### Ejemplo 2: Agregar item a lista en click

```js
const ul = document.querySelector("#items");
const input = document.querySelector("#item-input");
const addBtn = document.querySelector("#add-btn");

addBtn?.addEventListener("click", () => {
  const text = input?.value?.trim() || "";
  if (!text || !ul) return;
  const li = document.createElement("li");
  li.textContent = text;
  ul.appendChild(li);
});
```

### Ejemplo 3: Mini Todo con remove

```js
function addTodo(text) {
  const li = document.createElement("li");
  const btn = document.createElement("button");
  li.textContent = text + " ";
  btn.textContent = "x";
  btn.addEventListener("click", () => li.remove());
  li.appendChild(btn);
  document.querySelector("#todos")?.appendChild(li);
}
```

## 5. Errores frecuentes y correccion

- Error: resolver ejercicios con codigo duplicado.
  Correccion: extraer funciones auxiliares reutilizables.
- Error: construir HTML dinamico inseguro sin validar entrada.
  Correccion: sanitizar o usar textContent cuando sea posible.
- Error: no limpiar estado visual despues de cada accion.
  Correccion: resetear inputs y asegurar consistencia del DOM.
- Error: depender del orden accidental de nodos.
  Correccion: seleccionar por id o clase estable.

## 6. Cierre para sesion

- Mensaje clave: la fluidez en DOM se gana con practica corta y frecuente.
- Resultado esperado: estudiante capaz de resolver ejercicios de manipulación en minutos.
- Siguiente paso: pasar de ejercicios aislados a arquitectura SPA en resume_03.

## 7. Nota de calidad del scraping

El JSON contiene 15 lecciones practicas y cubre progresion completa desde seleccion basica hasta Todo List.
