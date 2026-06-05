# Unified Class Playbook: Object Modeling to Class Diagrams

Esta guia integra en una sola sesion los contenidos de:
- Understanding Objects, Models, Properties and Data
- Object Modeling Diagrams

El foco pedagogico de la clase unica es recorrer el camino completo:
del pensamiento objetual (modelo textual) al modelo visual (UML)
y finalmente al puente hacia implementacion en TypeScript.

## 0. Teaching Intent and Class Promise

Promesa de la sesion: en 120 minutos el estudiante pasa de ideas difusas del dominio
a un modelo de clases legible, defendible y listo para codificar.

Resultados observables al terminar:

- Cada equipo entrega un mini dominio con objetos tipados y metodos coherentes.
- Cada equipo produce un diagrama UML con cardinalidades justificadas.
- Al menos una parte del diagrama se traduce a TypeScript sin ambiguedades de tipos.

## 1. Objetivos de aprendizaje de la clase unica

Al finalizar la sesion, el estudiante deberia poder:

- Diferenciar modelo conceptual, clase y objeto concreto.
  Como explicarlo: partir de un dominio real y construir primero el molde, luego instancias.
- Distinguir propiedades, valores y metodos con criterio de diseno.
  Como explicarlo: separar estado persistente de comportamiento ejecutable.
- Definir estructuras de objetos tipadas, incluyendo arreglos y anidacion.
  Como explicarlo: evolucionar de un objeto simple a una coleccion coherente.
- Leer y construir diagramas de clases con notacion UML basica.
  Como explicarlo: identificar clase, atributos, tipos y relaciones en ejemplos reales.
- Modelar cardinalidades (1:1, 1:N, N:M) y evitar relaciones innecesarias.
  Como explicarlo: justificar cada enlace con reglas del dominio.
- Traducir un diagrama a clases TypeScript iniciales.
  Como explicarlo: mapear cada entidad visual a una estructura de codigo concreta.

## 2. Mapa de contenidos combinado

### Modulo A: Pensamiento objetual (18 lecciones)

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

### Modulo B: Diagramas de clases (18 lecciones)

1. 0 Introduccion al modelado visual de objetos
2. 1 Que son los diagramas de clases
3. 1.1 Conceptos basicos de notacion uml
4. 1.2 Leyendo diagramas de clases existentes
5. 2 De mundo real a modelos visuales
6. 2.1 Definiendo clases y propiedades
7. 2.2 Agregando tipos de datos a propiedades
8. 2.3 Creando tu primer modelo de clase
9. 3 Entendiendo asociaciones de objetos
10. 3.1 Relaciones uno a uno y uno a muchos
11. 3.2 Relaciones muchos a muchos
12. 3.3 Modelando objetos conectados
13. 4 Comenzando general enfoque de arriba hacia abajo
14. 4.1 Evitando objetos copo de nieve y relaciones circulares
15. 4.2 Refinando tus modelos
16. 5 Construyendo un modelo de objetos completo
17. 5.1 Evaluacion de conocimientos de modelado de objetos
18. 6 De diagramas a codigo

## 3. Guion sugerido para clase unica (120 minutos)

### Vista rapida del ritmo de clase

1. Bloques A-B: construir lenguaje comun de modelado.
2. Bloques C-D: consolidar criterio de diseno en objetos reales.
3. Bloques E-F: trasladar decisiones al diagrama UML.
4. Bloques G-H: integrar, defender decisiones y convertir a codigo base.

### Bloque A (15 min): Apertura y marco mental

- Objetivo de la sesion completa: del objeto al diagrama y del diagrama al codigo.
  Como explicarlo: presentar la ruta en tres pasos para que el estudiante vea el hilo conductor.
- Conceptos base: modelo, clase, objeto.
  Como explicarlo: usar un mismo ejemplo (curso, estudiante, inscripcion) para todo el recorrido.

### Bloque B (20 min): Propiedades, valores y tipos

- Propiedad vs valor.
  Como explicarlo: cambiar valores en tiempo real sin tocar estructura.
- Tipado de propiedades.
  Como explicarlo: mostrar que el tipo correcto evita errores de interpretacion.

Ejemplo 1:

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

Ejemplo 2:

```ts
type Usuario = {
  id: number;
  nombre: string;
  online: boolean;
};

const ana: Usuario = { id: 1, nombre: "Ana", online: false };
const pedro: Usuario = { id: 2, nombre: "Pedro", online: true };
console.log(ana.online, pedro.online);
```

### Bloque C (15 min): Metodos y comportamiento

- Cuando usar propiedad y cuando metodo.
  Como explicarlo: preguntar "esto se guarda o se calcula/ejecuta?".

Ejemplo:

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
```

### Bloque D (15 min): Arreglos de objetos y anidacion

- Modelar colecciones de entidades.
  Como explicarlo: operar con filtro, busqueda y lectura de datos anidados.
- Evitar anidacion excesiva.
  Como explicarlo: mostrar alternativa mas mantenible cuando el acceso se vuelve profundo.

Ejemplo:

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

### Bloque E (10 min): Transicion a UML

- Convertir objetos previos en clases candidatas para diagrama.
  Como explicarlo: extraer entidades, atributos y primeras relaciones.
- Notacion UML basica.
  Como explicarlo: caja de clase, atributos tipados y lineas de asociacion.

### Bloque F (15 min): Relaciones y cardinalidades

- Uno a uno, uno a muchos, muchos a muchos.
  Como explicarlo: validar cada cardinalidad con una regla del negocio.
- Entidad intermedia para N:M.
  Como explicarlo: demostrar que la relacion puede tener datos propios.

Ejemplo:

```ts
class Estudiante {
  id: number;
  nombre: string;
  constructor(id: number, nombre: string) {
    this.id = id;
    this.nombre = nombre;
  }
}

class Curso {
  id: number;
  titulo: string;
  constructor(id: number, titulo: string) {
    this.id = id;
    this.titulo = titulo;
  }
}

class Inscripcion {
  estudianteId: number;
  cursoId: number;
  fecha: string;
  constructor(estudianteId: number, cursoId: number, fecha: string) {
    this.estudianteId = estudianteId;
    this.cursoId = cursoId;
    this.fecha = fecha;
  }
}
```

### Bloque G (20 min): Taller integrador

- Actividad guiada en equipos: modelar un dominio completo (biblioteca o ecommerce).
  Como explicarlo: primero objeto textual, luego diagrama UML y finalmente clases base en TypeScript.
- Revision cruzada entre equipos.
  Como explicarlo: evaluar claridad de nombres, coherencia de tipos y calidad de relaciones.

Entregable minimo de taller:

- Lista de 4-6 clases con atributos y tipos.
- 3 relaciones como minimo, incluyendo una cardinalidad no trivial.
- 1 fragmento de codigo TypeScript que represente una clase clave.

### Bloque H (10 min): Cierre y evaluacion rapida

- Checklist final: estructura, comportamiento, relaciones y traduccion a codigo.
  Como explicarlo: preguntas de comprobacion cortas sobre decisiones de modelado.
- Siguiente paso.
  Como explicarlo: continuar con implementacion y validaciones del modelo en ejercicios de codigo.

## 4. Actividades practicas (para la sesion completa)

### Actividad 1 (individual, 10 min)

Definir modelo de una entidad real con propiedades tipadas y al menos un metodo.

### Actividad 2 (parejas, 15 min)

Construir arreglo de objetos y resolver consulta por filtro + busqueda.

### Actividad 3 (parejas, 20 min)

Diseñar diagrama de clases con 4 o mas clases y cardinalidades justificadas.

### Actividad 4 (individual, 10 min)

Traducir una parte del diagrama a clases TypeScript iniciales.

## 5. Preguntas de comprobacion rapida

- Que diferencia practica hay entre propiedad y metodo?
- Cuando una relacion debe modelarse como muchos a muchos?
- Que sintomas indican que un modelo esta sobreanidado?
- Que se gana al pasar del modelo textual al diagrama antes de codificar?

## 6. Errores frecuentes y como corregirlos

- Error: mezclar datos persistentes con logica derivada como si fueran lo mismo.
  Correccion: mantener propiedades para estado y metodos para comportamiento.
- Error: cardinalidades por intuicion, sin regla de negocio.
  Correccion: justificar cada relacion con un caso de uso concreto.
- Error: exceso de relaciones cruzadas o circulares.
  Correccion: simplificar dependencias y refinar desde una estructura top-down.
- Error: llevar el diagrama a codigo sin revisar nombres y tipos.
  Correccion: validar contratos de datos antes de implementar.

## 7. Cierre docente

- Mensaje clave: modelar bien primero reduce errores y acelera la implementacion.
- Resultado esperado: estudiante capaz de diseñar objetos, diagramarlos y traducirlos a codigo base.
- Tarea sugerida: entregar mini proyecto con modelo textual, UML y esqueleto TypeScript.

## 8. Rubrica rapida de evaluacion (0-2 por criterio)

- Claridad del dominio modelado.
  0: confuso, 1: parcialmente claro, 2: claro y consistente.
- Calidad de propiedades y tipos.
  0: ambiguos, 1: aceptables con huecos, 2: precisos y utiles.
- Coherencia de metodos y comportamiento.
  0: mezclado, 1: parcial, 2: bien separado de estado.
- Calidad del diagrama UML.
  0: incompleto, 1: util pero inconsistente, 2: completo y defendible.
- Trazabilidad a TypeScript.
  0: no mapea, 1: mapea parcialmente, 2: mapeo directo y limpio.

## 9. Referencias internas de la clase 10

- Base 1: class_10/resume_01.md
- Base 2: class_10/resume_02.md
- JSON A: class_10/understanding_objects_models_properties_and_da.json
- JSON B: class_10/object_modeling_diagrams.json
