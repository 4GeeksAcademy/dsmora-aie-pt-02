# Guia Docente: Mastering Arrays in TypeScript

Este documento adapta el modulo a una guia para clase online.
El foco es que el estudiante use arrays y matrices para resolver
problemas reales con mayor claridad, eficiencia y control de errores.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar que es un array y por que simplifica el manejo de colecciones.
  Como explicarlo: compara varias variables sueltas vs una sola estructura indexada.
- Crear, acceder y modificar arrays con sintaxis tipada en TypeScript.
  Como explicarlo: parte de ejemplos de lista de tareas, precios o calificaciones.
- Usar metodos esenciales para agregar, remover y consultar elementos.
  Como explicarlo: practica con `push`, `pop`, `shift`, `unshift`, `includes`, `indexOf`.
- Iterar arrays con bucles clasicos y metodos modernos.
  Como explicarlo: resolver el mismo caso con `for`, `for...of`, `forEach`, `map`, `filter`.
- Trabajar con matrices y recorrer datos bidimensionales.
  Como explicarlo: modelar tablero o calendario con `number[][]` y recorrer filas/columnas.
- Aplicar ordenamiento y busqueda segun el tipo de problema.
  Como explicarlo: comparar busqueda lineal vs binaria y discutir requisitos de cada una.

## 2. Mapa del modulo (20 lecciones)

1. 0 Welcome to arrays
2. 1 Understanding arrays
3. 1.1 Creating and accessing arrays
4. 1.2 Adding and removing elements
5. 1.3 Essential array methods
6. 2 Looping through arrays
7. 2.1 Modern iteration methods
8. 2.2 Practical iteration patterns
9. 3 Introduction to matrices
10. 3.1 Working with matrices
11. 3.2 Matrix iteration and access
12. 4 Sorting arrays
13. 4.1 Linear search in arrays
14. 4.2 Binary search algorithm
15. 4.3 Common array pitfalls
16. 4.4 Searching in matrices
17. 5 Array manipulation challenges
18. 5.1 Realworld array problems
19. 5.2 Arrays knowledge test
20. 6 Conclusion and next steps

## 3. Guion sugerido para clase online (90 minutos)

### Bloque A (20 min): Fundamentos de arrays

- Que es un array, indices y tipado basico.
  Como explicarlo: construir ejemplos minimos y visualizar indice inicial en 0.
- Crear, leer y actualizar valores.
  Como explicarlo: modificar elementos en vivo y validar resultados con consola.
- Metodos de insercion y eliminacion.
  Como explicarlo: demostrar impacto de `push/pop` y `shift/unshift` en orden y longitud.

### Bloque B (20 min): Metodos esenciales e iteracion

- `.length`, `.indexOf()`, `.includes()`, `.slice()`, `.concat()`.
  Como explicarlo: resolver preguntas frecuentes (contiene, posicion, sublista, union).
- Bucles clasicos (`for`, `while`, `for...of`).
  Como explicarlo: recorrer listas con control total del indice.
- Iteracion moderna (`forEach`, `map`, `filter`).
  Como explicarlo: separar casos de side effects vs transformacion de datos.

Ejemplo para mostrar en vivo:

```ts
const scores: number[] = [72, 85, 90, 66, 88];

const passed = scores.filter((s) => s >= 70);
const boosted = scores.map((s) => Math.min(s + 5, 100));

console.log(passed, boosted);
```

Catalogo rapido de metodos del modulo (ejemplos de una linea)

```ts
const nums = [10, 20, 30, 40];
const names = ["ana", "luis", "marta"];

nums.push(50); // agrega al final
nums.pop(); // elimina el ultimo
nums.shift(); // elimina el primero
nums.unshift(5); // agrega al inicio
nums.includes(20); // true si existe
nums.indexOf(30); // posicion o -1
nums.slice(1, 3); // copia parcial
nums.splice(1, 1, 25); // elimina/reemplaza en sitio
nums.concat([60, 70]); // une arreglos
names.join(", "); // une en string
nums.forEach((n) => console.log(n)); // recorrido con efecto
nums.map((n) => n * 2); // transforma y retorna
nums.filter((n) => n >= 20); // filtra por condicion
nums.find((n) => n > 25); // primer match
nums.sort((a, b) => a - b); // ordena con comparador
nums.reduce((acc, n) => acc + n, 0); // acumula resultado
nums.some((n) => n > 35); // al menos uno cumple
nums.every((n) => n >= 0); // todos cumplen
nums.at(-1); // acceso por indice relativo
new Array(3).fill(0); // rellena arreglo
```

Metodos mas importantes y usados (ejemplos mas completos)

```ts
type Product = { id: number; name: string; price: number; active: boolean; stock: number };

const products: Product[] = [
  { id: 1, name: "Mouse", price: 25, active: true, stock: 10 },
  { id: 2, name: "Keyboard", price: 50, active: true, stock: 0 },
  { id: 3, name: "Headset", price: 80, active: false, stock: 6 },
  { id: 4, name: "Monitor", price: 190, active: true, stock: 4 },
];

// filter: quedarse con productos vendibles
const sellable = products.filter((p) => p.active && p.stock > 0);

// map: transformar a DTO para UI
const cards = sellable.map((p) => ({
  label: `${p.name} ($${p.price.toFixed(2)})`,
  lowStock: p.stock <= 5,
}));

// find: buscar el primer producto premium
const premium = products.find((p) => p.price > 100);

// sort: ranking por precio descendente sin mutar original
const byPriceDesc = [...products].sort((a, b) => b.price - a.price);

// reduce: total de inventario valorizado
const inventoryValue = products.reduce((acc, p) => acc + p.price * p.stock, 0);

// forEach: NO muta el array por si mismo; se usa para efectos secundarios
products.forEach((p) => {
  if (!p.active) console.log(`Producto inactivo detectado: ${p.name}`);
});

console.log({ cards, premium, top3: byPriceDesc.slice(0, 3), inventoryValue });
```

Nota clave para explicar en clase: metodos que mutan vs no mutan

- Mutan el array original: `push`, `pop`, `shift`, `unshift`, `splice`, `sort`, `reverse`, `fill`.
- No mutan el array original: `forEach`, `map`, `filter`, `find`, `reduce`, `some`, `every`, `includes`, `indexOf`, `slice`, `concat`, `join`, `at`.
- Aclaracion importante: `forEach` no muta por defecto, pero dentro del callback puedes mutar elementos manualmente si los modificas.

Tabla rapida de referencia (metodos principales)

| Metodo | Muta el original | Devuelve nuevo array | Uso tipico |
|---|---|---|---|
| `forEach` | No | No | Recorrer con efectos secundarios |
| `map` | No | Si | Transformar elementos |
| `filter` | No | Si | Filtrar por condicion |
| `find` | No | No | Obtener primer elemento que cumple |
| `sort` | Si | No | Ordenar elementos |
| `reduce` | No | No | Acumular a un valor final |
| `some` | No | No | Verificar si alguno cumple |
| `every` | No | No | Verificar si todos cumplen |
| `includes` | No | No | Comprobar pertenencia |
| `push` | Si | No | Agregar al final |
| `pop` | Si | No | Quitar ultimo elemento |
| `slice` | No | Si | Copiar subarreglo |
| `splice` | Si | Si (elementos removidos) | Insertar/eliminar en posicion |
| `concat` | No | Si | Unir arreglos sin mutar |

Ejemplo corto para distinguir comportamiento:

```ts
const base = [3, 1, 2];

const sortedCopy = [...base].sort((a, b) => a - b); // no muta base por usar copia
base.sort((a, b) => a - b); // si muta base

base.forEach((n, i, arr) => {
  // esto SI muta porque modificamos el arreglo manualmente en el callback
  arr[i] = n * 10;
});
```

### Bloque C (15 min): Patrones practicos de recorrido

- Buscar maximo, minimo, suma y conteos por condicion.
  Como explicarlo: resolver cada patron sobre un carrito de compras.
- Elegir estrategia de iteracion segun objetivo.
  Como explicarlo: comparar legibilidad de `for` vs `reduce` en casos simples.

### Bloque D (15 min): Matrices en TypeScript

- Definicion y modelado con `T[][]`.
  Como explicarlo: usar ejemplos de asientos, tablero o notas por semana.
- Recorrido por filas y columnas.
  Como explicarlo: doble bucle con indices y cuidado de limites.
- Busqueda en matrices.
  Como explicarlo: mostrar cuando conviene barrido completo y como cortar temprano.

### Bloque E (10 min): Ordenamiento, busqueda y errores comunes

- Ordenamiento de arrays.
  Como explicarlo: demostrar orden ascendente/descendente y criterio de comparacion.
- Busqueda lineal vs binaria.
  Como explicarlo: explicar que busqueda binaria requiere datos ordenados.
- Pitfalls comunes.
  Como explicarlo: cubrir off-by-one, mutacion no deseada y supuestos de orden.

### Bloque F (10 min): Desafio y cierre

- Mini reto integrador con arrays y matrices.
  Como explicarlo: pedir solucion paso a paso y justificar metodo elegido.
- Verificacion de conocimientos.
  Como explicarlo: preguntas rapidas para validar comprension de operaciones clave.

## 4. Actividades practicas para la clase

### Actividad 1 (individual, 10 min)

Crear un arreglo de productos y aplicar `filter` + `map` para obtener solo activos con precio final.

### Actividad 2 (parejas, 12 min)

Resolver maximo, minimo y total de una lista numerica, comparando una solucion con `for` y otra con metodos modernos.

### Actividad 3 (individual, 10 min)

Recorrer una matriz de notas, calcular promedio por fila y detectar si existe una nota menor a 60.

## 5. Preguntas de comprobacion rapida

- Que diferencia practica hay entre `map` y `forEach`?
- Cuando conviene busqueda lineal y cuando binaria?
- Que error aparece si asumes indices desde 1 en lugar de 0?
- Que riesgo hay al mutar un array original sin querer?

## 6. Errores frecuentes y como corregirlos

- Error: confundir `forEach` con transformacion de datos.
  Correccion: usar `map` cuando se necesita un nuevo array.
- Error: aplicar busqueda binaria en arreglo no ordenado.
  Correccion: ordenar primero o usar busqueda lineal.
- Error: olvidar validar limites en matrices.
  Correccion: comprobar longitud por fila y controlar indices.
- Error: mutar datos compartidos sin intencion.
  Correccion: clonar antes de transformar cuando el original debe conservarse.

## 7. Cierre para la sesion

- Mensaje clave: arrays y matrices permiten modelar y resolver problemas de datos de forma estructurada.
- Resultado esperado: estudiante capaz de iterar, transformar, buscar y ordenar colecciones con criterio.
- Tarea sugerida: resolver un mini dashboard de ventas con arreglos de productos y matriz semanal.

## 8. Nota de calidad del scraping

El scraping completo las 20 lecciones del modulo y genero el JSON final sin errores.
Se valido presencia de `class_09/mastering_arrays_in_typescript.json` con contenido no vacio.