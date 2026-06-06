# Guia Docente: SPA Architecture and Bundling

Este documento adapta el modulo de arquitectura SPA para una clase online.
El foco es que el estudiante entienda el ciclo build/runtime,
la navegacion en cliente y el rol del bundling en aplicaciones modernas.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar que es una SPA y que problemas resuelve frente a MPA.
  Como explicarlo: comparar flujos de navegacion y recarga entre ambos enfoques.
- Diferenciar build time y runtime con ejemplos reales.
  Como explicarlo: seguir el viaje del codigo desde fuente hasta navegador.
- Describir el proceso de empaquetado y su impacto en performance.
  Como explicarlo: inspeccionar artefactos generados y tamaño de bundles.
- Entender enrutamiento del lado cliente con hash e History API.
  Como explicarlo: implementar navegacion simple sin recarga total.
- Detectar antipatrones comunes en SPA.
  Como explicarlo: analizar casos de acoplamiento excesivo y estado desordenado.

## 2. Mapa del modulo (19 lecciones)

1. 0 Bienvenido a la arquitectura spa
2. 1 Que significa construir una aplicacion
3. 1.1 El proceso de empaquetado
4. 1.2 Inspeccionando una aplicacion construida
5. 2 Tiempo de construccion explicado
6. 2.1 Tiempo de ejecucion en el navegador
7. 2.2 Modelo mental de dos fases
8. 3 Sitios web tradicionales multipagina
9. 3.1 Problemas que resuelven las spa
10. 3.2 Comparando mpa vs spa
11. 4 Un archivo html en spa
12. 4.1 Ilusion de navegacion
13. 4.2 Anti patrones en spa
14. 5 Enrutamiento basado en hash
15. 5.1 Api de historial del navegador
16. 5.2 Observando el comportamiento del enrutamiento
17. 6 Mapeando la arquitectura de una aplicacion real
18. 6.1 Evaluacion de spa y empaquetado
19. 7 Que sigue

## 3. Guion sugerido para clase online (50 minutos)

### Bloque A (12 min): Build vs Runtime

- Que ocurre al compilar y empaquetar.
  Como explicarlo: trazar pasos desde modulos fuente hasta bundle final.
- Que ocurre al ejecutar en navegador.
  Como explicarlo: mostrar carga inicial, hidratacion y navegacion interna.

### Bloque B (12 min): MPA vs SPA

- Comparacion de experiencia de usuario.
  Como explicarlo: medir recargas, latencia percibida y continuidad visual.
- Criterios para elegir arquitectura.
  Como explicarlo: decidir segun complejidad, SEO, equipo y mantenimiento.

### Bloque C (14 min): Routing en cliente

- Hash routing y History API.
  Como explicarlo: implementar rutas simples y observar URL + render.
- Ilusion de navegacion.
  Como explicarlo: mostrar cambio de vista sin descarga de documento completo.

### Bloque D (12 min): Antipatrones y evaluacion

- Antipatrones clasicos.
  Como explicarlo: ejemplos de estado global caotico, rutas sin contrato y componentes gigantes.
- Evaluacion rapida.
  Como explicarlo: checklist sobre build, runtime, routing y decisiones de arquitectura.

## 4. Ejemplos para mostrar en vivo

### Ejemplo 1: Diferencia build time vs runtime

```text
Build time:
- Transpilar TypeScript
- Empaquetar modulos
- Minificar assets

Runtime:
- Cargar bundle en navegador
- Ejecutar router cliente
- Renderizar vistas y manejar eventos
```

### Ejemplo 2: Hash routing minimo

```js
function render() {
  const route = window.location.hash || "#/home";
  const app = document.querySelector("#app");
  if (!app) return;
  app.textContent = route === "#/about" ? "Vista About" : "Vista Home";
}

window.addEventListener("hashchange", render);
render();
```

### Ejemplo 3: History API basica

```js
function navigate(path) {
  history.pushState({}, "", path);
  document.querySelector("#app").textContent = `Ruta actual: ${path}`;
}

window.addEventListener("popstate", () => {
  document.querySelector("#app").textContent = `Ruta actual: ${location.pathname}`;
});
```

## 5. Errores frecuentes y correccion

- Error: confundir bundle con aplicacion completa.
  Correccion: separar artefacto compilado de comportamiento en runtime.
- Error: usar SPA para cualquier caso sin evaluar contexto.
  Correccion: decidir con matriz simple de requisitos.
- Error: routing sin manejo de rutas no encontradas.
  Correccion: definir fallback y estados de error desde el inicio.
- Error: ignorar impacto de tamaño de bundle.
  Correccion: monitorear peso y aplicar division de codigo cuando proceda.

## 6. Cierre para sesion

- Mensaje clave: comprender arquitectura evita escalar deuda tecnica en frontend.
- Resultado esperado: estudiante capaz de justificar SPA/MPA y explicar bundling con claridad.
- Siguiente paso: integrar esta base con componentes React y Next.js en resume_04.

## 7. Nota de calidad del scraping

El JSON contiene 19 lecciones y cubre de forma completa arquitectura, routing y empaquetado.
