# Clase 41: medir y optimizar el rendimiento frontend

## Nota de alcance

Esta guía se redacta a partir de los JSON guardados en esta carpeta. El tutorial de Core Web Vitals contiene 7 lecciones. El tutorial de estrategias para React contiene 7 lecciones guardadas, hasta `2.3 Principios de memoria cache`; el scraper visitó más lecciones, pero no llegó a persistirlas en el JSON. Además, algunas lecciones presentan contenido repetido o desalineado con su título, por lo que la secuencia temática es la referencia principal.

## Objetivos de aprendizaje

Al terminar, el grupo podrá:

- Explicar qué miden FCP, LCP y TBT.
- Usar Lighthouse, PageSpeed Insights y la pestaña Performance de Chrome DevTools como herramientas de medición.
- Interpretar los umbrales de LCP: bueno hasta 2.5 s, necesita mejora por encima de 2.5 s y hasta 4 s, y pobre por encima de 4 s.
- Relacionar imágenes, CSS, JavaScript y renderizado del lado del cliente con el rendimiento observado.
- Explicar la división de código y la carga perezosa con `React.lazy` y `Suspense`.
- Distinguir `React.memo`, `useMemo` y la memoria caché para solicitudes de red.
- Aplicar el ciclo medir, identificar, optimizar y repetir.

## Preparación del profesor

- Abrir los dos JSON de esta carpeta para consultar los ejemplos.
- Tener disponible un proyecto React donde se puedan mostrar componentes, rutas o una lista filtrada. El material fuente usa ejemplos como `Dashboard`, `Settings`, `HeavyModal`, `ExpensiveList`, `FilteredList` y un endpoint `/api/users/${userId}`.
- Tener abierto Chrome DevTools para mostrar Lighthouse y la pestaña Performance.
- Preparar una explicación breve del estado inicial y del estado después de una optimización.
- Si se vuelve a extraer el tutorial React, comprobar primero que el JSON tenga las 12 lecciones antes de ampliar esta guía.

## Agenda de 60 minutos

| Tiempo | Bloque |
|---|---|
| 0-5 min | Entrada: rendimiento como experiencia y negocio |
| 5-18 min | Core Web Vitals y herramientas de medición |
| 18-30 min | FCP, LCP y TBT con escenarios |
| 30-42 min | División de código y carga perezosa |
| 42-53 min | Memoización: `React.memo` y `useMemo` |
| 53-57 min | Memoria caché para solicitudes |
| 57-60 min | Medir, mejorar, repetir y comprobación final |

Para una clase de 75 minutos, usar la extensión indicada en cada bloque y reservar 5 minutos para que el grupo interprete sus propias mediciones.

## Desarrollo para el profesor

### 1. Entrada: por qué medir (5 minutos)

**Qué decir (literal)**

> El rendimiento frontend no es solo una característica técnica. Una interfaz lenta puede frustrar a los usuarios, aumentar el abandono y afectar la experiencia. Antes de optimizar, necesitamos una medición. La idea que guía la clase es: no podemos mejorar lo que no medimos.

Presentar las tres áreas del curso React como tres preguntas: ¿podemos cargar menos código?, ¿podemos calcular menos?, ¿podemos repetir menos solicitudes? Conectar cada pregunta con división de código, memoización y caché.

**Pregunta para el grupo**

> Si una aplicación tiene Inicio, Configuración y Análisis, ¿qué problema aparece si el navegador descarga desde el principio el código de las tres rutas?

**Respuesta esperada**

Se descarga y ejecuta más JavaScript del necesario, aumentando la carga inicial, el uso de datos y el tiempo hasta la interacción.

### 2. Core Web Vitals y herramientas (13 minutos)

**Qué decir (literal)**

> Core Web Vitals es un conjunto de métricas definido por Google para capturar la experiencia real del usuario. Hoy nos interesan dos dimensiones: carga e interactividad. FCP indica cuándo aparece el primer contenido; LCP indica cuándo aparece el contenido principal; TBT indica cuánto tiempo la página bloquea la interacción durante la carga.

Mostrar las herramientas que aparecen en el material: Lighthouse, integrado en Chrome DevTools; PageSpeed Insights, que combina datos de laboratorio y datos reales; y la pestaña Performance de Chrome DevTools, que permite observar lo que ocurre durante la carga.

**Prompt exacto para la demo**

```text
Analiza esta página con Lighthouse y organiza el resultado en FCP, LCP y TBT. Para cada métrica, indica si el problema corresponde principalmente a carga o a interactividad y señala una posible causa visible en el informe.
```

**Qué preguntar después**

> ¿Qué diferencia hay entre una herramienta que simula una carga y una que también combina datos reales de usuarios?

No convertir la explicación en una lista de optimizaciones todavía. El objetivo de este bloque es que el grupo aprenda a leer una línea base.

### 3. FCP, LCP y TBT mediante escenarios (12 minutos)

**Qué decir (literal)**

> FCP se dispara cuando se renderiza cualquier contenido DOM visible. LCP se refiere al elemento visible más grande que representa el contenido principal. TBT refleja el bloqueo de la interacción durante la carga. Una página puede verse lista y, aun así, no responder a los clics: en ese caso la métrica que debemos investigar es TBT.

Usar estos escenarios del material:

- FCP de 4.2 segundos: investigar recursos que bloquean el renderizado, como CSS síncrono.
- LCP de 5.8 segundos con una imagen principal: comprimirla, convertirla a WebP y precargarla.
- Una tarea larga de 320 ms: aporta 270 ms al TBT.
- Un paquete grande usado para una sola fecha: puede crear tareas largas en el hilo principal durante la ejecución de JavaScript.

Mostrar el ejemplo de precarga incluido en la fuente:

```html
<link rel="preload" as="image" href="hero.webp">
```

**Qué decir (literal)**

> La precarga comunica pronto al navegador que la imagen principal es importante. No estamos aplicando una receta a ciegas: primero asociamos la intervención con el elemento LCP y después volvemos a medir.

**Extensión a 75 minutos**

Pedir al grupo que clasifique tres casos como FCP, LCP o TBT y que justifique la elección en una frase. La pregunta clave es: ¿la página tarda en mostrar algo, en mostrar lo principal o en responder?

### 4. División de código y carga perezosa (12 minutos)

**Qué decir (literal)**

> La división de código separa el paquete de JavaScript en fragmentos más pequeños. El navegador carga inicialmente solo lo que necesita para la página o interacción actual. Las importaciones dinámicas indican al empaquetador que cree fragmentos que se cargarán de forma asíncrona.

Presentar el ejemplo de componente perezoso del material:

```jsx
const Dashboard = React.lazy(() => import('./Dashboard'));
```

Explicar que `Suspense` proporciona una interfaz de reserva mientras se obtiene el componente. Para una demostración de rutas, usar la estructura fuente:

```jsx
import { Routes, Route } from 'react-router-dom';

const Dashboard = React.lazy(() => import('./Dashboard'));
const Settings = React.lazy(() => import('./Settings'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

**Qué decir (literal)**

> En este caso, Dashboard y Settings no forman necesariamente parte del primer fragmento. Cada ruta puede obtener su código cuando el usuario la visita. El fallback debe ser significativo porque representa el estado visible mientras llega ese código.

Mencionar la alternativa de cargar bajo demanda un modal pesado, como `HeavyModal`, solo cuando el usuario lo abre. Recordar la restricción indicada por la fuente: `React.lazy` trabaja con exportaciones por defecto.

**Prompt exacto para la demo**

```text
Revisa este componente React y propón cómo dividirlo para que Dashboard y Settings se carguen bajo demanda con React.lazy y Suspense. Conserva las rutas, añade un fallback significativo y explica qué código deja de cargarse inicialmente.
```

### 5. Memoización con React.memo y useMemo (11 minutos)

**Qué decir (literal)**

> Memoizar significa almacenar un resultado para evitar trabajo innecesario. `React.memo` envuelve un componente y evita su re-renderizado cuando sus props son superficialmente iguales. `useMemo` almacena el resultado de un cálculo costoso y lo recalcula cuando cambian sus dependencias.

Mostrar el ejemplo fuente de `React.memo`:

```jsx
const ExpensiveList = React.memo(function ExpensiveList({ items }) {
  console.log('Renderizando ExpensiveList');
  return <ul>{items.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
});
```

Después mostrar el ejemplo fuente de `useMemo`:

```jsx
function FilteredList({ products, filter }) {
  const filtered = React.useMemo(() => {
    return products.filter(p => p.category === filter);
  }, [products, filter]);

  return <ul>{filtered.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

**Qué decir (literal)**

> El arreglo de dependencias define cuándo se recalcula el valor. Si falta una variable usada dentro de la función, podemos conservar datos desactualizados. Por eso `useMemo` tiene sentido para filtrar, ordenar o formatear conjuntos grandes, no para cualquier cálculo barato.

Añadir un `console.log` dentro de la función memorizada y cambiar un estado no relacionado. La fuente propone observar así cuándo vuelve a ejecutarse el filtrado.

**Qué preguntar después**

> ¿Qué diferencia hay entre `React.memo` y `useMemo`?

Respuesta esperada: uno ayuda a evitar re-renderizados del componente según sus props; el otro memoriza el valor de un cálculo según sus dependencias. Recordar también que referencias nuevas de objetos o arreglos pueden hacer fallar la comparación superficial de `React.memo`.

### 6. Memoria caché para solicitudes (4 minutos)

**Qué decir (literal)**

> En frontend, repetir la misma solicitud de red añade latencia y desperdicia recursos. El principio de esta lección es que la solicitud más rápida es la que no hacemos. Una caché puede almacenar los datos del usuario y devolverlos directamente cuando ya están disponibles.

Usar el patrón de la fuente como lectura guiada:

```jsx
if (userCache[userId]) {
  setUser(userCache[userId]);
  setLoading(false);
  return;
}

setLoading(true);
setError(null);

fetch(`/api/users/${userId}`)
  .then(res => {
    if (!res.ok) throw new Error('La respuesta de la red no fue correcta');
    return res.json();
  })
  .then(data => {
    userCache[userId] = data;
    setUser(data);
  });
```

Aclarar que la caché exige decidir cuándo los datos quedan obsoletos. No presentar una política de expiración adicional como si estuviera definida por el material.

### 7. Cierre: medir, identificar, optimizar, repetir (3 minutos)

**Qué decir (literal)**

> La optimización es un ciclo. Primero medimos con una línea base. Después identificamos qué Core Web Vital está bajo rendimiento y buscamos la causa raíz. Aplicamos una corrección específica, como comprimir una imagen, diferir JavaScript, insertar CSS crítico, dividir paquetes o reducir solicitudes repetidas. Finalmente medimos de nuevo para comprobar si la mejora existe.

## Recorte a 60 minutos

- Mantener un solo escenario de cada métrica.
- Mostrar el ejemplo de `React.lazy` y explicar `Suspense` sin construir el flujo completo de rutas.
- Leer los ejemplos de `React.memo` y `useMemo`, pero ejecutar solo el log del filtrado.
- Presentar caché como cierre conceptual de cuatro minutos.

## Extensión a 75 minutos

- Hacer que el grupo interprete un informe de Lighthouse y formule una hipótesis antes de hablar de la solución.
- Comparar una ruta cargada inicialmente con una ruta cargada mediante `React.lazy`.
- Cambiar `products`, `filter` y un estado no relacionado para observar cuándo se ejecuta el cálculo memorizado.
- Añadir una pregunta de diseño: qué dato se puede reutilizar y cuándo dejaría de ser válido.
- Cerrar con una segunda medición y pedir que el grupo explique qué cambio produjo la diferencia.

## Preguntas de comprobación final

1. ¿Qué muestra FCP y qué muestra LCP?
2. Si el contenido aparece rápido pero los botones no responden, ¿qué métrica investigarías?
3. ¿Por qué dividir el código reduce el coste inicial?
4. ¿Qué papel cumplen `React.lazy` y `Suspense`?
5. ¿Cuándo tiene sentido `useMemo`?
6. ¿Qué error puede producir una dependencia omitida?
7. ¿Qué problema evita la memoria caché?
8. ¿Cuál es el orden del ciclo de trabajo de rendimiento?

## Plan de contingencia

- Si no se puede ejecutar Lighthouse, usar los escenarios numéricos del material y pedir diagnóstico oral.
- Si el proyecto React no tiene rutas, demostrar la carga perezosa con `HeavyModal`, que la fuente presenta como componente condicional pesado.
- Si el ejemplo no muestra re-renderizados, conservar el `console.log` y razonar sobre el cambio de props o dependencias.
- Si el grupo se retrasa, omitir la implementación de caché y conservar su principio: evitar solicitudes redundantes.
- Si se amplía el JSON React con las lecciones faltantes, revisar primero títulos y contenido por posibles duplicados antes de modificar esta guía.

## Cierre sugerido

> Hoy hemos unido medición y optimización. Una métrica nos dice dónde mirar; el código nos ayuda a formular una causa; una intervención concreta cambia el comportamiento; y una nueva medición nos dice si funcionó. La próxima decisión técnica debe empezar con esa evidencia, no con una optimización aplicada por costumbre.
