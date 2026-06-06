# Guia Docente: DOM Mastery with JavaScript

Este documento adapta el modulo a una guia para clase online.
El foco es que el estudiante domine el DOM con criterio practico:
seleccionar nodos, modificar contenido y construir interacciones.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar que es el DOM y por que conecta HTML, CSS y JavaScript.
  Como explicarlo: mostrar una pagina simple y representar el arbol de nodos en vivo.
- Seleccionar elementos con APIs del navegador.
  Como explicarlo: comparar querySelector y querySelectorAll en ejemplos cortos.
- Modificar texto, atributos y estructura de la pagina.
  Como explicarlo: editar contenido de un componente sin recargar la vista.
- Crear y eliminar elementos de forma controlada.
  Como explicarlo: construir una lista dinamica y desmontar nodos por evento.
- Manejar eventos para activar comportamiento interactivo.
  Como explicarlo: asociar acciones de usuario a cambios visibles en pantalla.

## 2. Mapa del modulo (10 lecciones)

1. 0 Bienvenido a dominio dom
2. 1 Entendiendo la estructura dom
3. 1.1 Seleccionando elementos dom
4. 1.2 Trabajando con multiples elementos
5. 2 Modificando contenido dom
6. 2.1 Cambiando texto y atributos
7. 2.2 Creando y eliminando elementos
8. 3 Manejando eventos dom
9. 3.1 Construyendo una funcion interactiva
10. 4 Prueba tus habilidades dom

## 3. Guion sugerido para clase online (40 minutos)

### Bloque A (10 min): Fundamentos del DOM

- DOM como representacion estructurada del documento.
  Como explicarlo: inspeccionar elementos en DevTools y ubicar padre/hijo/hermano.
- Lectura de estructura antes de programar cambios.
  Como explicarlo: identificar nodos objetivo y su rol en la interfaz.

### Bloque B (12 min): Seleccion y modificacion

- Seleccion de uno o multiples elementos.
  Como explicarlo: resolver una misma tarea con selectores distintos.
- Cambios de texto, atributos y clases.
  Como explicarlo: alternar estado visual de un bloque usando classList y setAttribute.

### Bloque C (12 min): Creacion, eliminacion y eventos

- Crear nodos y anexarlos al documento.
  Como explicarlo: generar items en una lista desde una entrada de usuario.
- Eliminar nodos de forma segura.
  Como explicarlo: asociar botones de borrar a cada item agregado.
- Eventos de click y flujo de interaccion.
  Como explicarlo: demostrar callback simple con validacion minima.

### Bloque D (6 min): Cierre y mini reto

- Integracion de conceptos en una funcion interactiva.
  Como explicarlo: construir un mini widget que lea input y pinte salida en DOM.
- Reto final.
  Como explicarlo: plantear mejora incremental para practicar fuera de clase.

## 4. Ejemplos para mostrar en vivo

### Ejemplo 1: Seleccion y actualizacion de contenido

```js
const title = document.querySelector("h1");
if (title) {
  title.textContent = "DOM actualizado en vivo";
}
```

### Ejemplo 2: Crear y eliminar elementos

```js
const list = document.querySelector("#tasks");
const item = document.createElement("li");
item.textContent = "Nueva tarea";

if (list) {
  list.appendChild(item);
  setTimeout(() => item.remove(), 2000);
}
```

### Ejemplo 3: Evento con validacion minima

```js
const btn = document.querySelector("#save-btn");
const input = document.querySelector("#name-input");

btn?.addEventListener("click", () => {
  const value = input?.value?.trim() || "";
  if (!value) return;
  console.log("Guardado:", value);
});
```

## 5. Errores frecuentes y correccion

- Error: modificar DOM sin verificar que el elemento existe.
  Correccion: validar null antes de operar y fallar con mensaje claro.
- Error: usar innerHTML para todo.
  Correccion: priorizar textContent y createElement cuando sea posible.
- Error: listeners duplicados por mala ubicacion del codigo.
  Correccion: registrar eventos una sola vez en inicializacion.
- Error: mezclar logica de datos con render sin orden.
  Correccion: separar funciones de lectura, actualizacion y pintado.

## 6. Cierre para sesion

- Mensaje clave: dominar DOM es dominar la base de cualquier frontend interactivo.
- Resultado esperado: estudiante capaz de construir interacciones sin frameworks.
- Siguiente paso: reforzar tecnica con ejercicios guiados del resume_02.

## 7. Nota de calidad del scraping

El JSON contiene 10 lecciones y se detecto contenido util para todo el flujo: estructura, manipulacion y eventos.
