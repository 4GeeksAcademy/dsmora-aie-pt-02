# Guia Docente: Introduction to React and Next.js

Este documento adapta el modulo de introduccion a React y Next.js para clase online.
El foco es pasar de paginas tradicionales a apps basadas en componentes,
entender App Router y tomar decisiones iniciales de renderizado.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar el modelo mental de componentes en React.
  Como explicarlo: descomponer una UI conocida en piezas reutilizables.
- Entender el rol de Next.js sobre React.
  Como explicarlo: diferenciar responsabilidades de libreria y framework.
- Navegar la estructura de proyecto con App Router.
  Como explicarlo: mapear carpetas, layouts, pages y metadata.
- Distinguir estrategias de renderizado (CSR y SSR).
  Como explicarlo: comparar impacto en UX, SEO y carga inicial.
- Identificar anti patrones de principiantes.
  Como explicarlo: revisar ejemplos comunes y su alternativa correcta.

## 2. Mapa del modulo (22 lecciones)

1. 0 Bienvenido de paginas html a aplicaciones basadas en componentes
2. 1 Que es un componente web en react
3. 1.1 Como react actualiza la web con virtual dom
4. 1.2 Creando tu primer componente react
5. 2 Que es next.js y por que usarlo
6. 2.1 Responsabilidades de react vs next.js
7. 2.2 Configurando un proyecto next.js
8. 3 Como se organiza un proyecto next.js
9. 3.1 Paginas vs componentes vs disenos
10. 3.2 Navegando por un codigo real de next.js
11. 4 Convenciones del enrutador de aplicaciones y carpetas principales
12. 4.1 Archivos de enrutamiento rutas anidadas y grupos
13. 4.2 Convenciones de archivos de metadata
14. 4.3 Construyendo una estructura multipagina con el enrutador de aplicaciones
15. 5 Estrategias de renderizado csr vs ssr
16. 5.1 Elegir la estrategia de renderizado correcta
17. 6 Primera mirada a props estado y efectos
18. 6.1 Construyendo un componente con props
19. 6.2 Anti patrones errores comunes de principiantes
20. 7 Practica armar una pagina simple next.js
21. 7.1 Evaluacion de conocimientos
22. 8 Conclusion del curso y proximos pasos

## 3. Guion sugerido para clase online (60 minutos)

### Bloque A (12 min): De HTML a componentes

- Por que pensar en componentes mejora mantenibilidad.
  Como explicarlo: reconstruir una pantalla por secciones reutilizables.
- Virtual DOM y actualizacion eficiente.
  Como explicarlo: comparar cambio puntual en DOM tradicional vs React.

### Bloque B (14 min): React vs Next.js

- Responsabilidades separadas.
  Como explicarlo: React para UI y estado; Next.js para arquitectura de app.
- Arranque de proyecto y estructura inicial.
  Como explicarlo: revisar carpetas y archivos clave de una app nueva.

### Bloque C (16 min): App Router y convenciones

- Layouts, pages y rutas anidadas.
  Como explicarlo: construir una mini estructura multipagina en vivo.
- Metadata y organización del proyecto.
  Como explicarlo: agregar metadata por ruta y validar resultado.

### Bloque D (12 min): Renderizado y anti patrones

- CSR vs SSR en decisiones reales.
  Como explicarlo: usar casos de dashboard, marketing page y contenido SEO.
- Errores frecuentes de principiantes.
  Como explicarlo: detectar uso incorrecto de estado/efectos y exceso de logica en componentes.

### Bloque E (6 min): Practica y cierre

- Mini practica guiada.
  Como explicarlo: armar una pagina simple con componentes y routing basico.
- Evaluacion corta.
  Como explicarlo: preguntas de chequeo sobre router y render.

## 4. Ejemplos para mostrar en vivo

### Ejemplo 1: Componente React con props

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

### Ejemplo 2: Estructura App Router minima

```text
app/
  layout.tsx
  page.tsx
  blog/
    page.tsx
  dashboard/
    page.tsx
```

### Ejemplo 3: Decision CSR vs SSR

```text
Caso A: dashboard interno con datos muy dinamicos -> CSR
Caso B: landing publica orientada a SEO -> SSR
Regla docente: elegir estrategia por contexto de producto, no por preferencia personal.
```

## 5. Errores frecuentes y correccion

- Error: crear componentes demasiado grandes.
  Correccion: dividir por responsabilidad y reutilizacion.
- Error: confundir carpeta de ruta con componente reutilizable.
  Correccion: separar app routing de components compartidos.
- Error: elegir CSR/SSR por intuicion.
  Correccion: decidir con criterio de datos, SEO y experiencia.
- Error: sobreusar useEffect para logica que no lo requiere.
  Correccion: simplificar flujo y mover calculos al render cuando aplique.

## 6. Cierre para sesion

- Mensaje clave: React + Next.js no es solo sintaxis, es diseño de arquitectura frontend.
- Resultado esperado: estudiante capaz de iniciar y organizar una app moderna con criterio.
- Siguiente paso: fortalecer modularizacion y estructura de carpetas en resume_05.

## 7. Nota de calidad del scraping

El JSON contiene 22 lecciones y cubre introduccion, routing, renderizado y practica final.
