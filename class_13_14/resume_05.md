# Guia Docente: Organizing Your Frontend

Este documento adapta el modulo de organizacion frontend para clase online.
El foco es que el estudiante estructure codigo y carpetas para escalar,
modularice correctamente y evite caos de nombrado.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar por que la estructura de carpetas impacta velocidad de desarrollo.
  Como explicarlo: comparar un proyecto ordenado frente a uno desorganizado.
- Definir que es un modulo y cuando conviene extraerlo.
  Como explicarlo: detectar responsabilidades repetidas en una misma vista.
- Separar vistas y componentes reutilizables.
  Como explicarlo: refactorizar una pantalla en piezas con contrato claro.
- Aplicar convenciones de nombrado y exportaciones barrel.
  Como explicarlo: estandarizar rutas de importacion y lectura del proyecto.
- Identificar antipatrones de organizacion y corregirlos.
  Como explicarlo: auditar una estructura caotica y proponer plan de mejora.

## 2. Mapa del modulo (16 lecciones)

1. 0 Por que la estructura de carpetas importa
2. 1 Que es un modulo
3. 1.1 El costo de no modularizar
4. 1.2 Identificando oportunidades de modularizacion
5. 2 Separacion vistas vs componentes
6. 2.1 Extrayendo un componente
7. 2.2 Estrategias de agrupacion
8. 2.3 Ejercicio de reorganizacion modal
9. 3 Arquitectura de carpetas nextjs
10. 3.1 Marco de colocacion de archivos
11. 3.2 Antipatrones de codigo desorganizado
12. 4 Convenciones de nombrado
13. 4.1 Ejercicio de exportaciones barrel
14. 4.2 Antipatrones de caos en nombrado
15. 5 Cuestionario de modularizacion frontend
16. 6 Conclusion del curso y proximos pasos

## 3. Guion sugerido para clase online (45 minutos)

### Bloque A (10 min): Importancia de la organizacion

- Impacto directo en mantenimiento y onboarding.
  Como explicarlo: mostrar tiempo de busqueda en estructura limpia vs caotica.
- Concepto de modulo y cohesión.
  Como explicarlo: separar por responsabilidad funcional y no por moda.

### Bloque B (12 min): Vistas, componentes y agrupacion

- Separar capa de pagina de componentes reutilizables.
  Como explicarlo: extraer una seccion repetida de una vista principal.
- Estrategias de agrupacion.
  Como explicarlo: organizar por feature o por tipo segun escala del proyecto.

### Bloque C (13 min): Arquitectura Next.js y naming

- Marco de colocacion de archivos.
  Como explicarlo: decidir donde viven rutas, UI compartida y utilidades.
- Convenciones de nombrado.
  Como explicarlo: definir patrones para componentes, hooks y servicios.
- Exportaciones barrel.
  Como explicarlo: centralizar exports para imports mas limpios.

### Bloque D (10 min): Antipatrones y evaluacion

- Antipatrones tipicos.
  Como explicarlo: archivos gigantes, nombres ambiguos y dependencias cruzadas.
- Evaluacion rapida.
  Como explicarlo: checklist de modularidad y legibilidad del proyecto.

## 4. Ejemplos para mostrar en vivo

### Ejemplo 1: Estructura por feature

```text
src/
  features/
    auth/
      components/
      hooks/
      services/
    products/
      components/
      services/
```

### Ejemplo 2: Separacion vista vs componente

```tsx
// app/products/page.tsx (vista)
import { ProductList } from "@/features/products/components/ProductList";

export default function ProductsPage() {
  return <ProductList />;
}
```

```tsx
// features/products/components/ProductList.tsx (componente reusable)
export function ProductList() {
  return <section>Listado de productos</section>;
}
```

### Ejemplo 3: Barrel exports para imports limpios

```ts
// features/products/components/index.ts
export * from "./ProductList";
export * from "./ProductCard";
```

## 5. Errores frecuentes y correccion

- Error: crear carpetas por impulso sin criterio estable.
  Correccion: documentar regla de organizacion y aplicarla de forma consistente.
- Error: mezclar vistas con componentes compartidos.
  Correccion: separar ambito de pagina y ambito reutilizable.
- Error: naming inconsistente entre archivos similares.
  Correccion: adoptar convención unica y hacer refactor incremental.
- Error: exportaciones dispersas que complican imports.
  Correccion: introducir archivos index por modulo cuando aporte claridad.

## 6. Cierre para sesion

- Mensaje clave: una buena arquitectura de carpetas reduce deuda tecnica desde el inicio.
- Resultado esperado: estudiante capaz de organizar un frontend para crecer sin caos.
- Siguiente paso: aplicar estas reglas en los proyectos de clase 13 y siguientes.

## 7. Nota de calidad del scraping

El JSON contiene 16 lecciones y cubre modularizacion, arquitectura de carpetas y convenciones de equipo.
