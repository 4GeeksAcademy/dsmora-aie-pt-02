# Guia Docente: Class 14 - React, Next.js y Organizacion Frontend

Este resumen integra los JSON de class_14 para una clase online de 60 minutos maximo.
El foco es que el estudiante entienda componentes, App Router y organizacion del codigo,
sin perder de vista arquitectura SPA y decisiones de renderizado.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar la diferencia entre React (libreria UI) y Next.js (framework).
  Como explicarlo: React construye componentes; Next.js organiza rutas, renderizado y estructura.
- Crear y reutilizar componentes basicos con JSX y props.
  Como explicarlo: construir un componente de tarjeta y usarlo varias veces con datos distintos.
- Entender App Router y estructura de carpetas en Next.js.
  Como explicarlo: mapear app/page.tsx, app/about/page.tsx y components/ en un ejemplo simple.
- Organizar un frontend por modulos y responsabilidades.
  Como explicarlo: separar vistas, componentes reutilizables, hooks y utilidades.
- Describir que es una SPA y como influye el bundling en la experiencia.
  Como explicarlo: comparar recarga total (MPA) vs navegacion fluida (SPA).

## 2. Conceptos clave explicados en palabras simples

- Componente: pieza reutilizable de interfaz, como un bloque lego.
- Props: datos de entrada para personalizar un componente sin reescribirlo.
- App Router: sistema de rutas por carpetas en Next.js.
- Modularizacion: dividir codigo en partes pequenas con responsabilidad clara.
- Build y bundling: proceso que transforma tu codigo fuente en archivos listos para navegador.
- SPA: app que cambia vistas sin recargar toda la pagina.

## 3. Guion sugerido para clase online (60 minutos)

### Bloque A (12 min): De HTML a componentes

- Que problema resuelven los componentes reutilizables.
- Ejemplo guiado de componente simple con JSX.

### Bloque B (12 min): React vs Next.js y App Router

- Responsabilidades de cada tecnologia.
- Estructura minima de proyecto Next.js y rutas por archivos.

### Bloque C (12 min): Organizacion del frontend

- Separar vistas y componentes.
- Agrupar por feature o por tipo sin mezclar responsabilidades.

### Bloque D (6 min): Arquitectura SPA y bundling

- Que pasa en build time y que pasa en runtime.
- Por que una SPA se siente mas fluida en navegacion.

### Bloque E (18 min): Mini ejercicio final (maximo 20 min)

- Objetivo: crear una mini app con 2 rutas y 1 componente reutilizable.
- Requisitos:
  - Ruta Home y ruta About.
  - Componente Card reutilizable con props title y description.
  - Una seccion organizada en carpeta components/.
  - Navegacion sin recarga completa usando Link.
- Criterio de exito:
  - El estudiante navega entre 2 paginas.
  - Reutiliza el componente al menos 2 veces.
  - Explica en 1 minuto por que su estructura es modular.

## 4. Ejemplos para mostrar en vivo

### Ejemplo 1: Componente reutilizable

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

### Ejemplo 2: App Router minimo

```text
app/
  page.tsx
  about/
    page.tsx
components/
  Card.tsx
```

### Ejemplo 3: Decidir SPA vs MPA en lenguaje simple

```text
Si necesitas transiciones rapidas entre vistas y UX tipo app, SPA ayuda.
Si necesitas paginas muy orientadas a SEO y contenido estatico, combinar SSR/SSG puede ser mejor.
```

## 5. Errores frecuentes y correccion

- Error: crear componentes gigantes.
  Correccion: dividir por responsabilidad y reuso.
- Error: mezclar codigo de ruta con utilidades.
  Correccion: mantener app/ para rutas y otras carpetas para logica compartida.
- Error: organizar carpetas sin criterio.
  Correccion: definir una convencion simple y aplicarla de forma consistente.
- Error: confundir SPA con "no necesita arquitectura".
  Correccion: mantener estructura, contratos y limites entre modulos.

## 6. Cierre para sesion

- Mensaje clave: una buena app no solo funciona, tambien esta bien organizada para crecer.
- Resultado esperado: estudiante capaz de crear una base React/Next.js clara y mantenible en pequeno.
- Siguiente paso: conectar esta base con hooks, renderizado y depuracion de class_15.
