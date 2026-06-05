# Guia Docente: Understanding Objects, Models, Properties and Data

Este documento adapta el modulo a una guia para clase online.
El foco es que el estudiante piense en terminos de objetos,
separe estructura de comportamiento y modele datos con criterio.
Este resume corresponde a la primera mitad de una clase integrada con resume_02.

## 1. Objetivos de aprendizaje

Al finalizar la clase, el estudiante deberia poder:

- Explicar la diferencia entre modelo conceptual y objeto concreto.
  Como explicarlo: usa un ejemplo de dominio (vehiculo, usuario o producto) para pasar de idea general a instancia real.
- Distinguir propiedad (atributo) y valor (dato actual) en una entidad.
  Como explicarlo: contrasta el esquema de una ficha (campos) con un registro ya completado (valores).
- Definir propiedades con tipos de datos adecuados para cada caso.
  Como explicarlo: decide en vivo cuando usar string, number o boolean segun la regla del negocio.
- Decidir cuando una necesidad se resuelve con propiedad y cuando con metodo.
  Como explicarlo: compara datos persistentes (estado) frente a acciones (comportamiento) en el mismo objeto.
- Modelar arreglos de objetos y estructuras anidadas sin perder legibilidad.
  Como explicarlo: evoluciona de un objeto simple a una coleccion y luego a jerarquias controladas.
- Identificar errores comunes en el diseno de objetos y corregirlos temprano.
  Como explicarlo: revisa ejemplos con campos redundantes, nombres ambiguos y anidacion innecesaria.

## 2. Mapa del modulo (18 lecciones)

1. 0 Bienvenido al pensamiento objetual
2. 1 Definiendo modelos y objetos
3. 1.1 Abstraccion en modelado digital
4. 1.2 Identificando modelos en sistemas
5. 2 Propiedades vs valores explicado
6. 2.1 Definiendo propiedades para modelos
7. 2.2 Tipos de datos en propiedades
8. 2.3 Disenando estructuras de objetos
9. 3 Metodos como propiedades comportamentales
10. 3.1 Agregando comportamiento con metodos
11. 3.2 Eligiendo propiedades o metodos
12. 4 Introduccion a arreglos de objetos
13. 4.1 Construyendo arreglos de objetos
14. 4.2 Objetos anidados y jerarquias
15. 4.3 Disenando estructuras anidadas
16. 4.4 Evitando errores en diseno de objetos
17. 5 Evaluacion de conceptos de objetos
18. 6 Resumen del curso y proximos pasos

## 3. Guion sugerido para clase integrada (Parte 1 de 2, 65 minutos)

### Bloque A (20 min): Pensamiento objetual y abstraccion

- Que es modelar y por que simplifica sistemas complejos.
  Como explicarlo: parte de un escenario real y extrae solo las entidades relevantes.
- Diferencia entre modelo e instancia.
  Como explicarlo: crea un "molde" y luego multiples objetos con datos distintos.
- Identificar modelos en un sistema cotidiano.
  Como explicarlo: mapea rapidamente actores, recursos y eventos en una app conocida.

### Bloque B (20 min): Propiedades, valores y tipos de datos

- Propiedad como definicion, valor como contenido.
  Como explicarlo: muestra cambios de estado del mismo objeto sin alterar su estructura base.
- Tipado de propiedades para prevenir errores.
  Como explicarlo: valida entradas y evidencia que un tipo incorrecto rompe decisiones posteriores.
- Diseno de estructura inicial de objeto.
  Como explicarlo: empezar simple, eliminar ruido y mantener nombres orientados al dominio.

Ejemplo para mostrar en vivo:

```ts
type Producto = {
  id: number;
  nombre: string;
  precio: number;
  activo: boolean;
};

const producto: Producto = {
  id: 101,
  nombre: "Mouse",
  precio: 25.5,
  activo: true,
};
```

Ejemplo adicional: diferencia entre propiedad y valor en tiempo real

```ts
type Usuario = {
  id: number;
  nombre: string;
  online: boolean;
};

const ana: Usuario = { id: 1, nombre: "Ana", online: false };
const pedro: Usuario = { id: 2, nombre: "Pedro", online: true };

// Misma propiedad (online), distinto valor segun la instancia
console.log(ana.online, pedro.online);
```

### Bloque C (20 min): Metodos y comportamiento

- Metodos como acciones del objeto.
  Como explicarlo: pasar de "dato suelto" a "objeto que sabe operar sobre su estado".
- Criterio propiedad vs metodo.
  Como explicarlo: usar pregunta guia "se almacena o se ejecuta?" para decidir diseño.
- Cohesion basica del objeto.
  Como explicarlo: mantener juntos datos y acciones relacionadas, evitando logica dispersa.

Ejemplo para mostrar en vivo: cuando conviene metodo en lugar de propiedad

```ts
type Carrito = {
  items: { nombre: string; precio: number; cantidad: number }[];
  calcularTotal: () => number;
};

const carrito: Carrito = {
  items: [
    { nombre: "Teclado", precio: 40, cantidad: 1 },
    { nombre: "Mouse", precio: 25, cantidad: 2 },
  ],
  calcularTotal() {
    return this.items.reduce((acc, item) => acc + item.precio * item.cantidad, 0);
  },
};

console.log(carrito.calcularTotal());
```

### Bloque D (20 min): Arreglos de objetos y anidacion

- Modelar colecciones de entidades.
  Como explicarlo: crear lista de objetos y ejecutar busquedas/filtrado por propiedad.
- Objetos anidados y jerarquias.
  Como explicarlo: construir un modelo por capas y revisar hasta donde conviene anidar.
- Errores frecuentes de modelado.
  Como explicarlo: detectar duplicidad, campos derivados mal ubicados y anidaciones profundas.

Ejemplo para mostrar en vivo: arreglo de objetos con filtro y busqueda

```ts
type Alumno = {
  id: number;
  nombre: string;
  promedio: number;
  contacto: { email: string; ciudad: string };
};

const alumnos: Alumno[] = [
  { id: 1, nombre: "Lia", promedio: 92, contacto: { email: "lia@mail.com", ciudad: "Madrid" } },
  { id: 2, nombre: "Noa", promedio: 68, contacto: { email: "noa@mail.com", ciudad: "Sevilla" } },
  { id: 3, nombre: "Ian", promedio: 81, contacto: { email: "ian@mail.com", ciudad: "Madrid" } },
];

const destacados = alumnos.filter((a) => a.promedio >= 80);
const alumnoMadrid = alumnos.find((a) => a.contacto.ciudad === "Madrid");

console.log(destacados.map((a) => a.nombre), alumnoMadrid?.nombre);
```

### Bloque E (5 min): Puente hacia diagramas

- Cierre conceptual de modelado textual.
  Como explicarlo: dejar claro que ya tienen clases candidatas, propiedades y relaciones iniciales.
- Transicion a resume_02 en la misma clase.
  Como explicarlo: convertir los objetos ya definidos en un diagrama de clases UML.

## 4. Microejemplos extra para usar durante la clase

### Ejemplo rapido 1: propiedad derivada no debe guardarse

```ts
type Factura = {
  subtotal: number;
  impuesto: number;
  total: () => number;
};

const f: Factura = {
  subtotal: 100,
  impuesto: 21,
  total() {
    return this.subtotal + this.impuesto;
  },
};
```

### Ejemplo rapido 2: evitar anidacion excesiva

```ts
// Menos recomendable
const pedidoA = { cliente: { perfil: { contacto: { email: "x@mail.com" } } } };

// Mas mantenible
const pedidoB = { clienteId: 10, emailContacto: "x@mail.com" };
```

### Ejemplo rapido 3: coleccion de objetos consistente

```ts
type Tarea = { id: number; titulo: string; completada: boolean };
const tareas: Tarea[] = [
  { id: 1, titulo: "Modelar usuario", completada: true },
  { id: 2, titulo: "Modelar curso", completada: false },
];
```

## 5. Actividades practicas para la clase

### Actividad 1 (individual, 10 min)

Definir el modelo de una entidad real (por ejemplo, estudiante) separando propiedades y tipos.

### Actividad 2 (parejas, 12 min)

Convertir un conjunto de datos sueltos en un arreglo de objetos y justificar la estructura elegida.

### Actividad 3 (individual, 10 min)

Refactorizar un objeto anidado excesivo para mejorar claridad sin perder informacion.

## 6. Preguntas de comprobacion rapida

- Que cambia entre un modelo y un objeto concreto?
- Como decides si algo debe ser propiedad o metodo?
- Que ventaja da tipar propiedades desde el inicio?
- Cuando una jerarquia de objetos deja de ser util y pasa a ser compleja?

## 7. Errores frecuentes y como corregirlos

- Error: confundir propiedad con valor.
  Correccion: documentar estructura base del objeto antes de cargar datos.
- Error: usar tipos genericos para todo.
  Correccion: elegir el tipo mas preciso posible por campo.
- Error: convertir acciones en propiedades estaticas.
  Correccion: mover logica a metodos cuando haya comportamiento.
- Error: anidar objetos sin necesidad.
  Correccion: aplanar estructura y conservar solo jerarquias con significado funcional.

## 8. Cierre para la sesion

- Mensaje clave: modelar bien objetos mejora comprension del dominio y calidad del codigo.
- Resultado esperado: estudiante capaz de definir entidades claras, tipadas y con comportamiento coherente.
- Tarea sugerida: llevar las entidades modeladas a resume_02 y representarlas en un diagrama de clases.

## 9. Nota de calidad del scraping

El scraping completo las 18 lecciones del modulo y genero el JSON final sin errores.
Se valido presencia de class_10/understanding_objects_models_properties_and_da.json con contenido no vacio.
